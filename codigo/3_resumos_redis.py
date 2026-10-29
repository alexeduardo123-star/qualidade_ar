# 3_resumos_redis.py
# Calcula o resumo de uma hora no MongoDB (pipeline de agregação)
# por sensor e por cidade, e grava o resultado em Hashes no Redis.

import unicodedata
from datetime import datetime, timedelta
from conexao import db, r

hora = input("Hora do resumo (ex: 2026-10-20 10): ")
inicio = datetime.strptime(hora, "%Y-%m-%d %H")
fim = inicio + timedelta(hours=1)

# Cálculos usados nos dois $group
calculos = {
    "qt_medicoes": {"$sum": 1},
    "pm25_media": {"$avg": "$pm25"},
    "pm10_media": {"$avg": "$pm10"},
    "co2_media": {"$avg": "$co2"},
    "temperatura_media": {"$avg": "$temperatura"},
    "umidade_media": {"$avg": "$umidade"},
    "pm25_max": {"$max": "$pm25"},
    "pm10_max": {"$max": "$pm10"},
}

# $project: arredonda as médias para 1 casa decimal
arredondar = {
    "qt_medicoes": 1, "pm25_max": 1, "pm10_max": 1,
    "pm25_media": {"$round": ["$pm25_media", 1]},
    "pm10_media": {"$round": ["$pm10_media", 1]},
    "co2_media": {"$round": ["$co2_media", 1]},
    "temperatura_media": {"$round": ["$temperatura_media", 1]},
    "umidade_media": {"$round": ["$umidade_media", 1]},
}

periodo = {
    "inicio_periodo": inicio.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "fim_periodo": fim.strftime("%Y-%m-%dT%H:%M:%SZ"),
}


def sem_acento(texto):
    """Chapecó -> chapeco"""
    return unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()


# ---------- Resumo por SENSOR ----------
por_sensor = db.Medicoes.aggregate([
    {"$match": {"timestamp": {"$gte": inicio, "$lt": fim}}},
    {"$group": {"_id": "$sensor_id", **calculos}},
    {"$project": arredondar},
    {"$sort": {"_id": 1}},
])

print("\n=== Resumo por sensor ===")
for resumo in por_sensor:
    sensor_id = resumo.pop("_id")
    chave = f"qualidadear:sensor:{sensor_id}"
    r.hset(chave, mapping={**periodo, **resumo})
    print(chave, resumo)

# ---------- Resumo por CIDADE ----------
# $lookup liga cada medição ao seu sensor para descobrir a cidade
por_cidade = db.Medicoes.aggregate([
    {"$match": {"timestamp": {"$gte": inicio, "$lt": fim}}},
    {"$lookup": {"from": "Sensores", "localField": "sensor_id",
                 "foreignField": "_id", "as": "sensor"}},
    {"$unwind": "$sensor"},
    {"$group": {"_id": {"uf": "$sensor.localizacao.uf",
                        "cidade": "$sensor.localizacao.cidade"}, **calculos}},
    {"$project": arredondar},
    {"$sort": {"_id.cidade": 1}},
])

print("\n=== Resumo por cidade ===")
for resumo in por_cidade:
    local = resumo.pop("_id")
    chave = f"qualidadear:cidade:{local['uf']}:{sem_acento(local['cidade'])}"
    r.hset(chave, mapping={**periodo, **resumo})
    print(chave, resumo)

print(f"\nResumos de {periodo['inicio_periodo']} a {periodo['fim_periodo']} gravados no Redis.")
