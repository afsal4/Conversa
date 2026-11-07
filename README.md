<div align="center">

# 💬 Conversa

**A simple chat platform to talk, connect, and stay in touch.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

</div>

## 💜 About

Having a clean, easy place to talk with other people online shouldn't be complicated. Conversa is a project built around that idea: a web platform where members can sign up, join conversations, and chat with each other. Everything is stored in a simple local database, so the app is easy to run and easy to understand.

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 💬 | **Chat** | A space for members to talk and share messages. |
| 🔐 | **User accounts** | Sign up and log in so every member has their own space. |
| 🗂️ | **Saved messages** | Conversations are stored in the database so nothing gets lost. |
| 🖥️ | **Simple pages** | Clean HTML templates that are easy to read and customize. |

## ⚙️ How It Works

1. **🔐 Join:** members create an account and log in.
2. **💬 Chat:** messages are sent through the chat page.
3. **🗂️ Save:** every message is stored in the database for later.

## 🛠️ Tech Stack

| Purpose | Tools |
|---|---|
| 🌐 Web app | Django |
| 🗄️ Database | SQLite |
| 🎨 Pages | HTML templates |

## 🚀 Getting Started

**You will need:** Python 3.10+ and pip.

```bash
git clone https://github.com/afsal4/Conversa.git
cd Conversa

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install django
```

Then set up the database, start the app, and open http://127.0.0.1:8000/

```bash
python manage.py migrate
python manage.py runserver
```

## 📁 Project Structure

```
Conversa/
├── home/                  # Main app: views, logic, chat
├── conversa/              # Project settings
├── templates/             # HTML pages
├── db.sqlite3             # Local database
└── manage.py
```

<div align="center">

Built with 💜 using **Django**.

</div>
