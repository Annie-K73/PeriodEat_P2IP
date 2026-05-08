import csv
from Database import init_db
from Models.Ingredient import Ingredient


# Initialisation de la base de données
init_db()

def import_aliments():
    # Lecture du CSV
    with open('aliments_cycle.csv', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        df = list(csv_reader)

    print(f"=== Import de {len(df)} aliments ===\n")

    for row in df:
        try:
            i = Ingredient(
                nom=row['Aliment'],
                estSaisonnier=row['Saison FR'] != "Toute l'année",
                saison=row['Saison FR'],
                scoreMenstruelle=int(row['Menstruation']),
                scoreFolliculaire=int(row['Folliculaire']),
                scoreOvulation=int(row['Ovulatoire']),
                scoreLuteale=int(row['Lutéale'])
            )
            i.sauvegarder()
            print(f"✓ {row['Aliment']} importé")
        except Exception as e:
            print(f"✗ Erreur sur {row['Aliment']} : {e}")

    print("\n=== Import terminé ! ===")