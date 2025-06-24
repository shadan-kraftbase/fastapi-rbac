# FastAPI RBAC Example

A simple FastAPI project implementing RBAC with JWT authentication.
Used Supabase as DB implementation

## How to run

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
2. Create a `.env` file in the project root with your configuration (example):
   ```env
   DATABASE_URL=your_database_url
   JWT_SECRET_KEY=your_jwt_secret
   JWT_REFRESH_SECRET_KEY=your_refresh_secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
