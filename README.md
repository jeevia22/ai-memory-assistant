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
