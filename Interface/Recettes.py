import streamlit as st
from Models.Plat import Plat
from Models.Ingredient import Ingredient
from Models.Avis import Avis

def afficher():
    st.title("🍽️ Recettes")

    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        phase_filtre = st.selectbox("Filtrer par phase", [
            "Toutes", "menstruelle", "folliculaire", "ovulation", "luteale"
        ])
    with col2:
        difficulte_filtre = st.selectbox("Filtrer par difficulté", [
            "Toutes", "facile", "moyen", "difficile"
        ])

    st.divider()

    # Récupération des plats
    if phase_filtre == "Toutes":
        plats = Plat.get_tous()
    else:
        plats = Plat.get_par_phase(phase_filtre)

    # Filtrage par difficulté
    if difficulte_filtre != "Toutes":
        plats = [p for p in plats if p[8] == difficulte_filtre]

    if not plats:
        st.info("Aucune recette trouvée.")
        return

    # Affichage des plats
    for plat in plats:
        with st.expander(f"🍴 {plat[1]} — Difficulté : {plat[8]} | {plat[7]} personnes"):
            col1, col2 = st.columns([1, 2])
            with col1:
                if plat[9] and plat[9] != "":
                    try:
                        st.image(plat[9], width="stretch")
                    except:
                        st.write("📷 Image non disponible")
            with col2:
                st.write(plat[6])
                st.write(f"**Scores par phase :**")
                st.write(f"\tMenstruelle : {plat[2]}/10")
                st.write(f"\tFolliculaire : {plat[3]}/10")
                st.write(f"\tOvulatoire : {plat[4]}/10")
                st.write(f"\tLutéale : {plat[5]}/10")

            # Ingrédients
            ingredients = Ingredient.get_par_plat(plat[0])
            if ingredients:
                st.write("**Ingrédients :**")
                st.write(", ".join([i[1] for i in ingredients]))

            # Avis
            avis = Avis.get_par_plat(plat[0])
            if avis:
                st.write(f"**Avis ({len(avis)}) :**")
                for av in avis:
                    st.write(f"⭐ {av[2]}/5 — {av[1]}")