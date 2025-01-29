# Network

## Overview
Network is a Twitter-like social media web application that allows users to create posts, follow other users, like posts, and engage in discussions. The project is built using Django for the backend and JavaScript for dynamic interactions on the frontend.

## Features
- User authentication (login, logout, registration)
- Create, edit, and delete posts
- Follow and unfollow users
- View posts from followed users in a personalized feed
- Like and unlike posts
- Pagination for browsing posts efficiently
- Interactive user interface with JavaScript

## Technologies Used
- **Backend:** Django, Python, SQLite
- **Frontend:** JavaScript, HTML, CSS, Bootstrap
- **Authentication:** Django's built-in authentication system
- **Data Fetching:** Django ORM and Fetch API

## Installation & Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/NoName3755/Network.git
   cd network
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply database migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
7. **Access the application:**
   Open `http://127.0.0.1:8000/` in your browser.

## Usage
- Register and log in to create and interact with posts.
- Follow other users to see their posts in your feed.
- Like and unlike posts to engage with content.
- Edit or delete your own posts as needed.
- Browse different pages with seamless pagination.

## Future Improvements
- Implement real-time notifications for likes and follows.
- Enhance UI with a more modern and responsive design.
- Add comment functionality to posts.
- Improve search and filtering for better content discovery.

## License
This project is part of CS50W and follows the course guidelines. Feel free to modify and improve it.

## Acknowledgments
- CS50W by Harvard University for providing the foundational knowledge.
- Django documentation for backend development guidance.
