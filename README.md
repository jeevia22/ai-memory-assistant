🧠 AI Memory Assistant
An AI-powered conversational assistant that provides persistent, user-specific long-term memory across independent chat sessions.
Unlike a conventional chatbot that mainly relies on the current conversation, this application can identify important facts from user conversations, store them as memories, retrieve relevant memories in future conversations, update outdated information, summarize long conversations, and give users control over what the system remembers.
🚀 Key Features
1. User Authentication
- User registration and login
- Secure password hashing using Werkzeug
- Flask session-based authentication
- Logout support
- Separate memory space for every user
2. Multi-Session Chat
- Create multiple independent chat sessions
- Store messages for each session
- Reopen previous conversations
- Long-term memories are shared across sessions for the same user
3. Automatic Long-Term Memory
The system uses the LLM to identify information worth remembering from conversations.
Example:
"My preferred programming language is Python."

The system can create:
Category: PROGRAMMING_LANGUAGE
Fact: User prefers Python
Importance: 8/10
4. Memory Actions: ADD / UPDATE / IGNORE
The memory extraction system can decide whether to:
- ADD a new memory
- UPDATE an existing memory
- IGNORE information that is not useful as long-term memory
Example:
Previous:
PROGRAMMING_LANGUAGE → Python

User correction:
"I now prefer Java."

Result:
PROGRAMMING_LANGUAGE → Java
The latest corrected value becomes authoritative.
5. Memory Importance and Expiration
Every memory receives an importance score from 1–10.
The application uses importance to determine memory retention.
1–3   → short retention
4–5   → medium retention
6–7   → long retention
8–10  → permanent
Expired memories are removed from the active memory stores.
6. Semantic Memory Retrieval
ChromaDB is used as the semantic retrieval layer.
This allows the application to retrieve memories based on meaning rather than exact keyword matching.
For example, a stored memory:
User prefers Java.
can be relevant to:
"What programming language am I most comfortable with?"
7. SQLite as Source of Truth
SQLite stores structured application data including:
- Users
- Chat sessions
- Messages
- Memories
- Conversation summaries
- Deleted-memory records
- Server-run information
SQLite is treated as the authoritative source of the current memory state.
ChromaDB is used primarily for semantic retrieval.
8. Memory Conflict Resolution
The application handles outdated memories.
For example:
Old conversation:
"I prefer Python."

Current memory:
PROGRAMMING_LANGUAGE → Java
For a memory query such as:
"What programming language do I prefer?"
the current memory is treated as authoritative rather than allowing stale conversation history to override it.
9. User-Controlled Memory
The memory panel allows users to:
- View memories
- Edit memories
- Delete memories
- View importance
- View expiration information
10. Deleted-Memory Protection
When a user explicitly deletes a memory, the application records the deletion so that the deleted information is not immediately recreated as an active memory.
11. Long-Conversation Summarization
The application monitors conversation size using tiktoken.
When the configured token threshold is exceeded:
Older messages
      ↓
LLM summarization
      ↓
Important information retained
      ↓
Summary stored
      ↓
Recent messages retained
The summary preserves important:
- Decisions
- Goals
- Context
- Unresolved tasks
- Preferences
This reduces prompt size while preserving important conversation context.
12. Persistent Storage
Memories persist after restarting Flask because the application uses disk-backed:
SQLite
+
ChromaDB
The UI includes a Verify Persistence feature to demonstrate that stored memories survive a server restart.
🏗️ System Architecture
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
       Save conversation          Memory Extraction
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
            Long-term            Summary          Recent Chat
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
                     Below limit              Above limit
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
🔄 Memory Workflow
New Memory
User message
     ↓
LLM memory extraction
     ↓
ADD
     ↓
SQLite
     ↓
ChromaDB synchronization
Updated Memory
Existing memory
     ↓
User provides correction
     ↓
LLM identifies UPDATE
     ↓
SQLite updated
     ↓
Conflicting old value removed
     ↓
ChromaDB synchronized
     ↓
New value becomes authoritative
Memory Query
User question
     ↓
Is this a memory-related query?
     ↓
YES
     ↓
Find authoritative memory
     ↓
SQLite current value
     ↓
Ignore stale conflicting conversation information
     ↓
Groq LLM
     ↓
Answer
🗄️ Data Storage
SQLite
SQLite acts as the structured source of truth.
Conceptually, the database contains:
users
sessions
messages
memories
summaries
deleted_memories
server_runs
ChromaDB
ChromaDB stores the semantic representation of memories and supports similarity-based retrieval.
Memory records are associated with a user_id so that users cannot retrieve another user's memories.
🔐 User Isolation
Every authenticated user has a separate memory space.
User A
 ├── Sessions
 └── Memories

User B
 ├── Sessions
 └── Memories
Memory retrieval is restricted to the authenticated user's ID.
This prevents one user from receiving another user's stored memories.
🧩 Context Construction
For a normal chat request, the model receives a combination of:
System Instructions
        +
Relevant Long-Term Memories
        +
Conversation Summary
        +
Recent Conversation
        +
Current User Message
For direct memory questions, the current authoritative memory takes priority over stale conversation history.
📝 Conversation Summarization
The application uses tiktoken to monitor conversation token usage.
When the configured threshold is exceeded, older messages are summarized.
Large conversation
       ↓
Token counting
       ↓
Threshold exceeded
       ↓
Summarize older messages
       ↓
Store summary
       ↓
Keep recent messages
       ↓
Use summary + recent messages
The goal is to reduce context size while retaining the important information from the earlier conversation.
💻 Technology Stack
Component	Technology	Purpose
Frontend	HTML, CSS, JavaScript	User interface
Backend	Flask	Web server and APIs
LLM	Groq	AI response generation and memory processing
Model	openai/gpt-oss-120b	Language model
Vector Database	ChromaDB	Semantic memory retrieval
Database	SQLite	Structured persistent storage
Tokenization	tiktoken	Token counting
Authentication	Flask Session + Werkzeug	Authentication and password hashing
Configuration	python-dotenv	Environment variables


📁 Project Structure
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
Important
The following files/directories contain local runtime data and should not be committed to GitHub:
.env
memory.db
chroma_db/
__pycache__/
⚙️ Installation
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-memory-assistant
2. Create a virtual environment
Windows
python -m venv venv
venv\Scripts\activate
Linux / macOS
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables
Create a .env file:
GROQ_API_KEY=your_groq_api_key
FLASK_SECRET_KEY=your_secret_key
Never commit your real .env file or API key to GitHub.
A safe .env.example should contain placeholders:
GROQ_API_KEY=your_groq_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
▶️ Run the Application
python app.py
Open:
http://127.0.0.1:5000
🧪 Recommended Demo
The following sequence demonstrates the major features.
1. Register / Login
Create a user account and login.
2. Create a Memory
Send:
My preferred programming language is Python.
Show the memory appearing in My Memories.
3. Update the Memory
Edit the memory:
PROGRAMMING_LANGUAGE → Java
Then ask:
What programming language do I prefer?
The assistant should answer:
Java
This demonstrates memory correction and conflict resolution.
4. Cross-Session Memory
Create a new chat and ask about the preference again.
The assistant can retrieve the long-term memory even though the question is being asked in a different chat session.
5. User Isolation
Create/login as another user and verify that the first user's memories are not visible.
6. Summarization
Generate a sufficiently long conversation to exceed the configured token threshold.
Show:
Conversation Summary
and explain that older messages are summarized while recent context is retained.
7. Persistence
Click:
Verify Persistence
Then:
Stop Flask
Restart Flask
Login again
Verify that the memories are still available.
🎯 Problem Statement
Traditional conversational AI systems often have limited persistence across independent conversations. Important user preferences, goals, and context can be lost when a conversation ends.
This project addresses that problem by creating an AI assistant capable of:
- Persisting important user information
- Retrieving relevant memories across conversations
- Updating outdated memories
- Managing memory importance and expiration
- Allowing users to edit and delete memories
- Summarizing long conversations
- Maintaining isolated memory for different users
- Persisting memory across server restarts
💡 Key Design Decisions
Why SQLite?
SQLite provides a simple persistent relational database for structured application data and acts as the authoritative source for the current state of memories.
Why ChromaDB?
ChromaDB provides semantic retrieval, allowing the application to find memories based on meaning rather than only exact text matching.
Why both SQLite and ChromaDB?
They serve different purposes:
SQLite
→ What is the current truth?

ChromaDB
→ Which memories are semantically relevant?
Why an LLM?
The LLM is used for:
- Conversational responses
- Memory extraction
- Memory classification
- Importance assessment
- Conversation summarization
Why token counting?
Token counting allows the application to detect when a conversation is becoming too large and trigger summarization before context size becomes a problem.
🔒 Security Considerations
- Passwords are hashed before storage.
- Authentication is handled through Flask sessions.
- API endpoints require authentication where appropriate.
- Memories are associated with user IDs.
- ChromaDB retrieval is filtered by user.
- API keys are stored in environment variables.
- Secrets are not included in frontend code.
- .env should never be committed to source control.
🚧 Current Limitations
This project is designed as a functional prototype/demo. For production deployment, the following improvements could be considered:
- PostgreSQL instead of SQLite for higher concurrency
- A production-grade vector database for larger-scale deployments
- Redis for caching and session management
- Background workers for memory extraction and summarization
- More sophisticated memory conflict resolution
- Stronger authorization and security controls
- Rate limiting
- API monitoring and logging
- Automated tests
- Production WSGI server
- Containerized deployment
- More granular memory categories and lifecycle policies
🔮 Future Improvements
Possible future extensions include:
- User-configurable memory settings
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
- Observability and analytics
🏆 Project Highlights
The key capabilities demonstrated by this project are:
✅ Multi-user authentication
✅ User-specific persistent memory
✅ Cross-session memory
✅ Automatic memory extraction
✅ ADD / UPDATE / IGNORE memory actions
✅ Memory importance scoring
✅ Memory expiration
✅ Semantic retrieval with ChromaDB
✅ SQLite source of truth
✅ Memory editing
✅ Memory deletion
✅ Deleted-memory protection
✅ Long-conversation summarization
✅ Token-aware context management
✅ Server-restart persistence
✅ Memory isolation between users
📌 One-Line Description
An AI conversational assistant with persistent, user-specific, editable long-term memory, semantic retrieval, memory lifecycle management, and automatic long-conversation summarization.
