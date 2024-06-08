# Social Network API

This is a social networking application API built with Django Rest Framework.

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/social-network-api.git
   cd social-network-api
   ```

2. Build and start the Docker containers:
    ```bash
   docker-compose up --build
   ```

3. Apply database migrations:
    ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

4. Create a superuser:
    ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. Access the API at `http://localhost:8000`


### Endpoints
* `POST /signup/` - User signup
* `POST /login/` - User login
* `GET /search/?q=keyword` - Search users by email or name
* `POST /friend-request/send/` - Send friend request
* `POST /friend-request/manage/` - Accept/Reject friend request
* `GET /friends/` - List friends
* `GET /friend-requests/pending/` - List pending friend requests
