# LITReview

A Django web application where users can create review requests (tickets), publish reviews, follow other users, and view a personalized feed.

---

# Features

* User authentication
* Follow / unfollow users
* Create tickets
* Create reviews
* Personalized feed (Flux)
* Upload images
* Edit & delete posts

---

# Project Structure

```text
LITReview/
│
├── authentification/
├── reviews/
├── tickets/
├── media/
├── static/
├── templates/
├── manage.py
└── db.sqlite3
```

---

# Installation

## 1. Clone the project

```bash
git clone <repository-url>
cd LITReview
```

---

## 2. Create virtual environment

### Windows

```bash
python -m venv env
env\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv env
source env/bin/activate
```

---

## 3. Install dependencies

```bash
pip install django pillow
```

---

## 4. Apply migrations

```bash
python manage.py migrate
```

---

## 5. Run server

```bash
python manage.py runserver
```

Open in browser:

```text
http://127.0.0.1:8000/
```

---

# Main Apps

## authentification

Handles:

* Login
* Signup
* Logout
* Follow system

---

## tickets

Handles:

* Ticket creation
* Ticket updates
* Feed system


---

## reviews

Handles:

* Review creation
* Ratings
* Review updates


---

## Database

SQLite database:

```text
db.sqlite3
```

---

## Media Files

Uploaded images are stored in:

```text
/media/
```

---

## Static Files

CSS and static assets:

```text
/static/
```

---
