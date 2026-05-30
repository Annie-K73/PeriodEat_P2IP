from Database import get_connection
from datetime import date

class Vendre:
    
    def __init__(self,id_user,id_ingredient):
        self.id_utilisateur = id_user
        self.id_ingredient = id_ingredient

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Vendre (id_utilisateur, id_ingredient)
            VALUES (?, ?)
        """, (self.id_utilisateur, self.id_ingredient))
        conn.commit()
        conn.close()


    @staticmethod
    def supprimer(id_utilisateur, id_ingredient):
        """Supprime une association entreprise/ingrédient de la table Vendre."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM vendre WHERE id_utilisateur = ? AND id_ingredient = ?
        """, (id_utilisateur, id_ingredient))
        conn.commit()
        conn.close()

    @staticmethod
    def get_tous_par_id_vendeur(id_user):
        """Retourne toutes les produits vendus par un professionnel"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Vendre WHERE id_utilisateur = ? ",(id_user,))
        rows = cur.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def get_vendeurs_par_ingredient(id_ingredient):
        """Retourne tous les professionnels vendant un ingrédient donné."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Vendre WHERE id_ingredient = ?
        """, (id_ingredient,))
        rows = cur.fetchall()
        conn.close()
        return rows