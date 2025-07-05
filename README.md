# Smart Support AI

**Smart Support AI** is an innovative, AI-driven customer support solution built to revolutionize query handling. By combining the power of **DistilBERT**, **Google Gemini**, and a sophisticated **multi-agent system** orchestrated through **LangGraph**, this project automates the entire support process—from categorizing queries to generating personalized responses—all in real time.

With a sleek, user-friendly web interface and a robust **FastAPI-powered backend**, Smart Support AI is designed for scalability, performance, and exceptional customer experiences.

---

## 🚀 Project Objectives

- **Automate Support Tasks:** Minimize manual effort using AI agents for query categorization, sentiment analysis, prioritization, answer retrieval, and response generation.
- **Boost Customer Satisfaction:** Deliver fast, accurate, and personalized replies to enhance user experience and reduce resolution times.
- **Scale Seamlessly:** Handle high query volumes with asynchronous processing and optimized workflows.
- **Ensure Dependability:** Incorporate robust error handling, logging, and fallback mechanisms for uninterrupted service.

---

## 🔑 Key Features

### 🧠 Multi-Agent System

A team of specialized AI agents collaborates to process incoming queries:

- **Categorizer Agent:** Classifies queries (e.g., Billing, Technical) using a fine-tuned DistilBERT model.
- **Sentiment Analyzer Agent:** Detects emotional tone (positive, negative, neutral).
- **Priority Agent:** Assigns urgency based on sentiment and category.
- **Knowledge Base Search Agent:** Retrieves relevant answers from a JSON-based knowledge base.
- **Response Agent:** Crafts context-aware replies using Google Gemini.
- **Escalation Agent:** Flags queries that need human attention.
- **Ticket Agent:** Generates unique support tickets for escalated cases.

### 🌐 Real-Time Web Interface
- Bootstrap-styled front-end for submitting queries and viewing responses instantly.

### ⚙️ Asynchronous Processing
- Efficiently handles multiple queries using async workflows.

### 📜 Robust Logging
- Daily-rotated logs and detailed error handling for high reliability.

### 🆔 Unique Ticket IDs
- Secure, collision-free ticket generation using UUIDs.

---

## 🛠️ Technologies Used

- **Python** — Core language
- **FastAPI** — High-performance backend API
- **LangGraph** — Agent orchestration framework
- **DistilBERT (Hugging Face)** — Query classification
- **Google Gemini** — Response generation
- **TensorFlow** — Model fine-tuning
- **aiofiles** — Asynchronous file handling
- **UUID** — Unique ticket generation
- **Bootstrap** — Frontend styling

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.9+
- Google Cloud Account (with Vertex AI API enabled for Gemini)
- Hugging Face Account (optional, for model access)

### 📦 Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/smart-support-ai.git
   cd smart-support-ai
