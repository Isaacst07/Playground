# link do colab: https://colab.research.google.com/drive/10gRd2uDzakTAAbiiThgW4exy-iwLyO3_#scrollTo=tve6QkaCVwR7

import craft_utils as c
import utils as u 


estoque_inicial = [
    {'id': '287', 'quantidade': '64', 'nome': 'Linha'},
    {'id': '296', 'quantidade': '64', 'nome': 'Trigo'},
    {'id': '353', 'quantidade': '64', 'nome': 'Açúcar'},
    {'id': '344', 'quantidade': '64', 'nome': 'Ovo'},
    {'id': '334', 'quantidade': '64', 'nome': 'Leite'},
    {'id': '260', 'quantidade': '64', 'nome': 'Maça'},
    {'id': '371', 'quantidade': '64', 'nome': 'Pepita de Ouro'}
]

estoque_inicial_insumos = [
   {'id': '23', 'quantidade': '64', 'nome': 'Tábuas de Madeira'}
]

livro_de_receitas = [

    # --- PRIMEIRO PRODUTO: O ARCO ---
    {
        'produto_final': 'Arco',
        'id_produto': '261',
        # 'receita' é uma LISTA de dicionários (ingredientes)
        'receita': [
            {'id_material': '280', 'nome_material': 'Graveto', 'quantidade': '3'},
            {'id_material': '287', 'nome_material': 'Linha', 'quantidade': '3'}
        ]
    },

    # --- SEGUNDO PRODUTO: O BOLO ---
    {
        'produto_final': 'Bolo',
        'id_produto': '354',
        'receita': [
            {'id_material': '296', 'nome_material': 'Trigo', 'quantidade': '3'},
            {'id_material': '353', 'nome_material': 'Açúcar', 'quantidade': '2'},
            {'id_material': '344', 'nome_material': 'Ovo', 'quantidade': '1'},
            {'id_material': '334', 'nome_material': 'Leite', 'quantidade': '3'}
        ]
    },

    # --- TERCEIRO PRODUTO: A MAÇÃ DOURADA ---
    {
        'produto_final': 'Maça Dourada',
        'id_produto': '322',
        'receita': [
            {'id_material': '260', 'nome_material': 'Maçã', 'quantidade': '1'},
            {'id_material': '371', 'nome_material': 'Pepita de Ouro', 'quantidade': '8'}
        ]
    },

    {
       'produto_final': 'Graveto',
       'id_produto': '280',
       'receita': [
          {'id_material': '23', 'nome_material': 'Tábua de Madeira', 'quantidade': '2'}
       ]
    }

]


def main():
  # Cria Diciónario com nome e o index(posição) desse item dentro de livro_de_receitas
  index_itens = {item['produto_final']: indice for indice, item in enumerate(livro_de_receitas)}
  u.cls()

  escolha = 1
  estoque_finalizados = c.iniciar_estoque(estoque_inicial)
  estoque_insumos = c.iniciar_estoque(estoque_inicial_insumos)

  while escolha != 0:
    u.cls()

    escolha = c.menu(1)

    if escolha == 1:
        u.cls()

        item =  c.devolver_item(c.menu(2), livro_de_receitas)
        u.cls()

        print(c.para_criacao(item, livro_de_receitas, index_itens))
        input('Enter to continue...')

        u.cls()

        qtd_item = u.obter_numero_minimo(f'Quantidade de {item}s a se fazer(Obs: No mínimo 1): ', 1)
        
        if c.validar_criacao(estoque_finalizados, estoque_insumos, item, livro_de_receitas, index_itens, qtd_item):
            u.cls()
            print('Bom checamos no estoque aqui e o item pode ser criado!')
            input('Enter to continue...')
            u.cls()
            print(c.atualizar_estoque(estoque_finalizados, estoque_insumos, item, livro_de_receitas, index_itens, qtd_item))
            
            print(estoque_finalizados)
            print('')
            

            estoque_finalizados = c.adicionar_item_finalizado(estoque_finalizados, livro_de_receitas[index_itens[item]]['id_produto'], item ,qtd_item)

            print(estoque_finalizados)
            print('')
            print(estoque_insumos)

            input('Enter to continue...')

        else:
           u.cls()

           print(c.nao_criou(estoque_finalizados, estoque_insumos, item, livro_de_receitas, index_itens, qtd_item))

           input('Enter to continue ...')


    elif escolha == 2:
       u.cls()

       print(c.ver_estoque(estoque_finalizados, 'estoque de itens'))
       u.espaco()

       input('Enter to continue...')

    elif escolha == 3: 
       u.cls()

       print(c.ver_estoque(estoque_insumos, 'estoque de insumos'))
       u.espaco()

       input('Enter to continue...')

    elif escolha == 4:
        u.cls()

        opcao = c.menu(3)

        if opcao == 1:
            u.cls()

            print(c.ver_estoque(estoque_insumos, 'ESTOQUE DE INSUMOS'))

            u.espaco()

            id = u.obter_numero_minimo('Id do item a ser removido: ', 0)
            quantidade = u.obter_numero_minimo('Quantidade a ser removida: ', 0)

            u.cls()

            print(c.remover_estoque(estoque_insumos, str(id), quantidade))

            u.espaco()

            input('Enter to continue...')

        if opcao == 2:
            u.cls()

            print(c.ver_estoque(estoque_finalizados,'ESTOQUE DE FINALIZADOS' ))

            u.espaco()

            id = u.obter_numero_minimo('Id do item a ser removido: ', 0)
            quantidade = u.obter_numero_minimo('Quantidade a ser removida: ', 0)

            u.cls()

            print(c.remover_estoque(estoque_finalizados, str(id), quantidade))

            u.espaco()

            input('Enter to continue...')


main()