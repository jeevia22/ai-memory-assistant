# 🧠 AI Memory Assistant

An AI-powered full-stack chat assistant that remembers important facts about users across sessions and allows users to view, edit, and delete their stored memories.

The application combines an LLM, SQLite, and a vector database to provide persistent and controllable user memory.

---

## 🚀 Features

### 1. Persistent User Memory

The assistant automatically extracts lasting facts about the user from every conversation.

For example:

> "I prefer Python for programming."

The system extracts:

```text
Category: programming_language
Fact: The user prefers Python.