import os
import time


def obter_numero_inteiro(label: str):
    entrada = input(label)

    try:
        numero = int(entrada)
    except ValueError:
        print(f'O número digitado {entrada} não é um inteiro válido!')
        numero = obter_numero_inteiro(label)

    return numero


def obter_numero_da_faixa(label: str, min: int,max: int):
    numero = obter_numero_inteiro(label)

    while numero < min or numero > max:
        print(f'Número fora da faixa {min} minimo {max} maximo')
        numero = obter_numero_da_faixa(label, min, max)

    return numero


def cls():
    os.system('cls')


def espaco():
    print('')


def tempinho(tempo: float):
    time.sleep(tempo)