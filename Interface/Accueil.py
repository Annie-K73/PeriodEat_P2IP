import streamlit as st
from Models.Anamnese import Anamnese
from Models.Plat import Plat
from Models.Vendre import Vendre

def afficher():
    st.title("🏠 Accueil")

    utilisateur = st.session_state.utilisateur
    id_utilisateur = utilisateur[0]
    estProfessionnel = utilisateur[6]
    estParticulier = utilisateur[5]
    anamnese = Anamnese.get_par_utilisateur(id_utilisateur)

    if(estParticulier):
        if not anamnese:
            st.info("Bienvenue ! Renseignez votre cycle dans 'Mon profil' pour obtenir des recommandations personnalisées.")
            return

        phase = anamnese[4]

        phases_info = {
            "menstruelle": {
                "titre": "Phase menstruelle",
                "description": "Votre corps perd du fer. Privilégiez les aliments riches en fer et en magnésium.",
                "conseils": ["Restez hydratée", "Évitez le café", "Favorisez le repos"]
            },
            "folliculaire": {
                "titre": "Phase folliculaire",
                "description": "Votre énergie remonte ! C'est le moment idéal pour les protéines et les légumes verts.",
                "conseils": ["Augmentez les protéines", "Consommez des légumes verts", "Bonne période pour le sport"]
            },
            "ovulation": {
                "titre": "Phase ovulatoire",
                "description": "Pic hormonal. Privilégiez les antioxydants et le zinc.",
                "conseils": ["Mangez des fruits frais", "Favorisez les antioxydants", "Hydratez-vous bien"]
            },
            "luteale": {
                "titre": "Phase lutéale",
                "description": "Baisse d'énergie possible. Favorisez les aliments à faible indice glycémique.",
                "conseils": ["Évitez le sucre raffiné", "Privilégiez les glucides lents", "Limitez le sel"]
            }
        }

        info = phases_info.get(phase, None)

        if info:
            st.subheader(f"{info['titre']}")
            st.write(info["description"])
            st.divider()

            st.subheader("Conseils du moment")
            for conseil in info["conseils"]:
                st.write(f"• {conseil}")

            st.divider()
            st.subheader("Recettes recommandées pour vous")
            plats = Plat.get_par_phase(phase)[:3]

            if plats:
                cols = st.columns(len(plats))
                for col, plat in zip(cols, plats):
                    with col:
                        st.subheader(plat[1])
                        if plat[9] and plat[9] != "":
                            try:
                                st.image(plat[9], width="stretch")
                            except:
                                pass
                        st.write(plat[6])
                        st.caption(f"{plat[7]} personnes | {plat[8]}")
            else:
                st.info("Aucune recette disponible pour le moment.")
        else:
            st.warning("Phase non reconnue. Mettez à jour votre profil.")

    elif(estProfessionnel):
        produits = Vendre.get_tous_par_id_vendeur(id_utilisateur)
        if not produits:
            st.info("Bienvenue ! Renseignez l'ensemble de vos produits dans 'Mon profil' pour être mis en avant auprès des utilisateurs.")
            return
        
        commerce_info = {"commerce" : {
                "titre": "Règles à appliquer : mise en avant de vos produits",
                "description": "PeriodEat permet de mettre en avant les commerces locaux avec des utilisateurs soucieux de leur alimentation.",
                "conseils": ["Renseignez bien chacun de vos produits", "Mettez à jour votre compte régulièrement", "Restez bienveillants avec les utilisateurs"]
            }}
        
        info = commerce_info.get("commerce",None)

        if(info):
            st.subheader(f"{info['titre']}")
            st.write(info["description"])
            st.divider()

            st.subheader("Conseils du moment")
            for conseil in info["conseils"]:
                st.write(f"• {conseil}")
        else:
            st.info("Aucune information disponible pour le moment.")


