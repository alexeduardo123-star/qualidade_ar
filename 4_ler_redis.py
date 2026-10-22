# 4_ler_redis.py
# Lê os últimos resumos direto do Redis (sem acessar o MongoDB).

from conexao import r

chaves = sorted(r.keys("qualidadear:*"))

if not chaves:
    print("Nenhum resumo no Redis. Rode primeiro o 3_resumos_redis.py")

for chave in chaves:
    print("\nHGETALL", chave)
    for campo, valor in r.hgetall(chave).items():
        print(f"   {campo}: {valor}")
