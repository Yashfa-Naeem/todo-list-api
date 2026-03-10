#!/usr/bin/env python
"""Reset database - drops all tables and recreates them with new schema."""

from api.database.database import engine, Base
from api.database.schema import User, Task, TaskAttachment  # Import all models
import os
from dotenv import load_dotenv

load_dotenv()

def reset_db():
    """Drop all tables and recreate with current schema."""
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Tables dropped")
    
    print("🔨 Creating tables with updated schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
    print("\nNew User table columns:")
    print("  - reset_password_token")
    print("  - reset_password_expires")
    print("  - refresh_token")
    print("\nDatabase is ready to use!")

if __name__ == "__main__":
    reset_db()
