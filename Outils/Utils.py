from datetime import date

# Correspondance mois -> numéro
MOIS = {
    "Jan": 1, "Fév": 2, "Mars": 3, "Avr": 4, "Mai": 5, "Juin": 6,
    "Juil": 7, "Août": 8, "Sept": 9, "Oct": 10, "Nov": 11, "Déc": 12
}

def ingredient_de_saison(saison_str):
    """Retourne True si l'ingrédient est de saison ce mois-ci."""
    #print("\n------------------\nSaison : ",saison_str)
    if not saison_str or saison_str.strip() in ["Toute l'année", "/", ""]:
        #print("IF NOT") 
        return True

    mois_actuel = date.today().month

    try:
        parties = saison_str.replace(" ", "").split("-")
        debut = MOIS.get(parties[0], None)
        fin = MOIS.get(parties[1], None)
        #print("Mois actuel : ",mois_actuel)
        #print("Début : ",debut," et Fin : ",fin)

        if debut is None or fin is None:
            #print("(1 None) true")
            return True  # Si on ne sait pas, on considère disponible

        if debut <= fin:
            # Ex: Mars–Nov (pas de chevauchement d'année)
            #print("debut <= fin : ",debut <= mois_actuel <= fin)
            return debut <= mois_actuel <= fin
        else:
            # Ex: Sept–Mars (chevauche janvier)
            #print("debut > fin : ",mois_actuel <= debut or mois_actuel >= fin)
            return mois_actuel <= debut or mois_actuel >= fin

    except Exception:
        #print("Except")
        return True