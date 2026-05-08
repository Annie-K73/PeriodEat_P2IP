from Database import get_connection
from datetime import date, datetime

class Anamnese:
    def __init__(self, id_utilisateur, dateDebutCycle=None, dureeCycle=28, phaseActuelle=None, symptomes=None):
        self.id_utilisateur = id_utilisateur
        self.dateDebutCycle = dateDebutCycle
        self.dureeCycle = dureeCycle
        self.phaseActuelle = phaseActuelle  # menstruelle,folliculaire,ovulation,luteale
        self.symptomes = symptomes

    
    def sauvegarder(self):
        
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Anamnese
            (symptomes, dateDebutCycle, dureeCycle, phaseActuelle, Id_utilisateur)
            VALUES (?, ?, ?, ?, ?)
        """, (self.symptomes, self.dateDebutCycle, self.dureeCycle,
              self.phaseActuelle, self.id_utilisateur))
        conn.commit()
        conn.close()

    @staticmethod
    def get_par_utilisateur(id_utilisateur):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Anamnese WHERE Id_utilisateur = ?", (id_utilisateur,))
        row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def mettre_a_jour_phase(id_utilisateur, nouvelle_phase):
        """Met à jour la phase actuelle de l'utilisatrice."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Anamnese SET phaseActuelle = ? WHERE Id_utilisateur = ?
        """, (nouvelle_phase, id_utilisateur))
        conn.commit()
        conn.close()

    @staticmethod
    def mettre_a_jour(id_utilisateur, dateDebutCycle, dureeCycle, symptomes):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Anamnese
            SET dateDebutCycle = ?, dureeCycle = ?, symptomes = ?
            WHERE Id_utilisateur = ?
        """, (dateDebutCycle, dureeCycle, symptomes, id_utilisateur))
        conn.commit()
        conn.close()

    @staticmethod
    def calculer_phase(id_utilisateur):
        """Calcule et met à jour la phase actuelle d'un utilisateur selon la date du jour."""
        anamnese = Anamnese.get_par_utilisateur(id_utilisateur)
        if not anamnese:
            return None

        try :
            date_debut = datetime.strptime(anamnese[2], "%Y-%m-%d").date()
            duree_cycle = anamnese[3]

            # Nombre de jours depuis le début du cycle
            jours_ecoules = (date.today() - date_debut).days % duree_cycle

            # Détermination de la phase
            if jours_ecoules <= 5:
                phase = "menstruelle"
            elif jours_ecoules <= 13:
                phase = "folliculaire"
            elif jours_ecoules <= 15:
                phase = "ovulation"
            else:
                phase = "luteale"
            print("Phase calculée : ",phase)
            # Mise à jour en base
            Anamnese.mettre_a_jour_phase(id_utilisateur, phase)
            return phase
        except:
            print("Erreur dans calculer_phase")
            return None