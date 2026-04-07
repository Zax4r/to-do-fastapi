# To-Do FastAPI

A task manager built with FastAPI.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL
- **Cache**: Redis
- **Authentication**: JWT (cookies)
- **Containerization**: Docker Compose

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/registration/register/` | Register |
| POST | `/registration/login/` | Log in |
| POST | `/registration/logout/` | Log out |
| GET | `/users/` | List users |
| GET | `/users/{id}` | Get user by ID |
| POST | `/users/add/` | Add user |
| GET | `/tasks/` | Get current user's tasks |
| POST | `/tasks/add/` | Add task |
| PUT | `/tasks/update/{id}` | Update task |
| DELETE | `/tasks/delete/{id}` | Delete task |

## Running

```bash
docker compose build
docker compose up 
```

- Backend: `http://0.0.0.0:8000`
- Swagger UI: `http://0.0.0.0:8000/docs`

## Tests
Also, there are tests for this app.
Before running the tests, you have to disable the rate limiter middleware in the main file.
Also, you'll need to have Postgres installed on your device.

run this command in backend directory.
```bash
pytest tests/
```
