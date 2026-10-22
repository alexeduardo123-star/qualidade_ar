# conexao.py
# Conexões com o MongoDB e o Redis (usadas por todos os outros arquivos)

from pymongo import MongoClient
import redis

# MongoDB: banco QualidadeAr
mongo = MongoClient("mongodb://127.0.0.1:27017")
db = mongo["QualidadeAr"]

# Redis: decode_responses=True devolve texto em vez de bytes
# protocol=2 é necessário porque o Redis para Windows é a versão 5
r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True, protocol=2)
