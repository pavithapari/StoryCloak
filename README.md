

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

> **My very first project as a beginner!** 🎉  
> StoryCloak is a simple Flask web app that lets you create, store, and manage your personal stories and notes securely.
---

## 🚀 Live Demo
You can try the app here: [StoryCloak on Render](https://storycloak.onrender.com/)


## 📖 About the Project

StoryCloak is built with **Flask** as the backend and uses **Bootstrap** for styling.  
It supports **user authentication**, **note management**, and a clean UI for a smooth writing experience.  
The aim was to learn the basics of backend development, databases, and authentication — and I had fun building it!

---

## 🚀 Features

- 📝 **Create & Manage Stories** – Add, edit, and delete your personal stories.
- 🔐 **User Authentication** – Sign up, log in, and manage your account.
- 🎨 **Clean UI** – Responsive and mobile-friendly design using Bootstrap.

- 📂 **Database Support** – Store data securely using SQLAlchemy.

---

## 🛠️ Tech Stack
- **Backend:** Flask, SQLAlchemy ORM
- **Database:** PostgreSQL (via Render)
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Flask-Login, Bcrypt
- **Others:** WTForms, Flask-WTF, Flask-Mail, flask-migrate
- **Deployment** Render (Free Trail)

---

## 🖥️ Run Locally

Follow these steps to run StoryCloak on your local machine:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/storycloak.git
   cd storycloak


2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   * **Windows**:

     ```bash
     venv\Scripts\activate
     ```
   * **Mac/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables**

   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```

   *(On Windows use `set` instead of `export`)*

6. **Set up the database**

Run the following commands to set up and apply migrations:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```


7. **Run the application**

   ```bash
   flask run
   ```

8. **Visit in browser**
   Open [http://localhost:5000](http://localhost:5000) 🚀

---


## 🤝 Contributing

Since this is my first project, I’d love feedback! Feel free to fork the repo, make changes, and submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License** – you’re free to use, modify, and distribute it.

---

⭐ **If you like this project, please give it a star!** ⭐

