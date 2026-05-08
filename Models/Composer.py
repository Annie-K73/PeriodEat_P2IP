from Database import get_connection

class Composer:

    def __init__(self, id_plat, id_ingredient):
        self.id_plat = id_plat
        self.id_ingredient = id_ingredient

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Composer (id_plat, id_ingredient)
            VALUES (?, ?)
        """, (self.id_plat, self.id_ingredient))
        conn.commit()
        conn.close()


    @staticmethod
    def supprimer(id_plat, id_ingredient):
        """Supprime une association plat/ingrédient de la table Composer."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Composer WHERE id_plat = ? AND id_ingredient = ?
        """, (id_plat, id_ingredient))
        conn.commit()
        conn.close()

