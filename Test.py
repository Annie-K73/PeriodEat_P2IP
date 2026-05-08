from Database import init_db
from Models.Utilisateur import Utilisateur
from Models.Anamnese import Anamnese
from Models.Plat import Plat
from Models.Ingredient import Ingredient
from Models.Forum import Forum
from Models.Avis import Avis
from Models.Article import Article

print("=== DEBUT DE TEST ! ===")
print("=== Initialisation de la base de données ===")
init_db()
print("✓ Tables créées avec succès\n")

# ─────────────────────────────────────────────
# TEST UTILISATEUR
# ─────────────────────────────────────────────
print("=== Test Utilisateur ===")
u = Utilisateur(
    nom="Dupont",
    prenom="Léa",
    email="lea@test.com",
    mdp="motdepasse123",
    dateNaissance="2000-03-15",
    estParticulier=True
)
u.sauvegarder()
print("✓ Utilisateur sauvegardé")

resultat = Utilisateur.get_par_email("lea@test.com")
print(f"✓ Utilisateur récupéré : {resultat[1]} {resultat[2]}")
id_utilisateur = resultat[0]
print()

# ─────────────────────────────────────────────
# TEST ANAMNESE
# ─────────────────────────────────────────────
print("=== Test Anamnese ===")
a = Anamnese(
    id_utilisateur=id_utilisateur,
    dateDebutCycle="2025-04-01",
    dureeCycle=28,
    phaseActuelle="folliculaire",
    symptomes="fatigue, maux de tête"
)
a.sauvegarder()
print("✓ Anamnese sauvegardée")

anamnese = Anamnese.get_par_utilisateur(id_utilisateur)
print(f"✓ Anamnese récupérée : phase = {anamnese[4]}")

Anamnese.mettre_a_jour_phase(id_utilisateur, "ovulation")
anamnese = Anamnese.get_par_utilisateur(id_utilisateur)
print(f"✓ Phase mise à jour : {anamnese[4]}")
print()

# ─────────────────────────────────────────────
# TEST INGREDIENT
# ─────────────────────────────────────────────
print("=== Test Ingredient ===")
i = Ingredient(
    nom="Lentilles",
    estSaisonnier=False,
    saison="toute saison",
    scoreMenstruelle=10,
    scoreFolliculaire=8,
    scoreOvulation=8,
    scoreLuteale=9
)
i.sauvegarder()
print("✓ Ingrédient sauvegardé")

ingredients = Ingredient.get_tous()
print(f"✓ {len(ingredients)} ingrédient(s) dans la base")
id_ingredient = ingredients[0][0]
print()

# ─────────────────────────────────────────────
# TEST PLAT
# ─────────────────────────────────────────────
print("=== Test Plat ===")
p = Plat(
    nom="Soupe de lentilles corail",
    scoreMenstruelle=9,
    scoreFolliculaire=7,
    scoreOvulation=7,
    scoreLuteale=8,
    description="Une soupe réconfortante riche en fer, idéale pendant la phase menstruelle.",
    nbPersonne=2,
    difficulte="facile",
    photoUrl="images/soupe_lentilles.jpg"
)
p.sauvegarder()
print("✓ Plat sauvegardé")

plats = Plat.get_tous()
print(f"✓ {len(plats)} plat(s) dans la base")
id_plat = plats[0][0]

plats_phase = Plat.get_par_phase("menstruelle")
print(f"✓ Plats recommandés phase menstruelle : {[plat[1] for plat in plats_phase]}")
print()

# ─────────────────────────────────────────────
# TEST FORUM
# ─────────────────────────────────────────────
print("=== Test Forum ===")
f = Forum(
    titre="Communauté PeriodEat",
    description="Espace d'échange entre utilisatrices"
)
f.sauvegarder()
print("✓ Forum sauvegardé")

forums = Forum.get_tous()
print(f"✓ {len(forums)} forum(s) dans la base")
id_forum = forums[0][0]
print()

# ─────────────────────────────────────────────
# TEST ARTICLE
# ─────────────────────────────────────────────
print("=== Test Article ===")
art = Article(
    titre="Comprendre la phase folliculaire",
    description="La phase folliculaire commence après les règles et dure jusqu'à l'ovulation. C'est une période d'énergie croissante...",
    id_forum=id_forum
)
art.sauvegarder()
print("✓ Article sauvegardé")

articles = Article.get_par_forum(id_forum)
print(f"✓ {len(articles)} article(s) dans le forum")
print()

# ─────────────────────────────────────────────
# TEST AVIS
# ─────────────────────────────────────────────
print("=== Test Avis ===")
av = Avis(
    commentaire="Excellente recette, je me sens vraiment mieux !",
    note=5,
    id_forum=id_forum,
    id_plat=id_plat,
    id_utilisateur=id_utilisateur
)
av.sauvegarder()
print("✓ Avis sauvegardé")

avis = Avis.get_par_plat(id_plat)
print(f"✓ {len(avis)} avis pour ce plat : note = {avis[0][2]}/5")
print()

# ─────────────────────────────────────────────
# TEST SUPPRESSION (RGPD)
# ─────────────────────────────────────────────
print("=== Test Suppression RGPD ===")
Utilisateur.supprimer(id_utilisateur)
print("✓ Utilisateur supprimé")

anamnese_apres = Anamnese.get_par_utilisateur(id_utilisateur)
print(f"✓ Anamnese supprimée en cascade : {anamnese_apres}")
print()

print("=== FIN DE TEST ! ===")