from Database import get_connection
from datetime import date

class Avis:
    def __init__(self, commentaire, note, id_forum, id_plat, id_utilisateur, datePublication=None):
        self.commentaire = commentaire
        self.note = note  # 1 à 5
        self.id_forum = id_forum
        self.id_plat = id_plat
        self.id_utilisateur = id_utilisateur
        self.datePublication = datePublication or date.today()

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Avis
            (commentaire, note, datePublication, id_forum, id_plat, Id_utilisateur)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.commentaire, self.note, self.datePublication,
              self.id_forum, self.id_plat, self.id_utilisateur))
        conn.commit()
        conn.close()

    @staticmethod
    def get_par_plat(id_plat):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Avis WHERE id_plat = ?", (id_plat,))
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_par_forum(id_forum):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Avis WHERE id_forum = ?", (id_forum,))
        rows = cur.fetchall()
        conn.close()
        return rows