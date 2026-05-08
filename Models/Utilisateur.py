from Database import get_connection
from datetime import date
 
class Utilisateur:
    def __init__(self, nom, prenom, email, mdp, dateNaissance,estParticulier=True, estProfessionnel=False, nomEntreprise=None, dateInscription=None):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.estParticulier = estParticulier
        self.estProfessionnel = estProfessionnel
        self.nomEntreprise = nomEntreprise
        self.dateNaissance = dateNaissance
        self.dateInscription = dateInscription or date.today()
 
    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""INSERT INTO Utilisateur(nom, prenom, email, mdp, estParticulier, estProfessionnel, nomEntreprise, dateNaissance, dateInscription)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.nom, self.prenom, self.email, self.mdp,
              self.estParticulier, self.estProfessionnel,
              self.nomEntreprise, self.dateNaissance, self.dateInscription))
        conn.commit()
        conn.close()
 
    @staticmethod
    def get_par_email(email):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Utilisateur WHERE email = ?", (email,))
        row = cur.fetchone()
        conn.close()
        return row
 
    @staticmethod
    def get_par_id(id_utilisateur):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Utilisateur WHERE Id_utilisateur = ?", (id_utilisateur,))
        row = cur.fetchone()
        conn.close()
        return row
 
    @staticmethod
    def supprimer(id_utilisateur):
        """Supprime l'utilisateur et ses données en cascade (RGPD)."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Utilisateur WHERE Id_utilisateur = ?", (id_utilisateur,))
        conn.commit()
        conn.close()
