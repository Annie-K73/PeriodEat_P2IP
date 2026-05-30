import streamlit as st
from Models.Anamnese import Anamnese
from Models.Utilisateur import Utilisateur
from Models.Vendre import Vendre
from Models.Ingredient import Ingredient

def afficher():
    st.title("👤 Mon profil")

    utilisateur = st.session_state.utilisateur
    id_utilisateur = utilisateur[0]
    estProfessionnel = utilisateur[6]
    estParticulier = utilisateur[5]

    # Infos du compte
    st.subheader("Mes informations")
    st.write(f"**Nom :** {utilisateur[1]} {utilisateur[2]}")
    st.write(f"**Email :** {utilisateur[3]}")
    st.write(f"**Type de compte :** {'Particulier' if utilisateur[5] else 'Professionnel'}")
    if estProfessionnel:
        st.write(f"**Entreprise :** {utilisateur[7]}")

    st.divider()

    if(estParticulier):
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
                symptomes = st.text_area("Symptômes", value=anamnese[1] if anamnese[1] else "")

                if st.form_submit_button("Mettre à jour"):
                    Anamnese.mettre_a_jour(id_utilisateur, str(date_debut), duree,symptomes)
                    Anamnese.calculer_phase(id_utilisateur)
                    st.success("Dossier mis à jour !")
                    st.rerun()
        else:
            st.info("Vous n'avez pas encore renseigné votre dossier de santé.")
            with st.form("form_anamnese_new"):
                date_debut = st.date_input("Date de début du cycle")
                duree = st.number_input("Durée du cycle (jours)", min_value=21, max_value=35, value=28)
                symptomes = st.text_area("Symptômes (optionnel)")

                if st.form_submit_button("Enregistrer"):
                    a = Anamnese(
                        id_utilisateur=id_utilisateur,
                        dateDebutCycle=str(date_debut),
                        dureeCycle=duree,
                        symptomes=symptomes
                    )
                    a.sauvegarder()
                    Anamnese.calculer_phase(id_utilisateur)
                    st.success("Dossier enregistré !")
                    st.rerun()

        st.divider()

    elif(estProfessionnel):
        options = ["En vente","Ajouter un produit"]
        tabVente, tabAjout = st.tabs(options)

        with tabVente:
            st.header("Liste de vos produits")
            produits = Vendre.get_tous_par_id_vendeur(id_utilisateur)
            if(produits):
                for produit in produits:
                    ingredient = Ingredient.get_par_id_ingredient(produit[1])
                    st.write(f"**{ingredient[1]}** | Saison : {ingredient[3]}")
            else:
                st.info("Aucun produit mis en vente")

        with tabAjout:
            st.header("Sélectionner un produit à ajouter à votre catalogue")
            st.subheader("(parmi ceux proposés)")
            with st.form("form_produit"):
                tous_ingredients = Ingredient.get_tous()
                ingredients_choisis = st.multiselect(
                    label="Ingrédients",
                    options=tous_ingredients,
                    format_func=lambda i: i[1]  # affiche le nom de l'ingrédient
                )


                if st.form_submit_button("Ajouter le produit"):
                    if not ingredients_choisis:
                        st.error("Sélectionnez au moins un produit.")
                    else:
        
                        # Sauvegarde du produit
                        for i in ingredients_choisis:
                            id_ingredient = i[0]
                            try:
                                p = Vendre(id_utilisateur,id_ingredient)
                                p.sauvegarder()
                                st.success(f"Produit '{i[1]}' ajouté !")

                            except: # Si arguements invalides ou le produit figure déjà dans l'inventaire du vendeur
                                st.error("Ajout invalide")
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