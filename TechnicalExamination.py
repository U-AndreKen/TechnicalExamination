import requests
import sqlite3
from pydantic import BaseModel, EmailStr

class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str

# Connect to database and if not exists, create it
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Creating table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT,
    phone TEXT
)
""")

try:
    # Getting the users from API
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    users = response.json()

    # Save users to database
    for user in users:
        try:
            valid_user = UserModel(**user)
            cursor.execute(
                "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?)",
                (valid_user.id, valid_user.name, valid_user.username, 
                 valid_user.email, valid_user.phone)
            )
        except Exception as e:
            print(f"Error with user {user.get('id')}: {e}")

    conn.commit()
    print("Users saved to database")

except Exception as e:
    print(f"Error: {e}")

finally:
    conn.close()

    #Testing for commit