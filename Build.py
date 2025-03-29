import sqlite3
import uuid
import getpass

def create_database():
    conn = sqlite3.connect('Database/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notes (
            user_id TEXT UNIQUE NOT NULL,
            notes_json TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id TEXT PRIMARY KEY UNIQUE NOT NULL,
            id_ent TEXT NOT NULL,
            password TEXT NOT NULL,
            moyenneG NUMERIC,
            notifs TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_user():
    conn = sqlite3.connect('Database/database.db')
    cursor = conn.cursor()
    user_id = str(uuid.uuid4())
    id_ent = input("Entrez votre identifiant ent (prénom.nom) : ")
    password = getpass.getpass("Entrez votre mot de passe : ")
    cursor.execute('''
        INSERT INTO Users (id, id_ent, password)
        VALUES (?, ?, ?)
    ''', (user_id, id_ent, password))
    conn.commit()
    conn.close()

    with open('Variables.py', 'w') as file:
        file.write(f'USER_ID = "{user_id}"\n')
        file.write('TOKEN = ""\n')

    print(f"Utilisateur créé avec succès ! Votre ID est : {user_id}")
    print("Votre ID est stocké dans Variables.py")

if __name__ == "__main__":
    create_database()
    print("Base de données et tables créées avec succès.")
    create_user()