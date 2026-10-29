# 1_popular_mongo.py
# Cadastra 6 sensores (3 cidades) e gera 24 h de medições a cada 5 minutos.
# 6 sensores x 288 medições = 1.728 documentos.

import random
from datetime import datetime, timedelta
from conexao import db

GRANDEZAS = ["PM2.5", "PM10", "CO2", "temperatura", "umidade"]

# ---------- 1. Sensores ----------
sensores = [
    {"_id": "S001", "modelo": "AirMonitor-200", "descricao": "Sensor ambiental do centro",
     "localizacao": {"cidade": "Chapecó", "uf": "SC", "latitude": -27.1009, "longitude": -52.6157},
     "ativo": True, "grandezas": GRANDEZAS},
    {"_id": "S002", "modelo": "AirMonitor-200", "descricao": "Sensor ambiental da zona norte",
     "localizacao": {"cidade": "Chapecó", "uf": "SC", "latitude": -27.0748, "longitude": -52.6240},
     "ativo": True, "grandezas": GRANDEZAS},
    {"_id": "S003", "modelo": "AirMonitor-200", "descricao": "Sensor ambiental do centro",
     "localizacao": {"cidade": "Xanxerê", "uf": "SC", "latitude": -26.8747, "longitude": -52.4036},
     "ativo": True, "grandezas": GRANDEZAS},
    {"_id": "S004", "modelo": "AirMonitor-200", "descricao": "Sensor ambiental industrial",
     "localizacao": {"cidade": "Xanxerê", "uf": "SC", "latitude": -26.8890, "longitude": -52.3950},
     "ativo": True, "grandezas": GRANDEZAS},
    {"_id": "S005", "modelo": "AirMonitor-200", "descricao": "Sensor ambiental do centro",
     "localizacao": {"cidade": "Concórdia", "uf": "SC", "latitude": -27.2335, "longitude": -52.0278},
     "ativo": True, "grandezas": GRANDEZAS},
    {"_id": "S006", "modelo": "AirMonitor-200", "descricao": "Sensor ambiental do bairro industrial",
     "localizacao": {"cidade": "Concórdia", "uf": "SC", "latitude": -27.2450, "longitude": -52.0150},
     "ativo": True, "grandezas": GRANDEZAS},
]

db.Sensores.delete_many({})          # limpa para poder rodar de novo
db.Sensores.insert_many(sensores)
print(db.Sensores.count_documents({}), "sensores cadastrados")

# ---------- 2. Medições (simulador) ----------
random.seed(1)                        # gera sempre os mesmos números
inicio = datetime(2026, 10, 20, 0, 0) # 20/10/2026 00:00 (UTC)

medicoes = []
for sensor in sensores:
    for i in range(288):              # 24 h x 12 medições por hora
        medicoes.append({
            "sensor_id": sensor["_id"],
            "timestamp": inicio + timedelta(minutes=5 * i),
            "pm25": round(random.uniform(10, 40), 1),
            "pm10": round(random.uniform(20, 80), 1),
            "co2": random.randint(400, 650),
            "temperatura": round(random.uniform(18, 28), 1),
            "umidade": random.randint(50, 85),
        })

db.Medicoes.delete_many({})
db.Medicoes.insert_many(medicoes)

# Índice para buscar rápido por sensor + período
db.Medicoes.create_index([("sensor_id", 1), ("timestamp", -1)])

print(db.Medicoes.count_documents({}), "medições inseridas")
