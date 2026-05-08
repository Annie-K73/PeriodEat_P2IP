from Database import init_db
from Models.Plat import Plat
from Models.Ingredient import Ingredient
from Models.Utilisateur import Utilisateur
from ImportCSV import import_aliments
import streamlit as st


# Initialisation de la base de données
init_db()

#Chargement de tous les ingrédients
if not Ingredient.get_tous():
    import_aliments()

# Configuration de la page
st.set_page_config(
    page_title="PeriodEat",
    page_icon="🌸",
    layout="wide"
)

# Initialisation de la session
if "connecte" not in st.session_state:
    st.session_state.connecte = False
if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = None

# Navigation
if not st.session_state.connecte:
    from Pages.Connexion import afficher
    afficher()
else:
    st.sidebar.title("🌸 PeriodEat")
    st.sidebar.write(f"Bonjour, {st.session_state.utilisateur[2]} !")
    st.sidebar.divider()

    page = st.sidebar.radio("Navigation", [
        "🏠 Accueil",
        "🍽️ Recettes",
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
        from Pages.Accueil import afficher
        afficher()
    elif page == "🍽️ Recettes":
        from Pages.Recettes import afficher
        afficher()
    elif page == "💬 Forum":
        from Pages.Forum import afficher
        afficher()
    elif page == "👤 Mon profil":
        from Pages.Profil import afficher
        afficher()
    elif page == "⚙️ Admin":
        from Pages.Admin import afficher
        afficher()