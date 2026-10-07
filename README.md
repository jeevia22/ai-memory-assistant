# 🧠 AI Memory Assistant

An AI-powered full-stack chat assistant that remembers important facts about users across sessions and allows users to view, edit, and delete what the assistant remembers.

The application combines **Flask, Groq LLM, SQLite, ChromaDB, and JavaScript** to implement persistent user memory, semantic retrieval, conversation summarization, and user-controlled memory management.

---

## 🚀 Features

- 🧠 Persistent user memory across sessions
- 🔍 Semantic memory retrieval using ChromaDB
- 🔄 Automatic memory conflict detection and updating
- ➕ Automatic extraction of lasting user facts
- 📝 Conversation summarization when token limits are exceeded
- 👁️ View stored memories
- ✏️ Edit stored memories
- 🗑️ Delete stored memories
- 🔐 Deleted-memory protection using tombstones
- 💬 Context-aware AI responses
- 🗄️ SQLite-based persistent storage
- 🌐 Full-stack web interface

---

## 📌 Problem Statement

Build an AI chat assistant that:

1. Extracts lasting facts about the user after every conversation turn.
2. Stores those facts using a structured database and a vector database.
3. Updates conflicting facts instead of creating duplicate memories.
4. Retrieves relevant memories for every new user message.
5. Automatically summarizes older conversation history when the token limit is exceeded.
6. Provides a memory panel where users can view, edit, and delete stored memories.
7. Prevents explicitly deleted memories from being automatically stored again.

---

## 🏗️ Architecture

```text
                         ┌───────────────────┐
                         │       USER        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   HTML / CSS / JS │
                         │     Frontend      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │      Flask        │
                         │     Backend       │
                         └─────────┬─────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
          ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
          │   SQLite    │   │  ChromaDB   │   │    Groq     │
          │             │   │             │   │     LLM     │
          │ Memories    │   │ Embeddings  │   │             │
          │ Messages    │   │ Similarity  │   │ Chat        │
          │ Summaries   │   │ Search      │   │ Extraction  │
          │ Deletions   │   │             │   │ Summarizing |
          └─────────────┘   └─────────────┘   └─────────────┘

Absolutely — here is a **single, clean, professional README** you can copy directly into `README.md`.

```markdown
# 🧠 AI Memory Assistant

An AI-powered full-stack chat assistant that remembers important facts about users across sessions and allows users to view, edit, and delete what the assistant remembers.

The application combines **Flask, Groq LLM, SQLite, ChromaDB, and JavaScript** to implement persistent user memory, semantic retrieval, conversation summarization, and user-controlled memory management.

---

## 🚀 Features

- 🧠 Persistent user memory across sessions
- 🔍 Semantic memory retrieval using ChromaDB
- 🔄 Automatic memory conflict detection and updating
- ➕ Automatic extraction of lasting user facts
- 📝 Conversation summarization when token limits are exceeded
- 👁️ View stored memories
- ✏️ Edit stored memories
- 🗑️ Delete stored memories
- 🔐 Deleted-memory protection using tombstones
- 💬 Context-aware AI responses
- 🗄️ SQLite-based persistent storage
- 🌐 Full-stack web interface

---

## 📌 Problem Statement

Build an AI chat assistant that:

1. Extracts lasting facts about the user after every conversation turn.
2. Stores those facts using a structured database and a vector database.
3. Updates conflicting facts instead of creating duplicate memories.
4. Retrieves relevant memories for every new user message.
5. Automatically summarizes older conversation history when the token limit is exceeded.
6. Provides a memory panel where users can view, edit, and delete stored memories.
7. Prevents explicitly deleted memories from being automatically stored again.

---

## 🏗️ Architecture

```text
                         ┌───────────────────┐
                         │       USER        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   HTML / CSS / JS │
                         │     Frontend      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │      Flask        │
                         │     Backend       │
                         └─────────┬─────────┘
                                   │
                 ┌─────────────────┼─────────────────┐
                 │                 │                 │
                 ▼                 ▼                 ▼
          ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
          │   SQLite    │   │  ChromaDB   │   │    Groq     │
          │             │   │             │   │     LLM     │
          │ Memories    │   │ Embeddings  │   │             │
          │ Messages    │   │ Similarity  │   │ Chat        │
          │ Summaries   │   │ Search      │   │ Extraction  │
          │ Deletions   │   │             │   │ Summarizing │
          └─────────────┘   └─────────────┘   └─────────────┘
```

### Component Responsibilities

| Component | Purpose |
|---|---|
| **HTML/CSS/JavaScript** | Chat UI and memory management panel |
| **Flask** | Backend API and application logic |
| **Groq LLM** | Chat generation, memory extraction, summarization |
| **SQLite** | Structured persistent storage |
| **ChromaDB** | Vector storage and semantic retrieval |
| **tiktoken** | Token counting |
| **python-dotenv** | Environment variable management |

---

## 🔄 Application Workflow

```text
                    USER MESSAGE
                         │
                         ▼
                  Save Message
                         │
                         ▼
             Extract Lasting Facts
                         │
                         ▼
                  ADD / UPDATE /
                     IGNORE
                         │
                         ▼
              Check Deleted Memories
                         │
                         ▼
                SQLite + ChromaDB
                         │
                         ▼
              Retrieve Relevant Memory
                         │
                         ▼
              Retrieve Conversation
                    Summary
                         │
                         ▼
               Retrieve Recent
                   Messages
                         │
                         ▼
                 Build LLM Prompt
                         │
                         ▼
                    Groq LLM
                         │
                         ▼
                  AI Response
                         │
                         ▼
                 Save Response
                         │
                         ▼
                Check Token Limit
                         │
              ┌──────────┴──────────┐
              │                     │
          Within Limit          Exceeded
              │                     │
              │                     ▼
              │              Summarize Older
              │                 Messages
              │                     │
              └──────────┬──────────┘
                         ▼
                       DONE
```

---

## 🧠 Persistent Memory

After every user message, the system uses the LLM to identify lasting user-specific facts.

For example:

```text
User:
I prefer Python for programming.
```

The memory extraction layer produces:

```text
Category:
programming_language

Fact:
The user prefers Python.
```

The fact is then stored in SQLite and indexed in ChromaDB.

### Information suitable for memory

```text
I prefer Python.
I'm preparing for GATE.
I prefer backend development.
I'm interested in artificial intelligence.
```

### Information that should not normally become memory

```text
What is machine learning?
Explain Python loops.
What is a SQL JOIN?
```

The goal is to store **lasting user information**, not every conversation message.

---

## 🔄 Memory Conflict Resolution

The system prevents duplicate conflicting memories.

Example:

```text
User:
I prefer Python.

Stored:
programming_language → Python
```

Later:

```text
User:
Actually, I prefer Java now.
```

The system updates the existing memory:

```text
programming_language → Java
```

instead of storing:

```text
Python
Java
```

The memory extraction process classifies candidate memories as:

```text
ADD
UPDATE
IGNORE
```

---

## 🔎 Semantic Memory Retrieval

ChromaDB is used to retrieve memories that are semantically relevant to the current message.

```text
User Query
     │
     ▼
ChromaDB Similarity Search
     │
     ▼
Relevant Memories
     │
     ▼
LLM Context
     │
     ▼
AI Response
```

For example, the stored memory may be:

```text
The user prefers backend development.
```

The user can ask:

```text
What type of development should I focus on?
```

The system can retrieve the relevant memory even when the wording is different.

This allows the assistant to follow the principle:

> **Store persistent facts, but retrieve only what is relevant.**

---

## 💬 Cross-Session Memory

Memories are persisted using SQLite and ChromaDB rather than being kept only in application memory.

Therefore, after restarting the Flask application, previously stored memories can still be retrieved.

Example:

```text
Session 1:
User → I prefer Java.

        ↓

Memory stored

        ↓

Application restarted

        ↓

Session 2:
User → What programming language do I prefer?

AI → You prefer Java.
```

---

## 📝 Conversation Summarization

Conversation history grows as the user continues chatting.

To prevent the LLM context from becoming unnecessarily large, the application monitors the token count.

```text
Conversation History
        │
        ▼
   Token Counting
        │
        ▼
Token Limit Exceeded?
       /       \
     No         Yes
     │           │
     │           ▼
     │      Summarize Older
     │       Conversation
     │           │
     │           ▼
     │        SQLite
     │
     └───────────┘
```

The application retains recent messages while older messages are compressed into a summary.

### Memory vs Summary

| Persistent Memory | Conversation Summary |
|---|---|
| Long-term user fact | Compressed conversation context |
| User preference, goal, etc. | Important points from older messages |
| User can edit/delete | Automatically generated |
| Stored independently | Used for context management |

---

## 🎛️ Memory Management Panel

The application provides a dedicated memory panel.

Users can:

### View

See what the assistant currently remembers.

### Edit

Modify an existing memory.

### Delete

Remove an existing memory.

Example:

```text
┌──────────────────────────────────┐
│        🧠 My Memories            │
├──────────────────────────────────┤
│                                  │
│ programming_language             │
│ The user prefers Java.           │
│                                  │
│ [Edit]        [Delete]           │
│                                  │
├──────────────────────────────────┤
│                                  │
│ interest                         │
│ The user is interested in AI.    │
│                                  │
│ [Edit]        [Delete]           │
│                                  │
└──────────────────────────────────┘
```

---

## 🗑️ Deleted Memory Protection

Deleting a memory does more than remove it from the UI.

The system:

```text
User Deletes Memory
        │
        ├── Remove active SQLite record
        │
        ├── Remove ChromaDB vector
        │
        └── Store deletion tombstone
```

The deletion record allows the application to recognize that the user intentionally removed the information.

When a future memory candidate is extracted:

```text
New Candidate Memory
        │
        ▼
Previously Deleted?
      /     \
    YES      NO
     │        │
   BLOCK     STORE
```

This helps prevent a deleted fact from being automatically recreated.

---

# 🗄️ Data Storage

## SQLite

SQLite acts as the **structured source of truth**.

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

Stores summaries of older conversations.

```text
id
summary
created_at
```

### `deleted_memories`

Stores deletion tombstones.

```text
id
category
fact
fact_hash
deleted_at
```

---

## ChromaDB

ChromaDB acts as the **semantic retrieval layer**.

It is used for:

- Memory embeddings
- Similarity search
- Relevant memory retrieval

### Why use SQLite and ChromaDB together?

They have different responsibilities.

**SQLite provides:**

- Structured persistence
- CRUD operations
- IDs
- Timestamps
- Conversation history
- Summaries
- Deletion records

**ChromaDB provides:**

- Vector embeddings
- Semantic search
- Relevant memory retrieval

Therefore:

> **SQLite is the structured source of truth, while ChromaDB is the semantic retrieval layer.**

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

Runtime files are intentionally excluded from Git:

```text
.env
memory.db
chroma_db/
__pycache__/
```

---

# ⚙️ Installation

## Prerequisites

- Python 3.10+
- Git
- Groq API key

---

## 1. Clone the Repository

```bash
git clone https://github.com/jeevia22/ai-memory-assistant.git
```

```bash
cd ai-memory-assistant
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure the API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Never commit your `.env` file or expose your API key publicly.**

The repository contains `.env.example` only as a configuration template.

---

## 5. Run the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🧪 Testing

### Test 1 — Add Memory

Send:

```text
I prefer Python for programming.
```

Expected:

```text
programming_language
The user prefers Python.
```

---

### Test 2 — Update Memory

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

### Test 3 — Retrieve Memory

Ask:

```text
Which programming language do I prefer?
```

The assistant should respond using the stored memory.

---

### Test 4 — Cross-Session Persistence

Restart the Flask application and ask:

```text
Which programming language do I prefer?
```

The previously stored memory should still be available.

---

### Test 5 — Edit Memory

Use the **Edit** button in the memory panel.

Modify an existing fact and refresh the application.

The updated value should persist.

---

### Test 6 — Delete Memory

Use the **Delete** button.

The memory should disappear from the active memory panel.

---

### Test 7 — Deleted Memory Protection

After deleting a memory, provide the same fact again.

The application should prevent the previously deleted fact from being automatically recreated as persistent memory.

---

### Test 8 — Conversation Summarization

Temporarily lower the token limit and conduct a longer conversation.

When the token limit is exceeded, older conversation messages should be summarized and stored in SQLite.

---

# 📸 Demo

Add a screenshot of the running application:

```markdown
![AI Memory Assistant](screenshots/demo.png)
```

The interface demonstrates:

- AI chat
- Persistent memory
- Memory retrieval
- Memory editing
- Memory deletion

---

# 🎯 Requirements Mapping

| Requirement | Implementation |
|---|---|
| Extract lasting facts | Groq LLM memory extraction |
| Store memories | SQLite + ChromaDB |
| Update conflicting facts | ADD / UPDATE / IGNORE logic |
| Retrieve relevant memories | ChromaDB semantic search |
| Summarize long conversations | Groq + tiktoken |
| View memories | Memory panel |
| Edit memories | Flask PUT API |
| Delete memories | Flask DELETE API |
| Prevent deleted memory re-storage | Deleted-memory tombstones |

---

# ⚠️ Limitations

This project is implemented as a functional prototype.

Current limitations include:

- SQLite is suitable for local development but not ideal for large-scale concurrent workloads.
- Memory extraction depends on LLM output quality.
- Semantic retrieval requires suitable similarity thresholds.
- Deleted-memory matching can be improved with stronger semantic similarity checks.
- Authentication and authorization are not implemented.
- The current implementation is primarily designed for a local/single-user environment.
- LLM-generated memory extraction should be further validated before production deployment.

---

# 🚀 Future Improvements

Potential production improvements include:

- User authentication and authorization
- Multi-user support
- PostgreSQL for scalable structured storage
- pgvector or a managed vector database
- Structured JSON schema validation
- Memory confidence scoring
- Improved semantic duplicate detection
- Improved deleted-memory matching
- Encryption of sensitive user data
- API rate limiting
- Docker containerization
- Cloud deployment
- Automated unit and integration tests
- Logging and monitoring
- API versioning

---

# 🔑 Key Concepts Demonstrated

This project demonstrates practical implementation of:

- Large Language Models (LLMs)
- Prompt Engineering
- Persistent AI Memory
- Vector Databases
- Semantic Search
- Retrieval-Augmented Generation concepts
- Conversation Summarization
- Token Management
- REST APIs
- Flask Backend Development
- SQLite Database Management
- CRUD Operations
- Full-Stack Development
- Memory Conflict Resolution
- User-Controlled AI Memory
- Data Deletion and Tombstones

---

# 👩‍💻 Author

**Jeevia Harshini M**

AI & Data Science

GitHub: [@jeevia22](https://github.com/jeevia22)

---

## ⭐ Project Summary

The **AI Memory Assistant** combines:

```text
LLM
+
Persistent Memory
+
Semantic Retrieval
+
Conversation Summarization
+
User-Controlled Memory
```

to create a personalized conversational AI system where users can **see, modify, and control what the assistant remembers**.
```

**Before committing:** make sure `.env.example` contains only `GROQ_API_KEY=your_groq_api_key_here` and never your real `gsk_...` key. Also keep `.env`, `memory.db`, and `chroma_db/` excluded through `.gitignore`.
