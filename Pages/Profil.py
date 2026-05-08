import streamlit as st
from Models.Anamnese import Anamnese
from Models.Utilisateur import Utilisateur

def afficher():
    st.title("👤 Mon profil")

    utilisateur = st.session_state.utilisateur
    id_utilisateur = utilisateur[0]

    # Infos du compte
    st.subheader("Mes informations")
    st.write(f"**Nom :** {utilisateur[1]} {utilisateur[2]}")
    st.write(f"**Email :** {utilisateur[3]}")
    st.write(f"**Type de compte :** {'Particulier' if utilisateur[5] else 'Professionnel'}")
    if utilisateur[6]:
        st.write(f"**Entreprise :** {utilisateur[7]}")

    st.divider()

    # Dossier de santé
    st.subheader("🩺 Mon dossier de santé")
    anamnese = Anamnese.get_par_utilisateur(id_utilisateur)

    phases = ["menstruelle", "folliculaire", "ovulation", "luteale"]

    if anamnese:
        st.write(f"**Phase actuelle :** {anamnese[4]}")
        st.write(f"**Début du cycle :** {anamnese[2]}")
        st.write(f"**Durée du cycle :** {anamnese[3]} jours")
        if anamnese[1]:
            st.write(f"**Symptômes :** {anamnese[1]}")

        st.divider()
        st.subheader("Mettre à jour mon dossier")
        with st.form("form_anamnese"):
            date_debut = st.date_input("Date de début du cycle")
            duree = st.number_input("Durée du cycle (jours)", min_value=21, max_value=35, value=int(anamnese[3]) if anamnese[3] else 28)
            phase = st.selectbox("Phase actuelle", phases, index=phases.index(anamnese[4]) if anamnese[4] in phases else 0)
            symptomes = st.text_area("Symptômes", value=anamnese[1] if anamnese[1] else "")

            if st.form_submit_button("Mettre à jour"):
                Anamnese.mettre_a_jour(id_utilisateur, str(date_debut), duree, phase, symptomes)
                st.success("Dossier mis à jour !")
                st.rerun()
    else:
        st.info("Vous n'avez pas encore renseigné votre dossier de santé.")
        with st.form("form_anamnese_new"):
            date_debut = st.date_input("Date de début du cycle")
            duree = st.number_input("Durée du cycle (jours)", min_value=21, max_value=35, value=28)
            phase = st.selectbox("Phase actuelle", phases)
            symptomes = st.text_area("Symptômes (optionnel)")

            if st.form_submit_button("Enregistrer"):
                a = Anamnese(
                    id_utilisateur=id_utilisateur,
                    dateDebutCycle=str(date_debut),
                    dureeCycle=duree,
                    phaseActuelle=phase,
                    symptomes=symptomes
                )
                a.sauvegarder()
                st.success("Dossier enregistré !")
                st.rerun()

    st.divider()

    # Suppression du compte
    st.subheader("⚠️ Supprimer mon compte")
    st.warning("Cette action est irréversible. Toutes vos données seront supprimées (RGPD).")
    if st.button("Supprimer mon compte", type="primary"):
        Utilisateur.supprimer(id_utilisateur)
        st.session_state.connecte = False
        st.session_state.utilisateur = None
        st.rerun()