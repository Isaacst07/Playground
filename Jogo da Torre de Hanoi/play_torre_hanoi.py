# Link do colab com a documentação do código: https://colab.research.google.com/drive/1B65e55RXn05XArbRMqOqrcSIag3SgBs1?usp=sharing

import hanoi_utils as a
import utils as u
import copy


def main():
    u.cls()

    print(f'\033[{36}m Welcome to the Tower of Hanoi game!\033[0m')
    u.tempinho(2.5)
    print(f'\033[{36}m By Cotocs Corporation Games\033[0m')
    u.tempinho(2.5)
    print(f'\033[{36}m Version 1.1.0\033[0m')
    u.tempinho(2.5)
   
    nivel_jogo = None

    while nivel_jogo != 0:
        u.cls()

        nivel_jogo = a.menu()

        if nivel_jogo in (1, 2, 3):

            torres = a.iniciar_jogo(nivel_jogo)

            jogador1 = input("Jogador 1: ")
            jogador2 = input("Jogador 2: ")

            jogadas_1 = a.jogar_partida(jogador1, copy.deepcopy(torres), 1)

            u.cls()
            input("Pressione Enter para o próximo jogador...")

            jogadas_2 = a.jogar_partida(jogador2, copy.deepcopy(torres), 2)

            u.cls()

            print('Fim da partida!')
            u.tempinho(2.5)
            u.cls()

            print(f'{jogador1} fez {jogadas_1} movimentos.')
            print(f'{jogador2} fez {jogadas_2} movimentos.')
            ganhador = a.ganhador(jogadas_1, jogadas_2)
            u.espaco()

            a.salvar(jogador1, jogadas_1, jogador2, jogadas_2, ganhador, torres)

            input('Enter to continue...')

        a.iniciar_jogo(nivel_jogo)

    u.cls()

    print('Fim de jogo. Obrigado por jogar!')


main() 