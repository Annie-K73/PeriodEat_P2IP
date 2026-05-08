from Database import get_connection

class Forum:
    def __init__(self, titre, description):
        self.titre = titre
        self.description = description

    def sauvegarder(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Forum (titre, description) VALUES (?, ?)
        """, (self.titre, self.description))
        conn.commit()
        conn.close()

    @staticmethod
    def get_tous():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Forum")
        rows = cur.fetchall()
        conn.close()
        return rows

    @staticmethod
    def get_par_id(id_forum):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Forum WHERE id_forum = ?", (id_forum,))
        row = cur.fetchone()
        conn.close()
        return row