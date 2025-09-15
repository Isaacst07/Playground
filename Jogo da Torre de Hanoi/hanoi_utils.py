import random
import utils as u
import json
import copy
import os


def menu():

    RESET = "\033[0m"
    BRANCO = "\033[97m"

    print(f"{BRANCO}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{BRANCO}║                🎮 NÍVEL DO JOGO 🎮               ║{RESET}")
    print(f"{BRANCO}╠══════════════════════════════════════════════════╣{RESET}")
    print(f"{BRANCO}║ 1️⃣  Nível 1 (Normal)        → 🙂                 ║{RESET}")
    print(f"{BRANCO}║ 2️⃣  Nível 2 (Intermediário) → 🏹                 ║{RESET}")
    print(f"{BRANCO}║ 3️⃣  Nível 3 (Avançado)      → 💀                 ║{RESET}")
    print(f"{BRANCO}║ 4️⃣  Por que não passar este trabalho? ❓         ║{RESET}")
    print(f"{BRANCO}╠══════════════════════════════════════════════════╣{RESET}")
    print(f"{BRANCO}║ 0️⃣  Encerrar o jogo ❌                           ║{RESET}")
    print(f"{BRANCO}╚══════════════════════════════════════════════════╝{RESET}")

    u.espaco()

    nivel = u.obter_numero_da_faixa('>>> ', 0, 4)

    u.cls()

    return nivel


def iniciar_jogo(nivel: int):
    torres = {'R': [], 'G': [], 'B': []}
    lista_cores = ['R', 'G', 'B']

    if nivel == 1:
        torres['R'] = preencher_torre(6, lista_cores, 6) + ['R', 'G', 'B']
        torres['G'] = preencher_torre(0, lista_cores, 9)     # ou ['-'] * 9
        torres['B'] = preencher_torre(0, lista_cores, 9)     # ou ['-'] * 9

        random.shuffle(torres['R'])

    elif nivel == 2:
        torres['R'] = preencher_torre(6, lista_cores, 9)
        torres['G'] = preencher_torre(6, lista_cores, 9)
        torres['B'] = preencher_torre(0, lista_cores, 9) # ou ['-'] * 9 

    elif nivel == 3:
        cores_repetidas = [cor for cor in lista_cores for _ in range(3)]

        torres['R'] = preencher_torre(8, copy.deepcopy(cores_repetidas), 9)
        torres['G'] = preencher_torre(8, copy.deepcopy(cores_repetidas), 9)
        torres['B'] = preencher_torre(8, copy.deepcopy(cores_repetidas), 9)

    elif nivel == 4:
        print("Você não deve passar essa tarefa, pois ela causa tristeza em quem faz (eu)!")
        print("REFLITA SOBRE A FRASE: Índios e Veganos confusos maltratam novatos inocentes e incríveis!")
        u.espaco()
        input('Enter to continue...')

    return torres


def preencher_torre(qtd_cores, cores_base, total):
    torre = []

    for i in range(total):

        if i < qtd_cores:
            index = random.randint(0, len(cores_base) - 1)
            torre.append(cores_base[index])

            if len(cores_base) - 1 > 3:
                cores_base.pop(index)
        else:
            torre.append('-')
            
    return torre


def jogar_partida(nome_jogador, torres, jogador):
    movimentos = 0

    while not acabou(torres):
        u.cls()
        if jogador == 1:
            print(f'JOGADOR {jogador}: {nome_jogador}')

        u.espaco()
       
        print(f'\033[{35}m ========================\033[{37}m TORRE DE HANOI\33[{35}m ========================\033[0m')
        u.espaco()

        mostrar_torres(torres)
        u.espaco()

        movimento = input("Qual a sua jogada (Ex: RG): ")

        if validar_jogada(movimento):
            torres = mover(torres, movimento[0].upper(), movimento[1].upper())
            movimentos += 1
        else:
            print(f"O movimento {movimento} é inválido!")
            input("Enter para continuar...")

    return movimentos


def mostrar_torres(torres):
    torre_r = 'TORRE R'
    torre_g = 'TORRE G'
    torre_b = 'TORRE B'
    tracos = '---------'

    for a, b, c in zip(reversed(torres['R']), reversed(torres['G']), reversed(torres['B'])):
        print(f'           {a:<20}{b:<20}{c:<20}')

    print(f'      \033[{31}m {tracos}\033[0m          \033[{32}m {tracos}\033[0m          \033[{34}m {tracos}\033[0m')
    print(f'       \033[{31}m {torre_r}\033[0m            \033[{32}m {torre_g}\033[0m            \033[{34}m {torre_b}\033[0m')


def mover(torres, origem, destino):

    for i in range(0, len(torres[f'{destino}'])):  # percorre de cima para baixo

        if torres[f'{destino}'][i] == '-':  # achou espaço vazio

            for n in range(len(torres[origem]) - 1, -1, -1):  # pega peça da origem

                if torres[f'{origem}'][n] != '-':

                    torres[f'{destino}'][i] = torres[f'{origem}'][n]
                    torres[f'{origem}'][n] = '-'

                    return torres
    return torres
                

def acabou(torres):
    status_torre_r = status_torre(torres, 'R')
    status_torre_g = status_torre(torres, 'G')
    status_torre_b = status_torre(torres, 'B')

    return status_torre_r and status_torre_b and status_torre_g


def status_torre(torres, cor):
    status = True

    for elemento in torres[f'{cor}']:
        if elemento != cor and elemento != '-':
            status = False
            break

    return status


def validar_jogada(jogada: str) -> bool:
    movimentos = ['RG', 'RB', 'GR', 'GB', 'BR', 'BG']

    if jogada.upper() in movimentos:
        return True 
    else:
        return False


def ganhador(jogador1, jogador2):

    if jogador1 < jogador2:
        print(f'Jogador 1 é o ganhador com {jogador1} jogadas!')
        return jogador1
    elif jogador2 < jogador1:
        print(f'O jogador 2 é o ganhador com {jogador2} jogadas!')
        return jogador2
    else:
        print(f'Os jogadores empataram com {jogador1} jogadas cada!')
        return 'Empate'


def salvar(jogador1, movimentos_1, jogador2, movimento_2, vencedor, configuracoes_iniciais):
    nome_arquivo = "partidas_hanoi_rgb.json"

    dados_partida = {
    "nome_do_jogo": "Hanoi RGB",

    "jogadores": [{
        "nome_do_jogador": jogador1,
        "jogadas": movimentos_1,
        "configurações_iniciais": configuracoes_iniciais,
    }, 
    {   
        "nome_do_jogador": jogador2,
        "jogadas": movimento_2,
        "configurações_iniciais": configuracoes_iniciais,
    }],
    "ganhador": vencedor
}
    
    #encoding garante que python leia corretamente caracteres Unicode (acentos, ç, etc);
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = []  # se o arquivo estiver vazio/corrompido
    else:
        dados = []

# 2. Adicionar o novo dado
    dados.append(dados_partida)

# 3. Sobrescrever o arquivo com os dados antigos + novos
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)