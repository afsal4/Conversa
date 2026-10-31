<div align="center">

# 🧭 Scholar Compass

**A safe-space platform for women to chat, connect, and find answers.**

![Hackathon](https://img.shields.io/badge/Women's_Day_Hackathon-Brototype-F953C6?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=flat-square&logo=django&logoColor=white)
![Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)

</div>

## 💜 About

Finding a place online where you can speak openly and feel respected isn't always easy. Scholar Compass is a project built to explore that idea: a platform where women can chat, share experiences, and support one another. An AI assistant sits alongside the chat and answers questions using trusted documents, so the answers come from real sources instead of guesses.

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 💬 | **Women's chat** | A space designed for women to talk, share stories, and support each other. |
| 🤖 | **AI assistant** | Answers questions in plain language using Google Gemini. |
| 📄 | **Chat with PDFs** | Upload a document and ask questions about what is inside it. |
| 🔎 | **Smart search** | Finds the most relevant passages by meaning, not just matching keywords. |
| 🔐 | **User accounts** | Sign up and log in so every member has their own space. |

## ⚙️ How It Works

1. **📄 Read:** documents are split into small pieces and stored as vectors in Pinecone or FAISS.
2. **🔎 Retrieve:** when you ask a question, the most relevant pieces are pulled up.
3. **🤖 Answer:** Gemini writes a reply based only on those pieces, so it stays grounded.

## 🛠️ Tech Stack

| Purpose | Tools |
|---|---|
| 🌐 Web app | Django, Gunicorn, WhiteNoise |
| 🧠 AI | Google Gemini, LangChain |
| 🗂️ Vector search | Pinecone, FAISS |
| 📑 Documents | pypdf, NLTK |

## 🚀 Getting Started

**You will need:** Python 3.10+, a [Gemini API key](https://aistudio.google.com/app/apikey), and a [Pinecone](https://www.pinecone.io/) account with an index.

```bash
git clone https://github.com/afsal4/Scholar_Compass.git
cd Scholar_Compass

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the project root:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local development |
| `GOOGLE_API_KEY` | Gemini API key |
| `PINECONE_API_KEY` | Pinecone API key |
| `PINECONE_INDEX_NAME` | Name of your Pinecone index |

Then start the app and open http://127.0.0.1:8000/

```bash
python manage.py migrate
python manage.py runserver
```

## 📁 Project Structure

```
Scholar_Compass/
├── home/                  # Main app: views, logic, chat
├── scholar_compass/       # Project settings
├── templates/             # HTML pages
├── data/                  # Source documents
├── tmp_pdf_vectorstore/   # Temporary stores for uploaded PDFs
└── manage.py
```

<div align="center">

Built with 💜 during the **Women's Day Hackathon** organized by **Brototype**.

</div>
