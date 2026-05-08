import streamlit as st
import os
from Models.Plat import Plat
from Models.Ingredient import Ingredient
from Models.Utilisateur import Utilisateur
from Models.Article import Article
from Models.Forum import Forum
from Models.Composer import Composer

def afficher():
    st.title("⚙️ Administration")

    onglet1, onglet2, onglet3 = st.tabs([" Plats", " Utilisateurs", " Articles"])

    ################################################
    ###        GESTION DES PLATS
    ################################################


    with onglet1:
        st.subheader("Ajouter un plat")
        with st.form("form_plat"):
            nom = st.text_input("Nom du plat")
            description = st.text_area("Description")
            
            tous_ingredients = Ingredient.get_tous()
            ingredients_choisis = st.multiselect(
                label="Ingrédients",
                options=tous_ingredients,
                format_func=lambda i: i[1]  # affiche le nom de l'ingrédient
            )

            images_disponibles = os.listdir("Images")
            photo_choisie = st.selectbox(
                "Photo du plat",
                options=images_disponibles,
                format_func=lambda x: x  # affiche le nom du fichier
            )
                
            nb_personnes = st.number_input("Nombre de personnes", min_value=1, value=2)
            difficulte = st.selectbox("Difficulté", ["facile", "moyen", "difficile"])

            if st.form_submit_button("Ajouter le plat"):
                if not nom:
                    st.error("Le nom est obligatoire.")
                elif not ingredients_choisis:
                    st.error("Sélectionnez au moins un ingrédient.")
                else:
                    # Calcul automatique des scores
                    score_m, score_f, score_o, score_l = Plat.calculer_scores(ingredients_choisis)
                    
                    # Sauvegarde du plat
                    p = Plat(
                        nom=nom,
                        scoreMenstruelle=score_m,
                        scoreFolliculaire=score_f,
                        scoreOvulation=score_o,
                        scoreLuteale=score_l,
                        description=description,
                        nbPersonne=nb_personnes,
                        difficulte=difficulte,
                        photoUrl=f"Images/{photo_choisie}"
                        )
                    
                    p.sauvegarder()
                    
                    # Récupération de l'id du plat qu'on vient de créer
                    plats = Plat.get_tous()
                    id_plat = plats[-1][0]
                    
                    # Remplissage de la table Composer
                    for ingredient in ingredients_choisis:
                        c = Composer(id_plat=id_plat, id_ingredient=ingredient[0])
                        c.sauvegarder()
                    
                    st.success(f"Plat '{nom}' ajouté ! Scores calculés : \nMenstruelle : {score_m}\nFolliculaire : {score_f}\nOvulation : {score_o}\nLuteale: {score_l}")

        st.divider()
        st.subheader("Plats existants")
        plats = Plat.get_tous()
        if plats:
            for plat in plats:
                st.write(f"**{plat[1]}** | Difficulté : {plat[8]} | Menstruel : {plat[2]} | Folliculaire : {plat[3]} | Ovulatoire : {plat[4]} | Lutéale : {plat[5]}")
        else:
            st.info("Aucun plat dans la base.")

    ################################################
    ###         GESTION DES UTILISATEURS
    ################################################
    with onglet2:
        st.subheader("Liste des utilisateurs")
        st.info("Les données personnelles sont affichées à des fins d'administration uniquement.")

        conn = __import__('Database').get_connection()
        cur = conn.cursor()
        cur.execute("SELECT Id_utilisateur, nom, prenom, email, estParticulier, dateInscription FROM Utilisateur")
        utilisateurs = cur.fetchall()
        conn.close()

        if utilisateurs:
            for u in utilisateurs:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{u[1]} {u[2]}** — {u[3]} — {'Particulier' if u[4] else 'Professionnel'} — Inscrit le {u[5]}")
                with col2:
                    if st.button("Supprimer", key=f"suppr_{u[0]}"):
                        Utilisateur.supprimer(u[0])
                        st.success("Utilisateur supprimé.")
                        st.rerun()
        else:
            st.info("Aucun utilisateur.")

    ################################################
    ###         GESTION DES ARTICLES/FORUMS
    ################################################
    with onglet3:
        st.subheader("Ajouter un article éducatif")
        forums = Forum.get_tous()

        if not forums:
            st.warning("Aucun forum disponible. Créez d'abord un forum.")
        else:
            with st.form("form_article"):
                forum_choisi = st.selectbox("Forum", options=forums, format_func=lambda f: f[1])
                titre = st.text_input("Titre de l'article")
                contenu = st.text_area("Contenu")

                if st.form_submit_button("Publier l'article"):
                    if titre and contenu:
                        art = Article(
                            titre=titre,
                            description=contenu,
                            id_forum=forum_choisi[0]
                        )
                        art.sauvegarder()
                        st.success("Article publié !")
                    else:
                        st.error("Titre et contenu sont obligatoires.")

        st.divider()
        st.subheader("Créer un forum")
        with st.form("form_forum"):
            titre_forum = st.text_input("Titre du forum")
            desc_forum = st.text_area("Description")
            if st.form_submit_button("Créer le forum"):
                if titre_forum:
                    f = Forum(titre=titre_forum, description=desc_forum)
                    f.sauvegarder()
                    st.success("Forum créé !")
                else:
                    st.error("Le titre est obligatoire.")