import os 
import time

def obter_numero_inteiro(label: str):
    entrada = input(label)

    try:
        numero = int(entrada)
        return numero
    
    except ValueError:
        print(f'"{entrada}" não é uma inteiro válido!')
        return obter_numero_inteiro(label)


def obter_numero_minimo(label: str, min: int):
    numero = obter_numero_inteiro(label)

    while numero < min:
        print(f'Quantidade Fora da faixa mínima!')
        numero = obter_numero_minimo(label, min)

    return numero


def obter_numero_faixa(label: str, min: int, max: int):
    numero = obter_numero_inteiro(label)

    while numero < min or numero > max:
        print(f'O número {numero} está fora da faixa!')
        numero = obter_numero_faixa(label, min, max)

    return numero


def tempinho(tempo: float):
    time.sleep(tempo)


def cls():
    os.system('clear')


def espaco():
    print('')


