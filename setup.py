from utils.db import Db

from flask_bcrypt import check_password_hash
from flask_bcrypt import generate_password_hash

database = Db('database.db')

query = """
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL,
        teamID TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL
    )
"""

database.query(query, commit=True)



query = f"""
    INSERT INTO users (email, name, password, teamID, role) VALUES
    ('dattasoham805@gmail.com', 'Soham Datta', '{generate_password_hash("password").decode("utf-8")}', 'team_1', 'participant')
"""

database.query(query, commit=True)

# query = "DROP TABLE IF EXISTS users"

# database.query(query, commit=True)