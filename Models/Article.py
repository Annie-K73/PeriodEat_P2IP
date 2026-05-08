from Database import get_connection
from datetime import date

class Article:
    def __init__(self, titre, description, id_forum, datePublication=None):
        self.titre = titre
        self.description = description
        self.id_forum = id_forum
        self.datePublication = datePublication or date.today()

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Article (titre, description, datePublication, id_forum)
            VALUES (?, ?, ?, ?)
        """, (self.titre, self.description, self.datePublication, self.id_forum))
        conn.commit()
        conn.close()

    @staticmethod
    def get_par_forum(id_forum):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Article WHERE id_forum = ?", (id_forum,))
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_tous():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Article")
        rows = cur.fetchall()
        conn.close()
        return rows