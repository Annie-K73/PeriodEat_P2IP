from Database import get_connection

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
    def mettre_a_jour(id_utilisateur, dateDebutCycle, dureeCycle, phaseActuelle, symptomes):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Anamnese
            SET dateDebutCycle = ?, dureeCycle = ?, phaseActuelle = ?, symptomes = ?
            WHERE Id_utilisateur = ?
        """, (dateDebutCycle, dureeCycle, phaseActuelle, symptomes, id_utilisateur))
        conn.commit()
        conn.close()