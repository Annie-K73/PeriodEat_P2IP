from Database import get_connection
import pandas as pd

class Ingredient:
    def __init__(self, nom, estSaisonnier, saison, scoreMenstruelle,
                 scoreFolliculaire, scoreOvulation, scoreLuteale):
        self.nom = nom
        self.estSaisonnier = estSaisonnier
        self.saison = saison  # 'printemps','ete','automne','hiver','toute saison'
        self.scoreMenstruelle = scoreMenstruelle
        self.scoreFolliculaire = scoreFolliculaire
        self.scoreOvulation = scoreOvulation
        self.scoreLuteale = scoreLuteale

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Ingredient
            (nom, estSaisonnier, saison, scoreMenstruelle, scoreFolliculaire,
             scoreOvulation, scoreLuteale)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.nom, self.estSaisonnier, self.saison, self.scoreMenstruelle,
              self.scoreFolliculaire, self.scoreOvulation, self.scoreLuteale))
        conn.commit()
        conn.close()

    @staticmethod
    def get_par_plat(id_plat):
        """Retourne les ingrédients d'un plat via la table Composer."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT i.* FROM Ingredient i
            JOIN Composer c ON i.id_ingredient = c.id_ingredient
            WHERE c.id_plat = ?
        """, (id_plat,))
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_tous():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Ingredient")
        rows = cur.fetchall()
        conn.close()
        return rows
    