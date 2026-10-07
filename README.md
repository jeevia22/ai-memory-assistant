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
