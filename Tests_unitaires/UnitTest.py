import unittest
import sys
import os
os.environ["DB_PATH"] = "test_periodeat.db"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database import init_db, get_connection
from Models.Anamnese import Anamnese
from Models.Article import Article
from Models.Avis import Avis
from Models.Composer import Composer
from Models.Forum import Forum
from Models.Ingredient import Ingredient
from Models.Message import Message
from Models.Plat import Plat
from Models.Utilisateur import Utilisateur
from Models.Vendre import Vendre

###################################################################################
## Commande pour exécuter les tests : py -m unittest Tests_unitaires/UnitTest.py    
###################################################################################


def nettoyer_bdd():
    """Supprime toutes les données de test après chaque test."""
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript("""
        DELETE FROM Vendre;
        DELETE FROM Message;
        DELETE FROM Avis;
        DELETE FROM Composer;
        DELETE FROM Article;
        DELETE FROM Anamnese;
        DELETE FROM Lire;
        DELETE FROM Consulter;
        DELETE FROM Utilisateur;
        DELETE FROM Plat;
        DELETE FROM Ingredient;
        DELETE FROM Forum;
    """)
    conn.commit()
    conn.close()


class TestUtilisateur(unittest.TestCase): # 5 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_utilisateur(self):
        """Un utilisateur peut être créé et récupéré par email."""
        u = Utilisateur("Dupont", "Marie", "marie@test.com", "mdp123", "2000-03-15", estParticulier=True)
        u.sauvegarder()
        result = Utilisateur.get_par_email("marie@test.com")
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Dupont")
        self.assertEqual(result[2], "Marie")

    def test_email_inexistant(self):
        """Un email inexistant retourne None."""
        result = Utilisateur.get_par_email("inexistant@test.com")
        self.assertIsNone(result)

    def test_get_par_id(self):
        """Un utilisateur peut être récupéré par son id."""
        u = Utilisateur("Martin", "Sophie", "sophie@test.com", "mdp456", "1995-06-20", estParticulier=True)
        u.sauvegarder()
        utilisateur = Utilisateur.get_par_email("sophie@test.com")
        result = Utilisateur.get_par_id(utilisateur[0])
        self.assertIsNotNone(result)
        self.assertEqual(result[3], "sophie@test.com")

    def test_suppression_utilisateur(self):
        """Un utilisateur supprimé ne peut plus être retrouvé."""
        u = Utilisateur("Bernard", "Claire", "claire@test.com", "mdp789", "1990-01-01", estParticulier=True)
        u.sauvegarder()
        utilisateur = Utilisateur.get_par_email("claire@test.com")
        Utilisateur.supprimer(utilisateur[0])
        result = Utilisateur.get_par_email("claire@test.com")
        self.assertIsNone(result)

    def test_compte_professionnel(self):
        """Un compte professionnel est bien enregistré avec le nom d'entreprise."""
        u = Utilisateur("Durand", "Marc", "marc@entreprise.com", "mdp000", "1985-05-10",
                        estParticulier=False, estProfessionnel=True, nomEntreprise="BioShop")
        u.sauvegarder()
        result = Utilisateur.get_par_email("marc@entreprise.com")
        self.assertIsNotNone(result)
        self.assertEqual(result[7], "BioShop")


class TestAnamnese(unittest.TestCase): # 6 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()
        u = Utilisateur("Test", "User", "test@anamnese.com", "mdp", "2000-01-01", estParticulier=True)
        u.sauvegarder()
        self.utilisateur = Utilisateur.get_par_email("test@anamnese.com")
        self.id_utilisateur = self.utilisateur[0]

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_anamnese(self):
        """Une anamnèse peut être créée et récupérée."""
        a = Anamnese(self.id_utilisateur, dateDebutCycle="2026-05-01", dureeCycle=28,
                     phaseActuelle="folliculaire", symptomes="fatigue")
        a.sauvegarder()
        result = Anamnese.get_par_utilisateur(self.id_utilisateur)
        self.assertIsNotNone(result)
        self.assertEqual(result[1],"fatigue")

    def test_mise_a_jour_phase(self):
        """La phase peut être mise à jour."""
        a = Anamnese(self.id_utilisateur, dateDebutCycle="2026-05-01", dureeCycle=28,
                     phaseActuelle="folliculaire")
        a.sauvegarder()
        Anamnese.mettre_a_jour_phase(self.id_utilisateur, "ovulation")
        result = Anamnese.get_par_utilisateur(self.id_utilisateur)
        self.assertEqual(result[4], "ovulation")

    def test_calcul_phase_menstruelle(self):
        """La phase menstruelle est correctement calculée pour les jours 1-5."""
        from datetime import date, timedelta
        date_debut = date.today() - timedelta(days=3)
        a = Anamnese(self.id_utilisateur, dateDebutCycle=str(date_debut), dureeCycle=28,
                     phaseActuelle="folliculaire")
        a.sauvegarder()
        phase = Anamnese.calculer_phase(self.id_utilisateur)
        self.assertEqual(phase, "menstruelle")

    def test_calcul_phase_folliculaire(self):
        """La phase folliculaire est correctement calculée pour les jours 6-13."""
        from datetime import date, timedelta
        date_debut = date.today() - timedelta(days=8)
        a = Anamnese(self.id_utilisateur, dateDebutCycle=str(date_debut), dureeCycle=28,
                     phaseActuelle="menstruelle")
        a.sauvegarder()
        phase = Anamnese.calculer_phase(self.id_utilisateur)
        self.assertEqual(phase, "folliculaire")

    def test_suppression_cascade_rgpd(self):
        """La suppression d'un utilisateur supprime son anamnèse (RGPD)."""
        a = Anamnese(self.id_utilisateur, dateDebutCycle="2026-05-01", dureeCycle=28,
                     phaseActuelle="folliculaire")
        a.sauvegarder()
        Utilisateur.supprimer(self.id_utilisateur)
        result = Anamnese.get_par_utilisateur(self.id_utilisateur)
        self.assertIsNone(result)

    def test_anamnese_inexistante(self):
        """Un utilisateur sans anamnèse retourne None."""
        result = Anamnese.get_par_utilisateur(self.id_utilisateur)
        self.assertIsNone(result)


class TestIngredient(unittest.TestCase): # 3 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_ingredient(self):
        """Un ingrédient peut être créé et récupéré."""
        i = Ingredient("Lentilles", False, "Toute l'année", 10, 8, 8, 9)
        i.sauvegarder()
        result = Ingredient.get_tous()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Lentilles")

    def test_get_par_id(self):
        """Un ingrédient peut être récupéré par son id."""
        i = Ingredient("Épinards", True, "Mars-Nov", 10, 9, 8, 8)
        i.sauvegarder()
        tous = Ingredient.get_tous()
        result = Ingredient.get_par_id_ingredient(tous[0][0])
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Épinards")

    def test_plusieurs_ingredients(self):
        """Plusieurs ingrédients peuvent être ajoutés."""
        Ingredient("Lentilles", False, "Toute l'année", 10, 8, 8, 9).sauvegarder()
        Ingredient("Épinards", True, "Mars-Nov", 10, 9, 8, 8).sauvegarder()
        Ingredient("Saumon", False, "Toute l'année", 9, 9, 9, 9).sauvegarder()
        result = Ingredient.get_tous()
        self.assertEqual(len(result), 3)


class TestPlat(unittest.TestCase): # 5 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_plat(self):
        """Un plat peut être créé et récupéré."""
        p = Plat("Soupe de lentilles", 9, 7, 7, 8, "Une soupe réconfortante.", 2, "facile")
        p.sauvegarder()
        result = Plat.get_tous()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Soupe de lentilles")

    def test_get_par_phase_menstruelle(self):
        """Les plats sont triés par score décroissant pour la phase menstruelle."""
        Plat("Plat A", 9, 5, 5, 5, "desc", 2, "facile").sauvegarder()
        Plat("Plat B", 6, 5, 5, 5, "desc", 2, "facile").sauvegarder()
        Plat("Plat C", 10, 5, 5, 5, "desc", 2, "facile").sauvegarder()
        result = Plat.get_par_phase("menstruelle")
        self.assertEqual(result[0][1], "Plat C")
        self.assertEqual(result[1][1], "Plat A")
        self.assertEqual(result[2][1], "Plat B")

    def test_calcul_scores(self):
        """Le score d'un plat est correctement calculé depuis ses ingrédients."""
        ingredients = [
            (1, "Lentilles", False, "Toute l'année", 10, 8, 8, 9),
            (2, "Épinards", True, "Mars-Nov", 10, 9, 8, 8),
        ]
        score_m, score_f, score_o, score_l = Plat.calculer_scores(ingredients)
        self.assertEqual(score_m, 10.0)
        self.assertEqual(score_f, 8.5)
        self.assertEqual(score_o, 8.0)
        self.assertEqual(score_l, 8.5)

    def test_calcul_scores_liste_vide(self):
        """Le calcul de score avec une liste vide retourne 0."""
        result = Plat.calculer_scores([])
        self.assertEqual(result, (0, 0, 0, 0))

    def test_get_par_id(self):
        """Un plat peut être récupéré par son id."""
        Plat("Curry de lentilles", 9, 7, 7, 8, "desc", 4, "moyen").sauvegarder()
        tous = Plat.get_tous()
        result = Plat.get_par_id(tous[0][0])
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "Curry de lentilles")


class TestComposer(unittest.TestCase): # 3 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()
        Ingredient("Lentilles", False, "Toute l'année", 10, 8, 8, 9).sauvegarder()
        Ingredient("Épinards", True, "Mars-Nov", 10, 9, 8, 8).sauvegarder()
        Plat("Soupe de lentilles", 9, 7, 7, 8, "desc", 2, "facile").sauvegarder()
        self.id_plat = Plat.get_tous()[0][0]
        self.id_ingredient1 = Ingredient.get_tous()[0][0]
        self.id_ingredient2 = Ingredient.get_tous()[1][0]

    def tearDown(self):
        nettoyer_bdd()

    def test_association_plat_ingredient(self):
        """Un ingrédient peut être associé à un plat."""
        Composer(self.id_plat, self.id_ingredient1).sauvegarder()
        result = Ingredient.get_par_plat(self.id_plat)
        self.assertEqual(len(result), 1)

    def test_plusieurs_ingredients_par_plat(self):
        """Plusieurs ingrédients peuvent être associés à un plat."""
        Composer(self.id_plat, self.id_ingredient1).sauvegarder()
        Composer(self.id_plat, self.id_ingredient2).sauvegarder()
        result = Ingredient.get_par_plat(self.id_plat)
        self.assertEqual(len(result), 2)

    def test_suppression_association(self):
        """Une association plat/ingrédient peut être supprimée."""
        Composer(self.id_plat, self.id_ingredient1).sauvegarder()
        Composer.supprimer(self.id_plat, self.id_ingredient1)
        result = Ingredient.get_par_plat(self.id_plat)
        self.assertEqual(len(result), 0)


class TestForum(unittest.TestCase): # 3 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_forum(self):
        """Un forum peut être créé et récupéré."""
        Forum("Comprendre son cycle", "Articles éducatifs").sauvegarder()
        result = Forum.get_tous()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Comprendre son cycle")

    def test_get_par_id(self):
        """Un forum peut être récupéré par son id."""
        Forum("Communauté", "Espace d'échange").sauvegarder()
        tous = Forum.get_tous()
        result = Forum.get_par_id(tous[0][0])
        self.assertIsNotNone(result)

    def test_plusieurs_forums(self):
        """Plusieurs forums peuvent être créés."""
        Forum("Forum 1", "desc 1").sauvegarder()
        Forum("Forum 2", "desc 2").sauvegarder()
        result = Forum.get_tous()
        self.assertEqual(len(result), 2)


class TestArticle(unittest.TestCase): # 3 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()
        Forum("Comprendre son cycle", "Articles éducatifs").sauvegarder()
        self.id_forum = Forum.get_tous()[0][0]

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_article(self):
        """Un article peut être créé et récupéré."""
        Article("Phase menstruelle", "Contenu de l'article", self.id_forum).sauvegarder()
        result = Article.get_par_forum(self.id_forum)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Phase menstruelle")

    def test_plusieurs_articles_par_forum(self):
        """Plusieurs articles peuvent être ajoutés à un forum."""
        Article("Phase menstruelle", "Contenu 1", self.id_forum).sauvegarder()
        Article("Phase folliculaire", "Contenu 2", self.id_forum).sauvegarder()
        Article("Phase ovulatoire", "Contenu 3", self.id_forum).sauvegarder()
        result = Article.get_par_forum(self.id_forum)
        self.assertEqual(len(result), 3)

    def test_article_mauvais_forum(self):
        """Un forum inexistant ne retourne aucun article."""
        result = Article.get_par_forum(9999)
        self.assertEqual(len(result), 0)


class TestAvis(unittest.TestCase): # 4 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()
        Utilisateur("Test", "User", "test@avis.com", "mdp", "2000-01-01", estParticulier=True).sauvegarder()
        self.utilisateur = Utilisateur.get_par_email("test@avis.com")
        self.id_utilisateur = self.utilisateur[0]
        Forum("Communauté", "desc").sauvegarder()
        self.id_forum = Forum.get_tous()[0][0]
        Plat("Soupe", 9, 7, 7, 8, "desc", 2, "facile").sauvegarder()
        self.id_plat = Plat.get_tous()[0][0]

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_avis(self):
        """Un avis peut être créé et récupéré par plat."""
        Avis("Délicieux !", 5, self.id_forum, self.id_plat, self.id_utilisateur).sauvegarder()
        result = Avis.get_par_plat(self.id_plat)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][2], 5)

    def test_avis_par_forum(self):
        """Les avis peuvent être récupérés par forum."""
        Avis("Très bien !", 4, self.id_forum, self.id_plat, self.id_utilisateur).sauvegarder()
        result = Avis.get_par_forum(self.id_forum)
        self.assertEqual(len(result), 1)

    def test_note_avis(self):
        """La note d'un avis est correctement enregistrée."""
        Avis("Bof", 2, self.id_forum, self.id_plat, self.id_utilisateur).sauvegarder()
        result = Avis.get_par_plat(self.id_plat)
        self.assertEqual(result[0][2], 2)

    def test_suppression_cascade_avis(self):
        """La suppression d'un utilisateur supprime ses avis (RGPD)."""
        Avis("Super !", 5, self.id_forum, self.id_plat, self.id_utilisateur).sauvegarder()
        Utilisateur.supprimer(self.id_utilisateur)
        result = Avis.get_par_plat(self.id_plat)
        self.assertEqual(len(result), 0)


class TestMessage(unittest.TestCase): # 3 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()
        Utilisateur("Test", "User", "test@message.com", "mdp", "2000-01-01", estParticulier=True).sauvegarder()
        self.utilisateur = Utilisateur.get_par_email("test@message.com")
        self.id_utilisateur = self.utilisateur[0]
        Forum("Communauté", "desc").sauvegarder()
        self.id_forum = Forum.get_tous()[0][0]

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_message(self):
        """Un message libre peut être créé et récupéré."""
        Message("Bonjour tout le monde !", self.id_forum, self.id_utilisateur).sauvegarder()
        result = Message.get_par_forum(self.id_forum)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Bonjour tout le monde !")

    def test_plusieurs_messages(self):
        """Plusieurs messages peuvent être postés dans un forum."""
        Message("Message 1", self.id_forum, self.id_utilisateur).sauvegarder()
        Message("Message 2", self.id_forum, self.id_utilisateur).sauvegarder()
        result = Message.get_par_forum(self.id_forum)
        self.assertEqual(len(result), 2)

    def test_suppression_cascade_message(self):
        """La suppression d'un utilisateur supprime ses messages (RGPD)."""
        Message("Message à supprimer", self.id_forum, self.id_utilisateur).sauvegarder()
        Utilisateur.supprimer(self.id_utilisateur)
        result = Message.get_par_forum(self.id_forum)
        self.assertEqual(len(result), 0)


class TestVendre(unittest.TestCase): # 3 tests

    def setUp(self):
        init_db()
        nettoyer_bdd()
        Utilisateur("BioShop", "Pro", "pro@bioshop.com", "mdp", "1990-01-01",
                    estParticulier=False, estProfessionnel=True, nomEntreprise="BioShop").sauvegarder()
        self.utilisateur = Utilisateur.get_par_email("pro@bioshop.com")
        self.id_utilisateur = self.utilisateur[0]
        Ingredient("Lentilles", False, "Toute l'année", 10, 8, 8, 9).sauvegarder()
        self.id_ingredient = Ingredient.get_tous()[0][0]

    def tearDown(self):
        nettoyer_bdd()

    def test_creation_vendre(self):
        """Un professionnel peut référencer un ingrédient qu'il vend."""
        v = Vendre(self.id_utilisateur, self.id_ingredient)
        v.sauvegarder()
        result = Vendre.get_tous_par_id_vendeur(self.id_utilisateur)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) > 0)

    def test_vendeurs_par_ingredient(self):
        """Les vendeurs d'un ingrédient peuvent être récupérés."""
        Vendre(self.id_utilisateur, self.id_ingredient).sauvegarder()
        result = Vendre.get_vendeurs_par_ingredient(self.id_ingredient)
        self.assertEqual(len(result), 1)

    def test_ingredient_sans_vendeur(self):
        """Un ingrédient sans vendeur retourne une liste vide."""
        result = Vendre.get_vendeurs_par_ingredient(self.id_ingredient)
        self.assertEqual(len(result), 0) 



