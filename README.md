Copy everything below into your `README.md`:

```markdown
# 🧠 AI Memory Assistant

An AI-powered full-stack chat assistant that remembers important facts about users across sessions and allows users to view, edit, and delete what the AI remembers.

The application combines an LLM, SQLite, and ChromaDB to provide persistent memory, semantic retrieval, conversation summarization, and user-controlled memory management.

---

## 🚀 Features

### 1. Persistent User Memory

The assistant automatically extracts lasting, user-specific facts from each conversation turn.

For example:

> "I prefer Python for programming."

The system extracts:

```text
Category: programming_language
Fact: The user prefers Python.
```

Only useful, lasting facts are intended to be stored rather than every conversation message.

---

### 2. Memory Conflict Resolution

When a user provides information that conflicts with an existing memory, the system updates the existing memory instead of creating a duplicate.

Example:

```text
User: I prefer Python.

Memory:
programming_language → Python

User: Actually, I prefer Java now.

Memory:
programming_language → Java
```

This keeps the user's memory consistent with their latest information.

---

### 3. Semantic Memory Retrieval

Relevant memories are retrieved using vector similarity search through ChromaDB.

For example, if the stored memory is:

```text
The user prefers backend development.
```

and the user asks:

> "What type of development should I focus on?"

the system can retrieve the relevant memory even when the wording is different.

Only relevant memories are included in the LLM context.

---

### 4. Cross-Session Memory

User memories are stored persistently using SQLite and ChromaDB.

The assistant can therefore retrieve previously stored information even after restarting the Flask application.

---

### 5. Automatic Conversation Summarization

The application monitors the size of conversation history using token counting.

When the conversation exceeds the configured token limit:

```text
Older Conversation
        ↓
LLM Summarization
        ↓
Compact Summary
        ↓
SQLite
```

The summary is then used as context instead of continuously sending the entire older conversation to the LLM.

---

### 6. User-Controlled Memory Panel

The application provides a memory panel where users can:

- View stored memories
- Edit memories
- Delete memories

This gives users visibility and control over persistent AI memory.

---

### 7. Deleted Memory Protection

When a user deletes a memory, the system maintains a deletion record, also known as a tombstone.

```text
Active Memory
     ↓
   DELETE
     ↓
Remove from active memory
     ↓
Store deletion record
     ↓
Prevent automatic re-storage
```

This prevents the system from automatically recreating a fact that the user intentionally deleted.

---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │     User Interface   │
                    │      HTML/CSS/JS     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │        Flask         │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼─────────────────┐
              │                │                 │
              ▼                ▼                 ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │   SQLite    │  │  ChromaDB   │  │    Groq     │
       │             │  │             │  │     LLM     │
       │ Memories    │  │ Embeddings  │  │             │
       │ Messages    │  │ Similarity  │  │ Chat        │
       │ Summaries   │  │ Search      │  │ Extraction  │
       │ Deletions   │  │             │  │ Summarizing │
       └─────────────┘  └─────────────┘  └─────────────┘
```

---

# 🔄 Application Workflow

```text
User Message
     │
     ▼
Save Conversation
     │
     ▼
Extract Lasting Facts
     │
     ▼
ADD / UPDATE / IGNORE
     │
     ▼
Check Deleted Memories
     │
     ▼
Store in SQLite + ChromaDB
     │
     ▼
Retrieve Relevant Memories
     │
     ▼
Retrieve Conversation Summary
     │
     ▼
Retrieve Recent Messages
     │
     ▼
Build LLM Context
     │
     ▼
Generate AI Response
     │
     ▼
Save Response
     │
     ▼
Check Token Limit
     │
     ├── Within Limit ──→ Continue
     │
     └── Exceeded ─────→ Summarize Older Messages
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Flask | Backend and REST APIs |
| HTML/CSS/JavaScript | Frontend interface |
| Groq | LLM for chat, memory extraction and summarization |
| SQLite | Persistent structured storage |
| ChromaDB | Vector database and semantic retrieval |
| tiktoken | Token counting |
| python-dotenv | Environment variable management |

---

# 🗄️ Data Storage

## SQLite

SQLite acts as the structured source of truth for the application.

### `memories`

Stores active user memories.

```text
id
category
fact
created_at
updated_at
```

### `messages`

Stores conversation history.

```text
id
role
content
created_at
```

### `summaries`

Stores summaries of older conversation history.

```text
id
summary
created_at
```

### `deleted_memories`

Stores deleted memory records/tombstones.

```text
id
category
fact
fact_hash
deleted_at
```

---

## ChromaDB

ChromaDB acts as the semantic retrieval layer.

It is used for:

- Memory embeddings
- Similarity search
- Relevant memory retrieval

### Why SQLite + ChromaDB?

The two databases have different responsibilities.

**SQLite provides:**

- Structured storage
- CRUD operations
- Memory IDs
- Timestamps
- Conversation history
- Conversation summaries
- Deleted-memory records

**ChromaDB provides:**

- Vector embeddings
- Semantic similarity search
- Relevant memory retrieval

SQLite therefore acts as the structured source of truth, while ChromaDB is used for semantic retrieval.

---

# 🧠 Memory Extraction

The LLM analyzes each user message and determines whether a lasting fact should be:

```text
ADD
UPDATE
IGNORE
```

Example:

```json
{
    "category": "programming_language",
    "fact": "The user prefers Java.",
    "action": "UPDATE",
    "existing_id": 1
}
```

### Examples of lasting information

```text
"I prefer Python."
"I'm preparing for GATE."
"I prefer backend development."
"I'm interested in artificial intelligence."
```

### Examples of temporary information

```text
"What is machine learning?"
"Explain Python loops."
"How does SQL JOIN work?"
```

The goal is to store lasting, user-specific information rather than every message.

---

# 🔎 Memory Retrieval

When a new user message arrives:

```text
User Query
    ↓
Semantic Search
    ↓
ChromaDB
    ↓
Relevant Memories
    ↓
LLM Context
    ↓
AI Response
```

This allows the assistant to use relevant memories without sending every stored memory to the LLM.

---

# 🧾 Conversation Summarization

The application monitors the conversation using token counting.

When the configured token limit is exceeded:

```text
Conversation History
        ↓
Token Count
        ↓
Limit Exceeded
        ↓
Summarize Older Messages
        ↓
Store Summary in SQLite
        ↓
Keep Recent Messages
```

This reduces context size while preserving important conversational information.

---

# 🔐 Memory Deletion

When a user deletes a memory:

```text
User clicks Delete
        ↓
Remove active memory from SQLite
        ↓
Remove vector from ChromaDB
        ↓
Create deletion tombstone
        ↓
Prevent future automatic re-storage
```

The deletion record helps ensure that an intentionally deleted memory is not automatically recreated by the memory extraction process.

---

# 📁 Project Structure

```text
ai-memory-assistant/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
└── screenshots/
    └── demo.png
```

Runtime files such as `.env`, `memory.db`, `chroma_db/`, and Python cache files should not be committed to the repository.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/jeevia22/ai-memory-assistant.git
```

```bash
cd ai-memory-assistant
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit the `.env` file or your API key to GitHub.

A `.env.example` file is provided as a template.

---

## 5. Run the application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

# 🧪 Testing

## Test 1 — Add a Memory

Send:

```text
I prefer Python for programming.
```

Expected memory:

```text
programming_language
The user prefers Python.
```

---

## Test 2 — Update a Conflicting Memory

Send:

```text
Actually, I prefer Java now.
```

Expected:

```text
programming_language
The user prefers Java.
```

The old Python preference should not remain as an active duplicate.

---

## Test 3 — Retrieve a Memory

Ask:

```text
Which programming language do I prefer?
```

The assistant should retrieve the relevant memory and respond using it.

---

## Test 4 — Cross-Session Persistence

Restart the Flask application and ask:

```text
Which programming language do I prefer?
```

The previously stored memory should still be available.

---

## Test 5 — Edit a Memory

Use the **Edit** button in the memory panel to modify an existing memory.

The updated memory should persist after refreshing the application.

---

## Test 6 — Delete a Memory

Use the **Delete** button to remove a memory.

The memory should disappear from the active memory panel.

---

## Test 7 — Deleted Memory Protection

After deleting a memory, provide the same information again and verify that the system does not automatically recreate the deleted memory.

---

## Test 8 — Conversation Summarization

Temporarily reduce the token limit and have a longer conversation.

When the limit is exceeded, older messages should be summarized and stored in the `summaries` table.

---

# 🎯 Problem Statement

Build an AI chat assistant that:

1. Extracts lasting facts about users after every conversation turn.
2. Stores memories using structured and vector storage.
3. Updates conflicting memories instead of creating duplicates.
4. Retrieves relevant memories for future messages.
5. Automatically summarizes older conversations when the token limit is exceeded.
6. Provides a memory panel to view, edit, and delete stored memories.
7. Prevents explicitly deleted facts from being automatically stored again.

This project implements these requirements using an LLM-powered persistent memory pipeline.

---

# ⚠️ Current Limitations

This project is implemented as a functional prototype.

Current limitations include:

- SQLite is suitable for a local prototype but is not ideal for large-scale concurrent workloads.
- Memory extraction depends on LLM output quality.
- Semantic retrieval requires appropriate similarity thresholds.
- Deleted-memory matching can be improved with stronger semantic similarity checks.
- Authentication and authorization are not implemented.
- The current implementation is designed primarily for a single-user/local environment.

---

# 🔮 Future Improvements

For production deployment, the system could be extended with:

- User authentication and authorization
- PostgreSQL for scalable structured storage
- pgvector or a managed vector database
- Structured JSON schema validation for memory extraction
- Memory confidence scoring
- Better semantic duplicate detection
- Improved deleted-memory similarity matching
- Encryption of sensitive user information
- Rate limiting
- Docker deployment
- Cloud deployment
- Multi-user support
- Automated unit and integration testing
- Logging and monitoring
- API versioning

---

# 📸 Demo

![AI Memory Assistant](screenshots/demo.png)

The interface contains:

- AI chat interface
- Persistent memory panel
- Memory editing
- Memory deletion
- Context-aware responses

---

# 🎓 Key Concepts Demonstrated

This project demonstrates practical implementation of:

- Large Language Models (LLMs)
- Prompt Engineering
- Persistent AI Memory
- Vector Databases
- Semantic Search
- Retrieval-Augmented Generation concepts
- Conversation Summarization
- Token Management
- CRUD APIs
- REST API development
- SQLite database management
- Full-stack application development
- User-controlled AI memory
- Data deletion and tombstone records

---

# 👩‍💻 Author

**Jeevia Harshini M**

AI & Data Science

GitHub: [jeevia22](https://github.com/jeevia22)

---

## ⭐ Key Takeaway

The project combines:

```text
LLM
 +
Persistent Memory
 +
Vector Retrieval
 +
Conversation Summarization
 +
User-Controlled Memory
```

to build a personalized and controllable conversational AI assistant.
```

**One correction before you commit:** make sure your `.env.example` contains only:

```env
GROQ_API_KEY=your_groq_api_key_here
```

and **not your real `gsk_...` key**, since GitHub already blocked your previous push for detecting a Groq secret.
