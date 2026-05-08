import streamlit as st
import os
from Models.Plat import Plat
from Models.Ingredient import Ingredient
from Models.Composer import Composer

def afficher():
    st.title("🌸 Partager ma recette")
    st.write("Proposez votre propre recette à la communauté ! Elle sera signalée par une fleur 🌸.")
    st.divider()

    with st.form("form_ma_recette"):
        nom = st.text_input("Nom de la recette ")
        description = st.text_area("Description")

        tous_ingredients = Ingredient.get_tous()
        ingredients_choisis = st.multiselect(
            label="Ingrédients",
            options=tous_ingredients,
            format_func=lambda i: i[1]
        )

        nb_personnes = st.number_input("Nombre de personnes", min_value=1, value=2)
        difficulte = st.selectbox("Difficulté", ["facile", "moyen", "difficile"])

        # Sélection de la photo
        images_disponibles = os.listdir("Images") if os.path.exists("Images") else []
        photo_choisie = None
        if images_disponibles:
            photo_choisie = st.selectbox("Photo (optionnel)", ["Aucune"] + images_disponibles)
        else:
            st.info("Aucune image disponible.")

        if st.form_submit_button("Publier ma recette"):
            if not nom:
                st.error("Le nom est obligatoire.")
            elif not ingredients_choisis:
                st.error("Sélectionnez au moins un ingrédient.")
            else:
                # Calcul automatique des scores
                score_m, score_f, score_o, score_l = Plat.calculer_scores(ingredients_choisis)

                # Préfixe🌸 pour distinguer les recettes utilisateurs (non officielles)
                nom_final = f"🌸 {nom}"

                # Gestion de la photo
                photo_url = None
                if photo_choisie and photo_choisie != "Aucune":
                    photo_url = f"Images/{photo_choisie}"

                # Sauvegarde du plat
                p = Plat(
                    nom=nom_final,
                    scoreMenstruelle=score_m,
                    scoreFolliculaire=score_f,
                    scoreOvulation=score_o,
                    scoreLuteale=score_l,
                    description=description,
                    nbPersonne=nb_personnes,
                    difficulte=difficulte,
                    photoUrl=photo_url
                )
                p.sauvegarder()

                # Récupération de l'id du plat créé
                plats = Plat.get_tous()
                id_plat = plats[-1][0]

                # Remplissage de la table Composer
                for ingredient in ingredients_choisis:
                    c = Composer(id_plat=id_plat, id_ingredient=ingredient[0])
                    c.sauvegarder()

                st.success(f"Recette '{nom_final}' publiée ! Scores calculés ==> Menstruelle : {score_m} | Folliculaire : {score_f} | Ovulation : {score_o} | Lutéale : {score_l}")
                st.balloons()
                st.rerun()