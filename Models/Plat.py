from Database import get_connection
from Models.Ingredient import Ingredient
from Outils.Utils import ingredient_de_saison


class Plat:
    def __init__(self, nom, scoreMenstruelle, scoreFolliculaire, scoreOvulation, scoreLuteale, description, nbPersonne, difficulte, photoUrl=None):
        self.nom = nom
        self.scoreMenstruelle = scoreMenstruelle
        self.scoreFolliculaire = scoreFolliculaire
        self.scoreOvulation = scoreOvulation
        self.scoreLuteale = scoreLuteale
        self.description = description
        self.nbPersonne = nbPersonne
        self.difficulte = difficulte  # 'facile', 'moyen', 'difficile'
        self.photoUrl = photoUrl

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Plat
            (nom, scoreMenstruelle, scoreFolliculaire, scoreOvulation,
             scoreLuteale, description, nbPersonne, difficulte, photoUrl)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.nom, self.scoreMenstruelle, self.scoreFolliculaire,
              self.scoreOvulation, self.scoreLuteale, self.description,
              self.nbPersonne, self.difficulte, self.photoUrl))
        conn.commit()
        conn.close()

    @staticmethod
    def get_par_phase(phase):
        """Retourne les plats triés par score décroissant pour la phase donnée."""
        colonnes = {
            "menstruelle": "scoreMenstruelle",
            "folliculaire": "scoreFolliculaire",
            "ovulation": "scoreOvulation",
            "luteale": "scoreLuteale"
        }
        colonne = colonnes.get(phase)
        if not colonne:
            return []
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Plat ORDER BY {colonne} DESC")
        rows = cur.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def get_plats_de_saison():
        """Retourne les plats dont tous les ingrédients sont de saison."""

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT p.* FROM Plat p
            JOIN Composer c ON p.id_plat = c.id_plat
            JOIN Ingredient i ON c.id_ingredient = i.id_ingredient
        """)

        conn.close()

        # On récupère les plats dont tous les ingrédients sont de saison
        plats_de_saison = []

        tous_plats = Plat.get_tous()
        for plat in tous_plats:
            ingredients = Ingredient.get_par_plat(plat[0])
            if all(ingredient_de_saison(i[3]) for i in ingredients):
                plats_de_saison.append(plat)

        return plats_de_saison


    @staticmethod
    def get_tous():
        """Retourne toutes les lignes de la table Plat"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Plat")
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_par_id(id_plat):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Plat WHERE id_plat = ?", (id_plat,))
        row = cur.fetchone()
        conn.close()
        return row
    
    
    @staticmethod
    def calculer_scores(ingredients):
        """Calcule les scores d'un plat à partir de ses ingrédients, ramenés sur 10."""
        if not ingredients:
            return 0, 0, 0, 0
        
        n = len(ingredients)
        score_m = round(sum(i[4] for i in ingredients) / n, 1)
        score_f = round(sum(i[5] for i in ingredients) / n, 1)
        score_o = round(sum(i[6] for i in ingredients) / n, 1)
        score_l = round(sum(i[7] for i in ingredients) / n, 1)
        
        return score_m, score_f, score_o, score_l