
"""
MGPEB - Módulo de Gerenciamento de Pouso e Estabilização de Base

Projeto acadêmico que simula o controle de pouso de módulos em Marte.

Funcionalidades:
- Controle de fila de pouso (FIFO)
- Tratamento de falhas com pilha (LIFO)
- Algoritmos de busca e ordenação
- Lógica de decisão com portas lógicas
- Validação de condições (combustível, clima, sensores, massa, horário)
- Modelagem matemática da altura (queda livre)
"""

fila_pouso = [] # Criando uma fila vazia
pousados = [] #lista de modulos que pousaram 
alertas = [] #lista de alertas
pilha_emergencia = [] #pilha de emergencia 

fila_pouso.append({
    "nome": "Geração de Oxigênio",
      "prioridade": 1,
        "combustivel": 95,
          "massa": 9000,
            "criticidade": "alta",
              "horario": "07:30",
                "area": True,
                  "sensores": True,
                    "clima_ruim": False,
                      "tipo": "vida"
                  
}) # Adicionando um avião à fila

fila_pouso.append({
    "nome": "Suporte Médico",
        "prioridade": 2,
          "combustivel": 90,
            "massa": 7000,
              "criticidade": "alta",
                "horario": "08:00",
                   "area": True,
                     "sensores": True,
                       "clima_ruim": False,
                         "tipo": "vida"
})

fila_pouso.append({
    "nome": "Habitação",
         "prioridade": 3,
           "combustivel": 85,
             "massa": 9600,
               "criticidade": "media",
                 "horario": "08:30",
                   "area": True,
                     "sensores": True,
                       "clima_ruim": False,
                         "tipo": "infraestrutura"
})

fila_pouso.append({
    "nome": "Logística",
        "prioridade": 4,
          "combustivel": 70,
            "massa": 8000,
              "criticidade": "media",
                "horario": "09:00",
                  "area": True,
                    "sensores": True,
                      "clima_ruim": False,
                        "tipo": "infraestrutura"
})

fila_pouso.append({
       "nome": "Energia",
         "prioridade": 5,
           "combustivel": 55,
             "massa": 9000,
               "criticidade": "alta",
                 "horario": "09:30",
                    "area": True,
                      "sensores": True,
                        "clima_ruim": True,
                          "tipo": "infraestrutura"
})

fila_pouso.append({
    "nome": "Comunicações",
        "prioridade": 6,
          "combustivel": 6,
            "massa": 7500,
              "criticidade": "baixa",
                "horario": "10:00",
                  "area": True,
                    "sensores": False,
                      "clima_ruim": False,
                        "tipo": "infraestrutura"
})

#criando algoritmos de busca :)
def buscar_menor_combustivel (lista):
    menor = lista[0]
    for modulo in lista:
        if modulo["combustivel"] < menor["combustivel"]:   #comparação do combustível
            menor = modulo                                 #atualização do menor
    return menor                                   #looping 


def buscar_maior_prioridade(lista):
        maior = lista[0]
        for modulo in lista:
            if modulo["prioridade"] < maior["prioridade"]:
                maior = modulo
        return maior

def buscar_por_tipo(lista, tipo):
    resultado = []
    for modulo in lista:
        if modulo["tipo"] == tipo:
            resultado.append(modulo)
    return resultado


#ordenação
def ordernar_fila(lista):
    return sorted(lista, key=lambda x: x["prioridade"])  #pega o valor usado na comparação 

#função matematica (altura)
def calcular_altura(h0, t, g=3.7):
    return h0 - 0.5 * g * (t ** 2)

#validação do horário
def horario_valido(horario):
    hora = int(horario.split(":")[0]) 
    return 7 <= hora <= 10
  

#falha crítica 
def falha_critica(modulo):
    return modulo["combustivel"] < 20 or not modulo["sensores"]  #vai retornar True se o combustivel estiver baixo ou sensores falharem

#lógica de pouso (Portas lógicas)

def pode_pousar(modulo):
    C = modulo["combustivel"] > 50
    A = modulo["area"]
    S = modulo["sensores"]
    R = modulo["clima_ruim"]
    M = modulo["massa"] < 9500
    H = horario_valido(modulo["horario"])

    T = not R                                    #lógica com not, para deixar o clima como bom
    if C and A and S and T and M and H:          #lógica com and, se tudo for true, vai pousar 
        return True
    elif not C:
        print("Motivo: combustível insuficiente") 
    elif not S:
        print("Motivo: falha dos sensores")
    elif not T:                                  #not de novo para o clima bom ficar ruim
        print("Motivo: clima ruim")
    elif not M:
        print("Motivo: massa muito alta")
    elif not H:
        print("Motivo: fora da janela de pouso")
    else: 
        print("Motivo: área de pouso indisponível")

    return False
        
  #Pilha de  emergência
def tratar_emergencia():
    while pilha_emergencia:
        modulo = pilha_emergencia.pop()          #.pop() para removr o último elemento da pilha
        print(f"corrigindo: {modulo['nome']}")

        modulo ["sensores"] = True               #simulação de correção dos sensores
        modulo ["combustivel"] += 30             #simulação de reabastecimento

        fila_pouso.insert(0, modulo)             #retornando o módulo corrigido para o início da fila de pouso

#execução do programa

fila_pouso = ordernar_fila(fila_pouso)

print ("Maior prioridade:", buscar_maior_prioridade(fila_pouso)["nome"])
print ("Menor combustível:", buscar_menor_combustivel(fila_pouso)["nome"])

#
altura = calcular_altura(1000, 20)
print(f"\nAltura atual: {altura:.2f} metros")


if altura < 200:
    print("Ativar retrofoguetes!!!")

print("\n Inicio dos pousos \n")

while fila_pouso:
    modulo = fila_pouso.pop(0)           

    if falha_critica(modulo):
        print(f"{modulo["nome"]}: Falha crítica detectada!")
        pilha_emergencia.append(modulo)
        continue

    if pode_pousar(modulo):
        print(f"{modulo["nome"]} Pouso autorizado!")
        pousados.append(modulo)
    else:
        print(f"{modulo["nome"]} não pode pousar!")
        alertas.append(modulo)

    tratar_emergencia() 

print("\nPousados:", [m["nome"] for m in pousados])
print("Alertas:", [m["nome"] for m in alertas])