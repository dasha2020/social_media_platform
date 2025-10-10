# MySocial – Social Media Platform

**MySocial** is an Instagram-like social media platform with a lot of features built with Django. Users can share photos, like and comment on posts, join group chats, search for friends, and communicate in real time.

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
- View detailed post 

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
- User search by username

---


## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/mysocial.git(https://github.com/dasha2020/social_media_platform.git)
cd social_media_platform
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Run Development Server
```bash
python manage.py runserver
```

### 6. Run Daphne (WebSocket Server)
Make sure Redis is running.

```bash
daphne -b 127.0.0.1 -p 8002 social_media.asgi:application
```


