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
    
    @staticmethod
    def synchroniser_csv():
        """Synchronise les ingrédients depuis le CSV sans vider toute la BDD."""
        df = pd.read_csv("aliments_cycle.csv")

        conn = get_connection()
        cur = conn.cursor()

        for _, row in df.iterrows():
            nom = row['Aliment']
            estSaisonnier = row['Saison FR'] != "Toute l'année"
            saison = row['Saison FR']
            scoreMenstruelle = int(row['Menstruation'])
            scoreFolliculaire = int(row['Folliculaire'])
            scoreOvulation = int(row['Ovulatoire'])
            scoreLuteale = int(row['Lutéale'])

            # si l'ingrédient existe déjà, on le met à jour, sinon on l'insère
            cur.execute("SELECT id_ingredient FROM Ingredient WHERE nom = ?", (nom,))
            existant = cur.fetchone()

            if existant:
                cur.execute("""
                    UPDATE Ingredient
                    SET estSaisonnier = ?, saison = ?, scoreMenstruelle = ?,
                        scoreFolliculaire = ?, scoreOvulation = ?, scoreLuteale = ?
                    WHERE nom = ?
                """, (estSaisonnier, saison, scoreMenstruelle,
                    scoreFolliculaire, scoreOvulation, scoreLuteale, nom))
                print(f"✓ {nom} mis à jour")
            else:
                cur.execute("""
                    INSERT INTO Ingredient
                    (nom, estSaisonnier, saison, scoreMenstruelle, scoreFolliculaire,
                    scoreOvulation, scoreLuteale)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (nom, estSaisonnier, saison, scoreMenstruelle,
                    scoreFolliculaire, scoreOvulation, scoreLuteale))
                print(f"✓ {nom} ajouté")

        conn.commit()
        conn.close()
    