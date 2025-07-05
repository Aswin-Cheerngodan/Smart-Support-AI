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

- **Categorizer Agent:** Classifies queries (e.g., Billing, Order) using a fine-tuned DistilBERT model.
- **Sentiment Analyzer Agent:** Detects emotional tone (positive, negative, neutral).
- **Priority Agent:** Assigns urgency based on sentiment and category.
- **Knowledge Base Search Agent:** Retrieves relevant answers from a JSON-based knowledge base.
- **Response Agent:** Crafts context-aware replies using Google Gemini.
- **Escalation Agent:** Flags queries that need human attention.
- **Ticket Agent:** Generates unique support tickets for escalated cases.

### 🌐 Real-Time Web Interface
- Tailwind-CSS-styled front-end for submitting queries and viewing responses instantly.

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
- **Tailwind CSS** — Frontend styling

---

## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.12
- Google Cloud Account (API enabled for Gemini)

### 📦 Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aswin-Cheerngodan/Smart-Support-AI.git
   cd Smart-Support-AI
   ```
2. **Create .env file in the root**
   ```bash
   GOOGLE_API_KEY=your_google_api_key
   ```
   ### Run with Docker(Recommended)
   
   Build the Docker image
   ```bash
   docker build -t smart-support-ai .
   ```
   Run the Docker container
   ```bash
   docker run --env-file .env -p 8000:8000 smart-support-ai
   ```
   Access the app
   Open your browser and go to: http://localhost:8000
   
   ### Run Locally(without docker)
3. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
5. Run the Server
   ```bash
   python src/api/main.py
   ```
   Access the Interface
   Open your browser and go to: http://localhost:8000

## ▶️ Usage
- Submit a Query

   Example: "Why hasn’t my order shipped?"

- Monitor Activity

   Logs: Check logs/
   Tickets: View data/tickets.csv

## 📬 Contact
Questions or suggestions? Open an issue or contact me at aachu8966@gmail.com.


   
   
