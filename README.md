# MySocial – Social Media Platform

**MySocial** is a feature-rich, Instagram-like social media platform built with Django. Users can share photos, like and comment on posts, join group chats, search for friends, and communicate in real time.

---

## Features

### 🧑‍🤝‍🧑 User & Profile Management
- User registration and authentication
- Avatar option (users can add GIFs)
- Follow/unfollow users
- Search users by username

### 📷 Posts
- Upload images with captions
- Like/unlike posts
- Comment on posts
- Real-time like/comment count updates (AJAX)
- View detailed post modal/sidebar

### 💬 Real-Time Chat
- One-on-one messaging
- Group chats using WebSockets (Django Channels + Redis)
- Group admins can add/remove members
- Unread message notifications

### 🔔 Notifications
- Real-time notifications for:
  - Likes
  - Comments
  - Follows

### 🔍 Search
- Live user search by username

---

## 💻 Tech Stack

| Layer      | Technology                          |
|------------|--------------------------------------|
| Backend    | Django, Django REST Framework        |
| Real-Time  | Django Channels, Redis, WebSockets   |
| Frontend   | HTML, CSS, JavaScript (jQuery, AJAX) |
| Database   | SQLite (or PostgreSQL)               |
| Auth       | Django built-in authentication       |
| Media      | Django Media storage for images      |

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/mysocial.git
cd mysocial
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File (Optional)
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Run Development Server
```bash
python manage.py runserver
```

### 7. Run Daphne (WebSocket Server)
Make sure Redis is running.

```bash
daphne -b 127.0.0.1 -p 8002 social_media.asgi:application
```

---





---

