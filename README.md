# Qualidade do Ar — MongoDB + Redis + Python (versão simplificada)

Pré-requisitos: Python, MongoDB e Redis rodando no Windows.

```powershell
python -m pip install -r requirements.txt
python 1_popular_mongo.py      # sensores + 1.728 medições + índice
python 2_consultar_mongo.py    # medições de um sensor num intervalo
python 3_resumos_redis.py      # agregação no MongoDB -> Hashes no Redis
python 4_ler_redis.py          # lê os resumos do Redis
```

| Arquivo | Etapa da arquitetura |
|---|---|
| conexao.py | Conexão com MongoDB e Redis |
| 1_popular_mongo.py | Simulador → MongoDB (Sensores e Medicoes) |
| 2_consultar_mongo.py | Consulta ao histórico no MongoDB |
| 3_resumos_redis.py | Programa de agregação → Redis (Hashes) |
| 4_ler_redis.py | Consulta rápida aos resumos no Redis |

Horários em UTC.
