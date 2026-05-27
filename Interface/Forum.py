import streamlit as st
from Models.Forum import Forum
from Models.Article import Article
from Models.Avis import Avis
from Models.Plat import Plat
from Models.Message import Message

def afficher():
    st.title("💬 Forum")

    forums = Forum.get_tous()
    if not forums:
        st.info("Aucun forum disponible.")
        return

    id_utilisateur = st.session_state.utilisateur[0]

    onglets = st.tabs([f[1] for f in forums])

    for onglet, forum in zip(onglets, forums):
        with onglet:
            id_forum = forum[0]
            st.write(forum[2])
            st.divider()

            # Articles éducatifs
            st.subheader("Articles éducatifs")
            articles = Article.get_par_forum(id_forum)
            if articles:
                for article in articles:
                    with st.expander(article[1]):
                        st.write(article[2])
                        st.caption(f"Publié le {article[3]}")
            else:
                st.info("Aucun article pour le moment.")

            st.divider()

            # Avis
            st.subheader("Avis des utilisatrices")
            avis_liste = Avis.get_par_forum(id_forum)
            if avis_liste:
                for av in avis_liste:
                    if av[5] is None:  # message libre (pas de plat)
                        st.write(f"💬 {av[1]}")
                    else:
                        st.write(f"⭐ {av[2]}/5 — {av[1]}")
                    st.caption(f"Publié le {av[3]}")
            else:
                st.info("Aucun avis pour le moment.")

            st.divider()

            # Affichage des messages libres
            #print("ID Forum : ",id_forum) 
            st.subheader("Messages de la communauté")
            messages = Message.get_par_forum(id_forum)
            if messages:
                for msg in messages:
                    st.write(f"💬 {msg[1]}")
                    st.caption(f"Publié le {msg[2]}")
            else:
                st.info("Aucun message pour le moment.")

            st.divider()
        
            # Poster un message
            st.subheader("Poster un message")
            type_message = st.radio(
                "Type de message",
                ["💬 Message libre", "⭐ Avis sur un plat"],
                key=f"type_{id_forum}"
            )

            if type_message == "⭐ Avis sur un plat":
                plats = Plat.get_tous()
                if plats:
                    plat_choisi = st.selectbox(
                        "Sur quel plat ?",
                        options=plats,
                        format_func=lambda p: p[1],
                        key=f"plat_{id_forum}"
                    )
                    note = st.slider("Note", 1, 5, 3, key=f"note_{id_forum}")
                    commentaire = st.text_area("Commentaire", key=f"commentaire_{id_forum}")

                    if st.button("Publier", key=f"publier_{id_forum}"):
                        if commentaire:
                            av = Avis(
                                commentaire=commentaire,
                                note=note,
                                id_forum=id_forum,
                                id_plat=plat_choisi[0],
                                id_utilisateur=id_utilisateur
                            )
                            av.sauvegarder()
                            st.success("Avis publié !")
                            st.rerun()
                        else:
                            st.error("Veuillez écrire un commentaire.")

            else:  # Message libre

                commentaire_libre = st.text_area("Votre message", key=f"libre_{id_forum}")
                if st.button("Publier", key=f"publier_libre_{id_forum}"):
                    if commentaire_libre:
                        msg = Message(
                            contenu=commentaire_libre,
                            id_forum=id_forum,
                            id_utilisateur=id_utilisateur
                        )
                        msg.sauvegarder()
                        st.success("Message publié !")
                        st.rerun()
                    else:
                        st.error("Veuillez écrire un message.") 