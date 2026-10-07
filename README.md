Absolutely — here is the **GitHub-ready `README.md` content** in Markdown code format. You can copy everything inside the code block directly into your `README.md`.

```markdown
# 🧠 AI Memory Assistant

An AI-powered conversational assistant with **persistent, user-specific long-term memory** across independent chat sessions.

Unlike a conventional chatbot that mainly relies on the current conversation, this application can identify important information from conversations, store it as long-term memory, retrieve relevant memories in future conversations, update outdated information, summarize long conversations, and give users control over what the system remembers.

---

## 🚀 Key Features

### 🔐 1. User Authentication

- User registration and login
- Secure password hashing using Werkzeug
- Flask session-based authentication
- Logout support
- Separate memory space for every user

### 💬 2. Multi-Session Chat

- Create multiple independent chat sessions
- Store messages for each session
- Reopen previous conversations
- Long-term memories are shared across sessions for the same user

### 🧠 3. Automatic Long-Term Memory

The system uses an LLM to identify information worth remembering from conversations.

For example:

> "My preferred programming language is Python."

The system can create:

```text
Category: PROGRAMMING_LANGUAGE
Fact: User prefers Python
Importance: 8/10
```

This memory can then be retrieved in future conversations.

---

### 🔄 4. ADD / UPDATE / IGNORE Memory

The memory system can decide whether to:

- **ADD** a new memory
- **UPDATE** an existing memory
- **IGNORE** information that does not need to be stored

Example:

```text
Previous Memory:
PROGRAMMING_LANGUAGE → Python

User:
"I now prefer Java."

Updated Memory:
PROGRAMMING_LANGUAGE → Java
```

The latest corrected value becomes the authoritative memory.

---

### ⭐ 5. Memory Importance Scoring

Every memory receives an importance score from **1–10**.

Example:

```text
User likes blue
→ Importance: 3/10

User prefers Java
→ Importance: 8/10

User's long-term career goal
→ Importance: 10/10
```

The importance score is also used for memory retention.

---

### ⏳ 6. Memory Expiration

The application uses importance to determine how long a memory should remain active.

```text
Importance 1–3   → Short retention
Importance 4–5   → Medium retention
Importance 6–7   → Long retention
Importance 8–10  → Permanent
```

Expired memories are automatically removed from active storage.

---

### 🔎 7. Semantic Memory Retrieval

ChromaDB is used as the semantic retrieval layer.

This allows the system to retrieve memories based on **meaning**, rather than requiring an exact keyword match.

For example, stored memory:

```text
User prefers Java.
```

can be relevant to:

```text
"What programming language am I most comfortable with?"
```

---

### 🗄️ 8. SQLite as the Source of Truth

SQLite stores structured application data including:

- Users
- Chat sessions
- Messages
- Memories
- Conversation summaries
- Deleted-memory records
- Server-run information

SQLite acts as the **authoritative source of the current memory state**.

ChromaDB is primarily used for semantic retrieval.

---

### ⚡ 9. Memory Conflict Resolution

The application handles outdated or conflicting information.

Example:

```text
Old conversation:
"I prefer Python."

Current Memory:
PROGRAMMING_LANGUAGE → Java
```

If the user asks:

```text
"What programming language do I prefer?"
```

the current memory is treated as authoritative.

Therefore:

```text
Old information → Python
Current memory  → Java
                       ↓
                   Answer: Java
```

This prevents stale conversation history from overriding an updated memory.

---

### ✏️ 10. User-Controlled Memory

Users can manage their memories through the memory panel.

Available operations:

- View memories
- Edit memories
- Delete memories
- View importance
- View expiration information

Example:

```text
🧠 My Memories

PROGRAMMING_LANGUAGE

User prefers Java

⭐ Importance: 8/10
♾️ Permanent memory

[ Edit ] [ Delete ]
```

---

### 🗑️ 11. Deleted-Memory Protection

When a user explicitly deletes a memory, the application records the deletion.

This helps prevent the same deleted information from immediately being recreated as an active memory.

---

### 📝 12. Long-Conversation Summarization

The application uses `tiktoken` to monitor conversation size.

When the configured token threshold is exceeded:

```text
Older Messages
      ↓
Token Threshold Exceeded
      ↓
LLM Summarization
      ↓
Important Information Preserved
      ↓
Summary Stored
      ↓
Recent Messages Retained
```

The summary preserves important:

- Decisions
- User goals
- Context
- Unresolved tasks
- Preferences

This reduces context size while preserving important information.

---

### 💾 13. Persistent Storage

The application uses disk-backed:

```text
SQLite
+
ChromaDB
```

Therefore memories survive a Flask server restart.

The application also provides a:

```text
Verify Persistence
```

feature to demonstrate that stored memories remain available after restarting the server.

---

# 🏗️ System Architecture

```text
                         USER
                           │
                           ▼
                  LOGIN / REGISTER
                           │
                           ▼
                    AUTHENTICATION
                           │
                           ▼
                     CHAT SESSION
                           │
                           ▼
                    USER MESSAGE
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Save Conversation          Memory Extraction
                                      │
                                ADD / UPDATE / IGNORE
                                      │
                                      ▼
                              Importance + Expiry
                                      │
                                      ▼
                               ┌─────────────┐
                               │   SQLite    │
                               │ Source of   │
                               │   Truth     │
                               └──────┬──────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │  ChromaDB   │
                               │  Semantic   │
                               │  Retrieval  │
                               └──────┬──────┘
                                      │
                                      ▼
                              RELEVANT MEMORY
                                      │
                                      ▼
                           CONTEXT ASSEMBLY
                                      │
                 ┌────────────────────┼─────────────────┐
                 │                    │                 │
                 ▼                    ▼                 ▼
            Long-Term            Summary          Recent Chat
             Memory
                 │                    │                 │
                 └────────────────────┼─────────────────┘
                                      │
                                      ▼
                                  GROQ LLM
                                      │
                                      ▼
                                 AI RESPONSE
                                      │
                                      ▼
                              Save Response
                                      │
                                      ▼
                              Token Monitoring
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                     Below Limit              Above Limit
                         │                         │
                         │                         ▼
                         │                    Summarization
                         │                         │
                         │                         ▼
                         │                   Store Summary
                         │
                         └─────────────┬───────────┘
                                       ▼
                                  NEXT MESSAGE
```

---

# 🔄 Complete Memory Workflow

## New Memory

```text
User Message
     ↓
LLM Memory Extraction
     ↓
ADD
     ↓
SQLite
     ↓
ChromaDB Synchronization
```

## Updated Memory

```text
Existing Memory
     ↓
User Provides Correction
     ↓
LLM Identifies UPDATE
     ↓
SQLite Updated
     ↓
Conflicting Old Value Removed
     ↓
ChromaDB Synchronized
     ↓
New Value Becomes Authoritative
```

## Memory Query

```text
User Question
     ↓
Detect Memory Query
     ↓
Identify Category
     ↓
Retrieve Current Memory from SQLite
     ↓
Ignore Stale Conflicting Information
     ↓
Groq LLM
     ↓
Final Answer
```

---

# 🧩 Context Construction

For a normal chat request, the LLM receives:

```text
System Instructions
        +
Relevant Long-Term Memories
        +
Conversation Summary
        +
Recent Conversation
        +
Current User Message
```

Conceptually:

```text
┌─────────────────────────────┐
│ System Instructions         │
├─────────────────────────────┤
│ Long-Term Memory            │
├─────────────────────────────┤
│ Conversation Summary        │
├─────────────────────────────┤
│ Recent Conversation         │
├─────────────────────────────┤
│ Current User Question       │
└──────────────┬──────────────┘
               ↓
             Groq
               ↓
          AI Response
```

For direct memory questions, the current authoritative memory takes priority over stale conversation history.

---

# 📝 Conversation Summarization Workflow

The application monitors token usage using `tiktoken`.

```text
Conversation
      ↓
Token Counting
      ↓
Is Threshold Exceeded?
      │
   ┌──┴──┐
   │     │
  NO    YES
   │     │
   │     ▼
   │  Summarize
   │  Older Messages
   │     │
   │     ▼
   │  Store Summary
   │     │
   │     ▼
   │  Keep Recent
   │  Messages
   │
   └───────────────→ Continue
```

The purpose is to prevent excessively large prompts while preserving important conversation context.

---

# 👥 Multi-User Memory Isolation

Each authenticated user has an independent memory space.

```text
User A
 ├── Chat Sessions
 └── Memories

User B
 ├── Chat Sessions
 └── Memories
```

Memory retrieval is restricted using the authenticated user's ID.

Therefore:

```text
User A's memories
        ≠
User B's memories
```

This prevents one user from retrieving another user's information.

---

# 🗄️ Data Storage Architecture

## SQLite

SQLite acts as the structured source of truth.

Conceptually:

```text
users
sessions
messages
memories
summaries
deleted_memories
server_runs
```

## ChromaDB

ChromaDB stores the semantic representation of memories and supports similarity-based retrieval.

Each memory is associated with a user so retrieval can be isolated per user.

---

# 💻 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | User interface |
| Backend | Flask | Web server and REST APIs |
| LLM API | Groq | AI response generation and memory processing |
| LLM | `openai/gpt-oss-120b` | Language model |
| Vector Database | ChromaDB | Semantic memory retrieval |
| Database | SQLite | Structured persistent storage |
| Tokenization | tiktoken | Token counting |
| Authentication | Flask Session + Werkzeug | Authentication and password hashing |
| Configuration | python-dotenv | Environment variables |

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
├── memory.db
│
└── chroma_db/
```

### Files that should NOT be committed

```text
.env
memory.db
chroma_db/
__pycache__/
```

The `.env` file contains secrets and API keys.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-memory-assistant
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
FLASK_SECRET_KEY=your_secret_key
```

Never commit the real `.env` file to GitHub.

Use `.env.example` for sharing the required configuration format:

```env
GROQ_API_KEY=your_groq_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

---

# ▶️ Run the Application

Start the Flask server:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

# 🧪 Demo Workflow

The following sequence demonstrates the major features of the application.

## 1. Register / Login

Create an account and login.

---

## 2. Create a Memory

Send:

```text
My preferred programming language is Python.
```

The system should extract and display a memory similar to:

```text
PROGRAMMING_LANGUAGE
User prefers Python
```

---

## 3. Update the Memory

Edit the memory:

```text
PROGRAMMING_LANGUAGE → Java
```

Then ask:

```text
What programming language do I prefer?
```

Expected:

```text
Your preferred programming language is Java.
```

This demonstrates:

- Memory editing
- Memory conflict resolution
- SQLite as source of truth
- Protection against stale conversation history

---

## 4. Demonstrate Cross-Session Memory

Create a new chat.

Ask:

```text
What programming language do I prefer?
```

The system can retrieve the long-term memory even though the question is being asked in a different chat session.

---

## 5. Demonstrate User Isolation

Logout and create another user.

Verify that the new user cannot see the previous user's memories.

---

## 6. Demonstrate Summarization

Generate a sufficiently long conversation to exceed the configured token threshold.

The application automatically:

```text
Detects token threshold
        ↓
Summarizes older messages
        ↓
Stores summary
        ↓
Retains recent messages
```

The generated summary is displayed in the conversation summary section.

---

## 7. Demonstrate Persistence

Click:

```text
Verify Persistence
```

Then:

```text
Stop Flask
Restart Flask
Login again
```

Verify that the previously stored memories are still available.

---

# 🎯 Problem Statement

Traditional conversational AI systems often have limited persistence across independent conversations.

Important user preferences, goals, and context can be lost when a conversation ends.

This project addresses that problem by creating an AI assistant capable of:

- Persisting important user information
- Retrieving relevant memories across conversations
- Updating outdated memories
- Managing memory importance and expiration
- Allowing users to edit and delete memories
- Summarizing long conversations
- Maintaining isolated memory for different users
- Persisting memory across server restarts

---

# 💡 Key Design Decisions

### Why SQLite?

SQLite provides persistent relational storage for structured application data and acts as the authoritative source for the current memory state.

### Why ChromaDB?

ChromaDB provides semantic retrieval, allowing the application to find relevant memories based on meaning rather than exact text matching.

### Why Both SQLite and ChromaDB?

They have different responsibilities:

```text
SQLite
→ What is the current truth?

ChromaDB
→ Which memories are semantically relevant?
```

### Why Groq?

Groq provides the LLM inference layer used for:

- Conversational responses
- Memory extraction
- Memory classification
- Importance assessment
- Conversation summarization

### Why Token Counting?

Token counting allows the application to detect when a conversation is becoming too large and trigger summarization before the context becomes impractical.

---

# 🔐 Security Considerations

- Passwords are hashed before storage.
- Authentication is handled using Flask sessions.
- Protected APIs require authentication.
- Memories are associated with user IDs.
- ChromaDB retrieval is filtered by user.
- API keys are stored in environment variables.
- Secrets are not included in frontend code.
- `.env` should never be committed to GitHub.

---

# 🚧 Current Limitations

This project is currently designed as a functional prototype/demo.

For production deployment, the following improvements could be considered:

- PostgreSQL instead of SQLite for higher concurrency
- Production-grade vector database for large-scale deployments
- Redis for caching and session management
- Background workers for memory extraction and summarization
- More sophisticated contradiction detection
- Stronger authorization and security controls
- Rate limiting
- Automated testing
- Production WSGI server
- Containerized deployment
- Monitoring and logging
- Cloud deployment

---

# 🔮 Future Improvements

Possible future enhancements include:

- Memory confidence scores
- Memory history/versioning
- Memory audit logs
- More advanced contradiction detection
- Hybrid keyword + semantic retrieval
- Reranking retrieved memories
- Background memory processing
- Production cloud deployment
- PostgreSQL + production vector database
- Streaming LLM responses
- User-configurable memory policies
- Advanced observability and analytics

---

# 🏆 Project Highlights

```text
✅ Multi-user authentication
✅ User-specific persistent memory
✅ Cross-session memory
✅ Automatic memory extraction
✅ ADD / UPDATE / IGNORE memory actions
✅ Memory importance scoring
✅ Memory expiration
✅ Semantic retrieval with ChromaDB
✅ SQLite as source of truth
✅ Memory conflict resolution
✅ Memory editing
✅ Memory deletion
✅ Deleted-memory protection
✅ Long-conversation summarization
✅ Token-aware context management
✅ Server-restart persistence
✅ User memory isolation
```

---

# 📌 One-Line Description

> **An AI conversational assistant with persistent, user-specific, editable long-term memory, semantic retrieval, memory lifecycle management, conflict resolution, and automatic long-conversation summarization.**

---

## 👩‍💻 Author

**Jeevia Harshini M**

AI & Data Science | Machine Learning | NLP | Generative AI | Python
```

**For GitHub:** copy the entire block into your `README.md`. You can then commit it with:

```bash
git add README.md
git commit -m "Update README"
git push
```
