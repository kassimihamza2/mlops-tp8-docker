import sys
import time
import requests

URL = "http://fraude-api"

duree = int(sys.argv[1]) if len(sys.argv) > 1 else 10

transaction = {
    "montant": 1800,
    "anciennete": 30,
    "freq_24h": 4,
    "nuit": 1
}

print("Verification de l'API :")

try:
    print(requests.get(f"{URL}/health", timeout=5).json())
except requests.RequestException as e:
    print(f"Erreur health : {e}")

print("\nPredictions :")
fin = time.time() + duree

while time.time() < fin:
    try:
        reponse = requests.post(
            f"{URL}/predict",
            json=transaction,
            timeout=5
        )
        print(reponse.json())
    except requests.RequestException as e:
        print(f"Erreur : {e}")

    time.sleep(1)
