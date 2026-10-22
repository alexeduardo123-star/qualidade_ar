# 2_consultar_mongo.py
# Consulta as medições de um sensor dentro de um intervalo de tempo (UTC).

from datetime import datetime
from conexao import db

sensor = input("Sensor (ex: S001): ").strip().upper()
inicio = datetime.strptime(input("Início (ex: 2026-10-20 10:00): "), "%Y-%m-%d %H:%M")
fim = datetime.strptime(input("Fim    (ex: 2026-10-20 11:00): "), "%Y-%m-%d %H:%M")

# Mesmo filtro que se usa no Compass / mongosh
filtro = {"sensor_id": sensor, "timestamp": {"$gte": inicio, "$lt": fim}}

print()
for m in db.Medicoes.find(filtro).sort("timestamp", 1):
    print(m["timestamp"].strftime("%d/%m %H:%M"),
          "| PM2.5:", m["pm25"], "| PM10:", m["pm10"], "| CO2:", m["co2"],
          "| Temp:", m["temperatura"], "| Umid:", m["umidade"])

print("\nTotal:", db.Medicoes.count_documents(filtro), "medições")
