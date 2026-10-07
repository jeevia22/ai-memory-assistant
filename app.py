import os
import json
import sqlite3
import hashlib

import chromadb
import tiktoken

from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"

DB_NAME = "memory.db"

TOKEN_LIMIT = 2500

# Chroma persistent database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

memory_collection = chroma_client.get_or_create_collection(
    name="user_memories"
)

deleted_collection = chroma_client.get_or_create_collection(
    name="deleted_memories"
)

encoder = tiktoken.get_encoding("cl100k_base")


# ============================================================
# SQLITE
# ============================================================

def get_db():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    return conn


def init_db():

    conn = get_db()

    cursor = conn.cursor()

    # Conversation history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Active memories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            fact TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Deleted memories / tombstones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deleted_memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            fact TEXT NOT NULL,
            fact_hash TEXT UNIQUE,
            deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Conversation summaries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ============================================================
# UTILITY
# ============================================================

def fact_hash(category, fact):

    text = f"{category}:{fact}".lower().strip()

    return hashlib.sha256(text.encode()).hexdigest()


def count_tokens(text):

    return len(encoder.encode(text))


# ============================================================
# SQLITE MEMORY FUNCTIONS
# ============================================================

def get_all_memories():

    conn = get_db()

    rows = conn.execute("""
        SELECT *
        FROM memories
        ORDER BY updated_at DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_memory(memory_id):

    conn = get_db()

    row = conn.execute(
        "SELECT * FROM memories WHERE id=?",
        (memory_id,)
    ).fetchone()

    conn.close()

    return dict(row) if row else None


def add_memory(category, fact):

    # First check deleted facts
    h = fact_hash(category, fact)

    conn = get_db()

    deleted = conn.execute(
        "SELECT * FROM deleted_memories WHERE fact_hash=?",
        (h,)
    ).fetchone()

    if deleted:

        conn.close()

        return False

    cursor = conn.execute("""
        INSERT INTO memories(category, fact)
        VALUES (?, ?)
    """, (category, fact))

    memory_id = cursor.lastrowid

    conn.commit()

    conn.close()

    # Store semantic representation in Chroma
    memory_collection.add(
        ids=[str(memory_id)],
        documents=[fact],
        metadatas=[{
            "category": category
        }]
    )

    return True


def update_memory(memory_id, category, fact):

    old_memory = get_memory(memory_id)

    if not old_memory:
        return False

    conn = get_db()

    conn.execute("""
        UPDATE memories
        SET category=?,
            fact=?,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """, (category, fact, memory_id))

    conn.commit()

    conn.close()

    # Replace Chroma document
    memory_collection.delete(
        ids=[str(memory_id)]
    )

    memory_collection.add(
        ids=[str(memory_id)],
        documents=[fact],
        metadatas=[{
            "category": category
        }]
    )

    return True


def delete_memory(memory_id):

    memory = get_memory(memory_id)

    if not memory:
        return False

    h = fact_hash(
        memory["category"],
        memory["fact"]
    )

    conn = get_db()

    # Store tombstone
    conn.execute("""
        INSERT OR IGNORE INTO deleted_memories
        (category, fact, fact_hash)
        VALUES (?, ?, ?)
    """, (
        memory["category"],
        memory["fact"],
        h
    ))

    # Delete active memory
    conn.execute(
        "DELETE FROM memories WHERE id=?",
        (memory_id,)
    )

    conn.commit()

    conn.close()

    # Remove from active vector DB
    try:
        memory_collection.delete(
            ids=[str(memory_id)]
        )
    except Exception:
        pass

    # Store deleted memory semantically
    deleted_collection.upsert(
        ids=[h],
        documents=[memory["fact"]],
        metadatas=[{
            "category": memory["category"]
        }]
    )

    return True


# ============================================================
# VECTOR MEMORY RETRIEVAL
# ============================================================

def retrieve_memories(query, n=5):

    try:

        results = memory_collection.query(
            query_texts=[query],
            n_results=n
        )

        documents = results.get("documents", [[]])[0]

        return documents

    except Exception as e:

        print("Vector retrieval error:", e)

        return []


def retrieve_deleted_memories(query):

    try:

        results = deleted_collection.query(
            query_texts=[query],
            n_results=3
        )

        documents = results.get("documents", [[]])[0]

        return documents

    except Exception:

        return []


# ============================================================
# LLM CALL
# ============================================================

def ask_llm(messages):

    response = client.chat.completions.create(

        model=MODEL,

        messages=messages,

        temperature=0.2,

        max_tokens=1000
    )

    return response.choices[0].message.content


# ============================================================
# MEMORY EXTRACTION
# ============================================================

def extract_memories(user_message):

    existing = get_all_memories()

    existing_text = "\n".join(
        [
            f"{m['id']} | {m['category']} | {m['fact']}"
            for m in existing
        ]
    )

    prompt = f"""
You are a memory extraction system.

Extract ONLY lasting facts about the user.

Examples:
"I prefer Python" -> programming_language = Python
"I live in Madurai" -> location = Madurai
"I'm preparing for GATE" -> goal = preparing for GATE
"I am a final year student" -> education_status = final year student

Do NOT store:
- temporary questions
- general statements
- facts about other people
- information that is only relevant to this conversation

Existing memories:

{existing_text}

User message:

{user_message}

Return ONLY valid JSON:

{{
    "memories": [
        {{
            "category": "string",
            "fact": "string",
            "action": "ADD | UPDATE | IGNORE",
            "existing_id": null
        }}
    ]
}}

Rules:

1. If the fact is new -> ADD.
2. If it conflicts with an existing memory -> UPDATE.
3. If the fact is already stored -> IGNORE.
4. Do not create duplicates.
5. existing_id must contain the ID of the old memory for UPDATE.
"""

    try:

        result = ask_llm([
            {
                "role": "system",
                "content": prompt
            }
        ])

        # Remove accidental markdown
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        return json.loads(result)

    except Exception as e:

        print("Memory extraction error:", e)

        return {"memories": []}


# ============================================================
# PROCESS MEMORIES
# ============================================================

def process_memories(user_message):

    extracted = extract_memories(user_message)

    for item in extracted.get("memories", []):

        category = item.get("category")
        fact = item.get("fact")
        action = item.get("action")
        existing_id = item.get("existing_id")

        if not category or not fact:
            continue

        # ----------------------------------------------------
        # Check whether user previously deleted this fact
        # ----------------------------------------------------

        deleted_matches = retrieve_deleted_memories(fact)

        if deleted_matches:

            # Simple semantic safety check
            if fact.lower() in [
                x.lower() for x in deleted_matches
            ]:

                print("Blocked deleted memory:", fact)

                continue

        # ----------------------------------------------------
        # ADD
        # ----------------------------------------------------

        if action == "ADD":

            add_memory(
                category,
                fact
            )

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        elif action == "UPDATE" and existing_id:

            update_memory(
                int(existing_id),
                category,
                fact
            )

        # ----------------------------------------------------
        # IGNORE
        # ----------------------------------------------------

        else:

            pass


# ============================================================
# CONVERSATION HISTORY
# ============================================================

def get_messages():

    conn = get_db()

    rows = conn.execute("""
        SELECT role, content
        FROM messages
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [
        {
            "role": row["role"],
            "content": row["content"]
        }
        for row in rows
    ]


def save_message(role, content):

    conn = get_db()

    conn.execute("""
        INSERT INTO messages(role, content)
        VALUES (?, ?)
    """, (role, content))

    conn.commit()

    conn.close()


# ============================================================
# SUMMARIZATION
# ============================================================

def summarize_old_messages():

    messages = get_messages()

    if not messages:
        return

    total_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in messages
    )

    if count_tokens(total_text) <= TOKEN_LIMIT:
        return

    # Keep latest 6 messages
    old_messages = messages[:-6]

    if not old_messages:
        return

    old_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in old_messages
    )

    prompt = f"""
Summarize the following older conversation.

Keep:
- important decisions
- user goals
- important context
- unresolved tasks
- useful preferences

Do not invent information.

Conversation:

{old_text}
"""

    summary = ask_llm([
        {
            "role": "system",
            "content": prompt
        }
    ])

    conn = get_db()

    conn.execute("""
        INSERT INTO summaries(summary)
        VALUES (?)
    """, (summary,))

    # Delete old messages
    old_count = len(old_messages)

    conn.execute("""
        DELETE FROM messages
        WHERE id IN (
            SELECT id
            FROM messages
            ORDER BY id ASC
            LIMIT ?
        )
    """, (old_count,))

    conn.commit()

    conn.close()


def get_latest_summary():

    conn = get_db()

    row = conn.execute("""
        SELECT summary
        FROM summaries
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()

    conn.close()

    if row:
        return row["summary"]

    return ""


# ============================================================
# CHAT API
# ============================================================

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json

    user_message = data.get("message", "").strip()

    if not user_message:

        return jsonify({
            "error": "Message required"
        }), 400

    # --------------------------------------------------------
    # 1. Save user message
    # --------------------------------------------------------

    save_message(
        "user",
        user_message
    )

    # --------------------------------------------------------
    # 2. Extract lasting facts
    # --------------------------------------------------------

    process_memories(
        user_message
    )

    # --------------------------------------------------------
    # 3. Retrieve relevant memories
    # --------------------------------------------------------

    memories = retrieve_memories(
        user_message,
        n=5
    )

    memory_text = "\n".join(
        f"- {m}"
        for m in memories
    )

    # --------------------------------------------------------
    # 4. Conversation summary
    # --------------------------------------------------------

    summary = get_latest_summary()

    # --------------------------------------------------------
    # 5. Recent messages
    # --------------------------------------------------------

    history = get_messages()

    recent_history = history[-8:]

    # --------------------------------------------------------
    # 6. Build prompt
    # --------------------------------------------------------

    system_prompt = f"""
You are a helpful AI assistant with persistent user memory.

Relevant user memories:
{memory_text}

Previous conversation summary:
{summary}

Use memories naturally when relevant.

Do not claim to remember something unless it appears in the
provided memory/context.

If the user corrects a memory, follow the latest information.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(recent_history)

    # --------------------------------------------------------
    # 7. Generate answer
    # --------------------------------------------------------

    answer = ask_llm(messages)

    # --------------------------------------------------------
    # 8. Save assistant response
    # --------------------------------------------------------

    save_message(
        "assistant",
        answer
    )

    # --------------------------------------------------------
    # 9. Summarize if needed
    # --------------------------------------------------------

    summarize_old_messages()

    return jsonify({
        "response": answer,
        "memories": get_all_memories()
    })


# ============================================================
# MEMORY API
# ============================================================

@app.route("/api/memories", methods=["GET"])
def memories():

    return jsonify(
        get_all_memories()
    )


@app.route("/api/memories/<int:memory_id>", methods=["PUT"])
def edit_memory(memory_id):

    data = request.json

    category = data.get("category")
    fact = data.get("fact")

    if not category or not fact:

        return jsonify({
            "error": "category and fact required"
        }), 400

    update_memory(
        memory_id,
        category,
        fact
    )

    return jsonify({
        "success": True
    })


@app.route("/api/memories/<int:memory_id>", methods=["DELETE"])
def remove_memory(memory_id):

    success = delete_memory(
        memory_id
    )

    if not success:

        return jsonify({
            "error": "Memory not found"
        }), 404

    return jsonify({
        "success": True
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )