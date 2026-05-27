from Database import get_connection
from datetime import date

class Message:
    def __init__(self, contenu, id_forum, id_utilisateur, datePublication=None):
        self.contenu = contenu
        self.id_forum = id_forum
        self.id_utilisateur = id_utilisateur
        self.datePublication = datePublication or date.today()

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Message (contenu, datePublication, id_forum, Id_utilisateur)
            VALUES (?, ?, ?, ?)
        """, (self.contenu, self.datePublication, self.id_forum, self.id_utilisateur))
        conn.commit()
        conn.close()

    @staticmethod
    def get_par_forum(id_forum):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Message WHERE id_forum = ? ORDER BY datePublication DESC", (id_forum,))
        rows = cur.fetchall()
        conn.close()
        return rows