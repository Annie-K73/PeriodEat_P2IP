import sqlite3
 
DB_PATH = "periodeat.db"
 
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
 
def init_db():
    """Crée toutes les tables si elles n'existent pas encore."""
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS Utilisateur (
            Id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(50),
            prenom VARCHAR(50),
            email VARCHAR(50) NOT NULL,
            mdp VARCHAR(255) NOT NULL,
            estParticulier BOOLEAN,
            estProfessionnel BOOLEAN,
            nomEntreprise VARCHAR(50),
            dateNaissance DATE NOT NULL,
            dateInscription DATE NOT NULL
        );
 
        CREATE TABLE IF NOT EXISTS Anamnese (
            id_anamnese INTEGER PRIMARY KEY AUTOINCREMENT,
            symptomes VARCHAR(150),
            dateDebutCycle DATE,
            dureeCycle INT,
            phaseActuelle VARCHAR(50),
            Id_utilisateur INT NOT NULL UNIQUE,
            FOREIGN KEY (Id_utilisateur) REFERENCES Utilisateur(Id_utilisateur)
                ON DELETE CASCADE
        );
 
        CREATE TABLE IF NOT EXISTS Plat (
            id_plat INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(50),
            scoreMenstruelle INT NOT NULL,
            scoreFolliculaire INT NOT NULL,
            scoreOvulation INT NOT NULL,
            scoreLuteale INT NOT NULL,
            description VARCHAR(250),
            nbPersonne INT,
            difficulte VARCHAR(50) NOT NULL,
            photoUrl VARCHAR(250)
        );
 
        CREATE TABLE IF NOT EXISTS Ingredient (
            id_ingredient INTEGER PRIMARY KEY AUTOINCREMENT,
            nom VARCHAR(50) NOT NULL,
            estSaisonnier BOOLEAN NOT NULL,
            saison VARCHAR(50) NOT NULL,
            scoreMenstruelle INT NOT NULL,
            scoreFolliculaire INT NOT NULL,
            scoreOvulation INT NOT NULL,
            scoreLuteale INT NOT NULL
        );
 
        CREATE TABLE IF NOT EXISTS Forum (
            id_forum INTEGER PRIMARY KEY AUTOINCREMENT,
            titre VARCHAR(50) NOT NULL,
            description VARCHAR(250)
        );
 
        CREATE TABLE IF NOT EXISTS Avis (
            id_avis INTEGER PRIMARY KEY AUTOINCREMENT,
            commentaire VARCHAR(250),
            note INT NOT NULL,
            datePublication DATE NOT NULL,
            id_forum INT NOT NULL,
            id_plat INT,
            Id_utilisateur INT NOT NULL,
            FOREIGN KEY (id_forum) REFERENCES Forum(id_forum),
            FOREIGN KEY (id_plat) REFERENCES Plat(id_plat),
            FOREIGN KEY (Id_utilisateur) REFERENCES Utilisateur(Id_utilisateur)
                ON DELETE CASCADE
        );
 
        CREATE TABLE IF NOT EXISTS Article (
            id_article INTEGER PRIMARY KEY AUTOINCREMENT,
            titre VARCHAR(50) NOT NULL,
            description VARCHAR(255) NOT NULL,
            datePublication DATE NOT NULL,
            id_forum INT NOT NULL,
            FOREIGN KEY (id_forum) REFERENCES Forum(id_forum)
        );
 
        CREATE TABLE IF NOT EXISTS Composer (
            id_plat INT,
            id_ingredient INT,
            PRIMARY KEY (id_plat, id_ingredient),
            FOREIGN KEY (id_plat) REFERENCES Plat(id_plat),
            FOREIGN KEY (id_ingredient) REFERENCES Ingredient(id_ingredient)
        );
 
        CREATE TABLE IF NOT EXISTS Consulter (
            Id_utilisateur INT,
            id_plat INT,
            PRIMARY KEY (Id_utilisateur, id_plat),
            FOREIGN KEY (Id_utilisateur) REFERENCES Utilisateur(Id_utilisateur),
            FOREIGN KEY (id_plat) REFERENCES Plat(id_plat)
        );
 
        CREATE TABLE IF NOT EXISTS Lire (
            Id_utilisateur INT,
            id_forum INT,
            PRIMARY KEY (Id_utilisateur, id_forum),
            FOREIGN KEY (Id_utilisateur) REFERENCES Utilisateur(Id_utilisateur),
            FOREIGN KEY (id_forum) REFERENCES Forum(id_forum)
        );
    """)
    conn.commit()
    conn.close()