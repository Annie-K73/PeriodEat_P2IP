import streamlit as st
from Models.Utilisateur import Utilisateur
from datetime import date

def afficher():
    st.title("🌸 PeriodEat")
    st.subheader("Bienvenue ! Connectez-vous ou créez un compte.")
    st.divider()

    onglet1, onglet2 = st.tabs(["Se connecter", "S'inscrire"])

    ################################################
    ###              CONNEXION
    ################################################
    with onglet1:
        st.subheader("Connexion")
        email = st.text_input("Email", key="login_email")
        mdp = st.text_input("Mot de passe", type="password", key="login_mdp")

        if st.button("Se connecter"):
            utilisateur = Utilisateur.get_par_email(email)
            if utilisateur and utilisateur[4] == mdp:
                st.session_state.connecte = True
                st.session_state.utilisateur = utilisateur
                st.success("Connexion réussie !")
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect.")

    ################################################
    ###              INSCRIPTION
    ################################################
    with onglet2:
        st.subheader("Créer un compte")
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        email_inscr = st.text_input("Email", key="inscr_email")
        mdp_inscr = st.text_input("Mot de passe", type="password", key="inscr_mdp")
        date_naissance = st.date_input("Date de naissance", min_value=date(1950, 1, 1))
        type_compte = st.radio("Type de compte", ["Particulier", "Professionnel"])
        nom_entreprise = None
        if type_compte == "Professionnel":
            nom_entreprise = st.text_input("Nom de l'entreprise")

        if st.button("Créer mon compte"):
            # Champs non renseignés
            if not nom or not prenom or not email_inscr or not mdp_inscr:
                st.error("Veuillez remplir tous les champs obligatoires.")

            # compte déjà existant
            elif Utilisateur.get_par_email(email_inscr):
                st.error("Cet email est déjà utilisé.")
                
            else:
                u = Utilisateur(
                    nom=nom,
                    prenom=prenom,
                    email=email_inscr,
                    mdp=mdp_inscr,
                    dateNaissance=str(date_naissance),
                    estParticulier=(type_compte == "Particulier"),
                    estProfessionnel=(type_compte == "Professionnel"),
                    nomEntreprise=nom_entreprise
                )
                u.sauvegarder()
                st.success("Compte créé avec succès ! Connectez-vous.")