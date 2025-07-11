import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from faker import Faker

fake = Faker('pt_BR')

# Zonas proibidas (lagos e parques)
zonas_proibidas = [
    (-15.7900, -47.8790, 0.002),  # Parque Dona Sarah Kubitschek
    (-15.7890, -47.8940, 0.002),  # Lago Parque das Nações
    (-15.7850, -47.8950, 0.002)   # Lago Sul
]


# Tipos de crime com pesos ajustáveis
tipos_crime = ["furto", "roubo", "homicídio", "tráfico", "vandalismo", "feminicídio"]

# Pesos por região (usado para ajustar tipo de crime)
crime_pesos_por_regiao = {
    "Eixo L Sul": [35, 25, 10, 15, 25, 10],  # Furto e Vandalismo pesam mais
    "W3 Sul": [20, 20, 15, 35, 10, 10],       # Tráfico e Homicídio pesam mais
    "W5 Sul": [10, 15, 35, 30, 10, 10],      # Homicídio e Tráfico pesam mais
    "L2 Sul": [10, 10, 30, 20, 10, 40],      # Homicídio e Feminicídio pesam mais
    "Novo Setor 1": [10, 30, 10, 10, 30, 10]  # Roubo e Vandalismo pesam mais
}

# Setores da Asa Sul (com variação espacial)
# Setores da Asa Sul (com variação espacial)
setores_asa_sul = {
    "Eixo L Sul": [
        (-15.8260, -47.9120),  # Centro do Eixo L Sul
        (-15.8247, -47.9100),  # Próximo ao Clube do Exército
        (-15.8285, -47.9140),  # Região da Praça dos Três Poderes
        (-15.8220, -47.9080)   # Área comercial da Asa Sul
    ],
    "W3 Sul": [
        (-15.817760, -47.913787),  # SQS 314
        (-15.814581, -47.909281),  # SQS 212
        (-15.811360, -47.904775),  # SQS 112
        (-15.806983, -47.899453),  # SQS 108
        (-15.800748, -47.893874),  # SQS 104
        (-15.816951, -47.902616),  # Centro da W3 Sul
        (-15.817344, -47.907337),  # Expansão leste
        (-15.818286, -47.899531)   # Sul da W3 Sul
    ],
    "W5 Sul": [  # Coordenadas aproximadas da W5 Sul
        (-15.8165, -47.9180),  # SQS 304
        (-15.8140, -47.9160),  # SQS 204
        (-15.8120, -47.9140),  # SQS 104
        (-15.8100, -47.9120),  # SQS 102
        (-15.8080, -47.9100),  # SQS 100
        (-15.8150, -47.9150),  # Centro da W5 Sul
        (-15.8130, -47.9170),  # Parte alta da W5 Sul
        (-15.8110, -47.9130)   # Extremidade sul da W5
    ],
    "L2 Sul": [
        (-15.8300, -47.9080),  # Centro da L2 Sul
        (-15.8280, -47.9050),  # Próximo à CLS 208
        (-15.8250, -47.9020),  # Região comercial
        (-15.8220, -47.8990),  # Área residencial
        (-15.821972, -47.920525),  # Centro-norte da L2 Sul
        (-15.831757, -47.921340),  # Extremo norte da L2 Sul
        (-15.824573, -47.925245),   # Nordeste da L2 Sul
        (-15.817510, -47.892228),
        (-15.820010, -47.888692)
    ],
    "Novo Setor 1": [  # Áreas com alta densidade
        (-15.808346, -47.891342),  # Ponto central
        (-15.8100, -47.8950),      # Sudoeste
        (-15.8050, -47.8850),      # Sul
        (-15.804471, -47.891790),  # Sudoeste
        (-15.816681, -47.901966),  # Centro-oeste
        (-15.809755, -47.884687),  # Sul do setor
        (-15.815680, -47.901966),  # Leste do Novo Setor 1
        (-15.826569, -47.926808)
    ]
}
# Mapeamento de tipos de crime → regiões com maior incidência
crimes_regioes_prioritarias = {
    "furto": ["Eixo L Sul"] * 4 + list(setores_asa_sul.keys()),
    "roubo": ["Novo Setor 1"] * 4 + list(setores_asa_sul.keys()),
    "homicídio": ["W3 Sul", "L2 Sul"] * 3 + list(setores_asa_sul.keys()),
    "tráfico": ["W3 Sul", "W5 Sul"] * 5 + list(setores_asa_sul.keys()),
    "vandalismo": ["Eixo L Sul", "Novo Setor 1"] * 3 + list(setores_asa_sul.keys()),
    "feminicídio": ["L2 Sul"] * 6 + list(setores_asa_sul.keys())
}
# Feriados fictícios
feriados = [
    "2020-04-10", "2020-04-12", "2020-04-21", "2020-05-01", "2020-09-07", "2020-10-12", "2020-11-02", "2020-11-15", "2020-12-25",
    "2021-04-02", "2021-04-04", "2021-04-21", "2021-05-01", "2021-09-07", "2021-10-12", "2021-11-02", "2021-11-15", "2021-12-25",
    "2022-04-15", "2022-04-17", "2022-04-21", "2022-05-01", "2022-09-07", "2022-10-12", "2022-11-02", "2022-11-15", "2022-12-25",
    "2023-04-07", "2023-04-09", "2023-04-21", "2023-05-01", "2023-09-07", "2023-10-12", "2023-11-02", "2023-11-15", "203-12-25",
    "2024-03-29", "2024-03-31", "2024-04-21", "2024-05-01", "2024-09-07", "2024-10-12", "2024-11-02", "2024-11-15", "2024-12-25",
    "2025-04-18", "2025-04-20", "2025-04-21", "2025-05-01", "2025-09-07", "2025-10-12", "2025-11-02", "2025-11-15", "2025-12-25"
]

# Dicionário de risco por região
risco_mapa = {
    "W3 Sul": 4,
    "W5 Sul": 4,
    "Eixo L Sul": 2,
    "L2 Sul": 5,
    "Novo Setor 1": 3
}

# Endereços típicos da Asa Sul
enderecos_asa_sul = [
    "{rua} Bloco {bloco}, Ap {num}",
    "{rua} Lote {lote}, Sala {sala}",
    "{rua} Edifício {edificio}, Unidade {unidade}"
]
blocos = ["A", "B", "C", "D"]
lotes = list(range(1, 50))
salas = list(range(100, 300))
edificios = ["Alpha", "Bravo", "Delta", "Omega", "Prime", "Center"]
unidades = list(range(101, 250))

# Função para data/hora noturna
def random_datetime():
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    delta_days = (end - start).days
    hora = int(np.random.normal(loc=23, scale=5)) % 24
    return start + timedelta(
        days=random.randint(0, delta_days),
        hours=hora,
        minutes=random.randint(0, 59)
    )

# Função para gerar variação espacial menor (500m)
def gerar_variacao(lat_base, lon_base):
    lat = lat_base + random.uniform(-0.005, 0.005)  # Menor dispersão
    lon = lon_base + random.uniform(-0.005, 0.005)
    return lat, lon

# Função para gerar idade com base na região e tipo de crime
def gerar_idade(rua, tipo_crime):
    padroes = {
        "W3 Sul": {"idade_min": 14, "idade_max": 25, "crimes": ["tráfico", "homicídio"]},
        "W5 Sul": {"idade_min": 14, "idade_max": 30, "crimes": ["tráfico", "roubo"]},
        "Eixo L Sul": {"idade_min": 50, "idade_max": 70, "crimes": ["furto", "vandalismo"]},
        "L2 Sul": {"idade_min": 20, "idade_max": 40, "crimes": ["homicídio", "roubo"]},
        "Novo Setor 1": {"idade_min": 14, "idade_max": 25, "crimes": ["roubo", "vandalismo"]}
    }
    padrao = padroes.get(rua, {"idade_min": 14, "idade_max": 70})
    if tipo_crime in padrao["crimes"]:
        idade = random.randint(padrao["idade_min"], padrao["idade_max"])
    else:
        if random.random() < 0.4:
            idade = int(np.random.normal(loc=23, scale=5))  # Jovens
        elif random.random() < 0.1:
            idade = int(np.random.normal(loc=65, scale=3))  # Idosos
        else:
            idade = random.randint(9, 90)  # Aleatório
    return min(max(idade, 7), 90)

# Pesos por tipo de dia
pesos_tipos = {
    'dia_normal': [30, 20, 10, 15, 20, 5],
    'final_semana': [25, 20, 15, 20, 15, 5],
    'feriado': [20, 15, 20, 25, 15, 5]
}

# Geração dos dados
num_registros = 30000
data = []
for _ in range(num_registros):
    data_hora = random_datetime()
    data_str = data_hora.strftime('%Y-%m-%d')
    hora = data_hora.hour

    # Tipo de dia
    if data_hora.weekday() in [4, 5]:
        tipo_dia = 'final_semana'
    elif data_str in feriados:
        tipo_dia = 'feriado'
    else:
        tipo_dia = 'dia_normal'

    # Escolher tipo de crime com base no tipo de dia
    base_pesos = pesos_tipos[tipo_dia]
    tipo = random.choices(tipos_crime, weights=base_pesos, k=1)[0]

    # Priorizar região com base no tipo de crime
    regioes_prioritarias = crimes_regioes_prioritarias.get(tipo, list(setores_asa_sul.keys()))
    via_aleatoria = random.choice(regioes_prioritarias)

    # Reforço noturno: aumentar chance de crime em regiões prioritárias
    if 21 <= hora or hora <= 3:
        regioes_prioritarias = crimes_regioes_prioritarias.get(tipo, list(setores_asa_sul.keys())) * 3 + list(setores_asa_sul.keys())
        via_aleatoria = random.choice(regioes_prioritarias)

    # Gerar coordenadas
    lat_base, lon_base = random.choice(setores_asa_sul[via_aleatoria])
    lat, lon = gerar_variacao(lat_base, lon_base)

    # Verificar zonas proibidas
    tentativas = 0
    while tentativas < 10:
        tentativas += 1
        lat_base, lon_base = random.choice(setores_asa_sul[via_aleatoria])
        lat, lon = gerar_variacao(lat_base, lon_base)
        proibido = False
        for (lat_p, lon_p, raio) in zonas_proibidas:
            distancia = ((lat - lat_p)**2 + (lon - lon_p)**2)**0.5
            if distancia < raio:
                proibido = True
                break
        if not proibido:
            break

    # Obter peso da região e ajustar tipo de crime
    regiao_pesos = crime_pesos_por_regiao.get(via_aleatoria, [1] * 6)
    combined_pesos = [b * r for b, r in zip(base_pesos, regiao_pesos)]
    tipo = random.choices(tipos_crime, weights=combined_pesos, k=1)[0]

    # Gerar idade
    idade = gerar_idade(via_aleatoria, tipo)

    # Gerar endereço
    formato = random.choice(enderecos_asa_sul)
    if "{bloco}" in formato:
        endereco = formato.format(rua=via_aleatoria, bloco=random.choice(blocos), num=random.randint(100, 999))
    elif "{lote}" in formato:
        endereco = formato.format(rua=via_aleatoria, lote=random.choice(lotes), sala=random.choice(salas))
    elif "{edificio}" in formato:
        endereco = formato.format(rua=via_aleatoria, edificio=random.choice(edificios), unidade=random.choice(unidades))

    # Gerar outros dados
    nome = fake.name()
    cpf_formatado = fake.cpf()
    email = fake.email()
    telefone = fake.phone_number()

    # Inserir NaN esporadicamente
    if random.random() < 0.03: nome = np.nan
    if random.random() < 0.08: idade = np.nan
    if random.random() < 0.01: tipo = np.nan
    if random.random() < 0.2: email = np.nan
    if random.random() < 0.07: telefone = np.nan
    if random.random() < 0.09: endereco = np.nan

    risco = risco_mapa.get(via_aleatoria, 2)

    data.append({
        'latitude': lat,
        'longitude': lon,
        'data': data_str,
        'hora': data_hora.strftime('%H:%M'),
        'tipo_crime': tipo,
        'bairro': 'Asa Sul',
        'rua': via_aleatoria,
        'tipo_dia': tipo_dia,
        'ano': data_hora.year,
        'nome': nome,
        'cpf': cpf_formatado,
        'idade': idade,
        'email': email,
        'telefone': telefone,
        'endereco': endereco,
        'risco': risco
    })

# Criar DataFrame e salvar CSV
df = pd.DataFrame(data)
df["__ERRO__"] = "ERRO_404"
df["null"] = np.nan
df.to_csv('crime_segunda_area.csv', index=False)
print("✅ Arquivo 'crime_segunda_area.csv' criado com sucesso!")