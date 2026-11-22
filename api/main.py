import os
import socket

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API de d?tection de fraude")

HOTE = socket.gethostname()
VERSION = "1.0"

modele = joblib.load("models/model.pkl")

class Transaction(BaseModel):
    montant: float
    anciennete: int
    freq_24h: int
    nuit: int


@app.get("/health")
def health():
    return {
        "status": "OK",
        "version": VERSION,
        "hote": HOTE
    }


@app.post("/predict")
def predict(transaction: Transaction):
    donnees = pd.DataFrame([transaction.model_dump()])
    probabilite = float(modele.predict_proba(donnees)[0, 1])

    return {
        "fraude": probabilite > 0.5,
        "probabilite": round(probabilite, 4),
        "version": VERSION,
        "hote": HOTE
    }

