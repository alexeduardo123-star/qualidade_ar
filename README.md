# Monitoramento da Qualidade do Ar
## Integração MongoDB + Redis com Python

Trabalho prático da disciplina **Bancos de Dados e Novas Tecnologias**, da Universidade Comunitária da Região de Chapecó (Unochapecó).

### Integrantes

- Lucas William Albertti
- Alex Eduardo Paweukievicz
- Gabriel Augusto Braatz
- Vinicius Henrich Mai

### Objetivo

Desenvolver um protótipo de monitoramento da qualidade do ar utilizando MongoDB para armazenar sensores e medições históricas, Python para consultar e agregar dados e Redis para armazenar resumos recentes em estruturas Hash.

### Tecnologias utilizadas

- Python
- MongoDB
- Redis

### Estrutura do projeto

- `codigo/`: scripts Python e arquivos de apoio ao protótipo.
- `documentacao/`: relatório técnico desenvolvido na Etapa I.

### Scripts do projeto

| Arquivo | Descrição |
|---|---|
| `conexao.py` | Configuração das conexões com MongoDB e Redis. |
| `1_popular_mongo.py` | Cadastro dos sensores e geração de medições históricas. |
| `2_consultar_mongo.py` | Consulta de medições por sensor e intervalo de tempo. |
| `3_resumos_redis.py` | Agregação de medições e armazenamento de resumos no Redis. |
| `4_ler_redis.py` | Leitura dos resumos armazenados no Redis. |

### Execução

Os scripts exigem Python, MongoDB e Redis configurados e em execução.

Consulte o arquivo `requirements.txt` e as configurações em `codigo/conexao.py` antes de executar os programas.