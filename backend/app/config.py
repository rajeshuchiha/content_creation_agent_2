import os

def get_database_url():
    
    database_url = os.environ.get("DATABASE_URL")
    
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+asyncpg://",
            1
        )
    
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
            1
        )
        
    return database_url

DB_URL = get_database_url()

allowed_origins_env = os.environ.get("ALLOWED_ORIGINS")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(',') if origin.strip()]