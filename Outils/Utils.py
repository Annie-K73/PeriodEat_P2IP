from datetime import date

# Correspondance mois -> numéro
MOIS = {
    "Jan": 1, "Fév": 2, "Mar": 3, "Avr": 4, "Mai": 5, "Juin": 6,
    "Juil": 7, "Août": 8, "Sept": 9, "Oct": 10, "Nov": 11, "Déc": 12
}

def ingredient_de_saison(saison_str):
    """Retourne True si l'ingrédient est de saison ce mois-ci."""
    if not saison_str or saison_str.strip() in ["Toute l'année", "/", ""]:
        return True

    mois_actuel = date.today().month

    try:
        parties = saison_str.replace(" ", "").split("–")
        debut = MOIS.get(parties[0], None)
        fin = MOIS.get(parties[1], None)

        if debut is None or fin is None:
            return True  # Si on ne sait pas, on considère disponible

        if debut <= fin:
            # Ex: Mars–Nov (pas de chevauchement d'année)
            return debut <= mois_actuel <= fin
        else:
            # Ex: Sept–Mars (chevauche janvier)
            return mois_actuel >= debut or mois_actuel <= fin

    except Exception:
        return True