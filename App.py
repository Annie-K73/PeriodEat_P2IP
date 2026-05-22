from Database import init_db
from Models.Plat import Plat
from Models.Ingredient import Ingredient
from Models.Utilisateur import Utilisateur
from Models.Anamnese import Anamnese
from ImportCSV import import_aliments
import streamlit as st

############################################################################
##  COMMANDE POUR LANCER L'APPLI (terminal) : py -m streamlit run App.py
#############################################################################

####################################################
## COMPTE DE TEST : lea@test.com et mdp : 1234
####################################################

# Initialisation de la base de données
init_db()

# Chargement/synchronisation des aliments CSV à chaque lancement
Ingredient.synchroniser_csv()

# Configuration de la page
st.set_page_config(
    page_title="PeriodEat",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de la session
if "connecte" not in st.session_state:
    st.session_state.connecte = False
if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None

if st.session_state.connecte:
    Anamnese.calculer_phase(st.session_state.utilisateur[0])

# Navigation
if not st.session_state.connecte:
    from Interface.Connexion import afficher
    afficher()
else:
    st.sidebar.title("🌸 PeriodEat")
    st.sidebar.write(f"Bonjour, {st.session_state.utilisateur[2]} !")
    st.sidebar.divider()

    page = st.sidebar.radio("Navigation", [
        "🏠 Accueil",
        "🍽️ Recettes",
        "🌸 Ma recette",
        "💬 Forum",
        "👤 Mon profil",
        "⚙️ Admin"
    ])

    st.sidebar.divider()
    if st.sidebar.button("Se déconnecter"):
        st.session_state.connecte = False
        st.session_state.utilisateur = None
        st.rerun()

    if page == "🏠 Accueil":
        from Interface.Accueil import afficher
        afficher()
    elif page == "🍽️ Recettes":
        from Interface.Recettes import afficher
        afficher()
    elif page == "🌸 Ma recette":
        from Interface.MaRecette import afficher
        afficher()
    elif page == "💬 Forum":
        from Interface.Forum import afficher
        afficher()
    elif page == "👤 Mon profil":
        from Interface.Profil import afficher
        afficher()
    elif page == "⚙️ Admin":
        from Interface.Admin import afficher
        afficher()