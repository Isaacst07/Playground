import numpy as np
import utils as u


def menu(n_menu):
    menu1 = '''=========VENANCRAFT=========
|1 - Criar item            |
|2 - Ver Estoque de Itens  |
|3 - Ver Estoque de Insumos|
|4 - Remover Item          |
|                          |
|0 - Sair                  |
============================

>>> '''

    menu2= '''=====CRAFTTABLE=====
|1 - Arco          |
|2 - Bolo          |
|3 - Maça Dourada  |
|4 - Graveto       |
====================

>>> '''
    menu3 = '''===== REMOVER DE QUAL =====
|1 - Estoque de Insumos    |
|2 - Estoque de Finalizados|
============================

>>> '''


    if n_menu == 1:
       escolha = u.obter_numero_faixa(menu1, 0, 4)
    elif n_menu == 2:
        escolha = u.obter_numero_faixa(menu2, 1, 4)
    else:
        escolha = u.obter_numero_faixa(menu3, 1, 2)

    return escolha


def devolver_item(escolha: int, livro_de_receita):
    itens = {}
    i = 1

    for receita in livro_de_receita:
        itens[i] = receita['produto_final']

        i += 1

    return itens[escolha]
    

def iniciar_estoque(estoque_inicial):

  ids = [item['id'] for item in estoque_inicial]
  qtds = [item['quantidade'] for item in estoque_inicial]
  nomes = [item['nome'] for item in estoque_inicial]

  estoque = np.column_stack((ids, qtds, nomes))

  return estoque


def validar_criacao(estoque_finalizados, estoque_insumos, item , livro_de_receitas, index_itens, qtd_item):

    # Cria uma lista com os materias necéssario para fazer aquele item:
    ingredientes = livro_de_receitas[index_itens[item]]['receita']

    for ingrediente in ingredientes:

        if ingrediente['id_material'] in estoque_finalizados[:,0]:

            if not tem_quantidade_suficiente(estoque_finalizados, ingrediente['id_material'], int(ingrediente['quantidade']) * qtd_item):
                return False
            
        elif ingrediente['id_material'] in estoque_insumos[:,0]:
            if not tem_quantidade_suficiente(estoque_insumos, ingrediente['id_material'], int(ingrediente['quantidade']) * qtd_item):
                return False

        else:
            componente = livro_de_receitas[index_itens[ingrediente['nome_material']]]['receita']

            if not tem_quantidade_suficiente(estoque_insumos, componente[0]['id_material'], int(componente[0]['quantidade']) * qtd_item * int(ingrediente['quantidade'])):
                return False

    return True


def tem_quantidade_suficiente(estoque, id_item, qtd_item):
    mascara = (estoque[:, 0] == id_item) # me volta qual a linha está esse produto pelo id
  
    quantidade_estoque = estoque[mascara][0, 1]# acesso a qtd do item, [mascara] acesso a linha que o item está e depois [0, 1] quantida daquela linha [id, qtd].

    return int(quantidade_estoque) >= qtd_item
        

def atualizar_estoque(estoque_finalizados, estoque_insumos,  nome_item, livro_de_receita, index_itens, qtd_item):  

    itens_atualizar = livro_de_receita[index_itens[nome_item]]['receita']

    for item in itens_atualizar:

        if item['id_material'] in estoque_finalizados[:,0]:

            mascara = (estoque_finalizados[:, 0] == item['id_material']) # linha onde tá esse item no estoque

            estoque_finalizados[mascara, 1]= int(estoque_finalizados[mascara, 1]) - (int(item['quantidade']) * qtd_item)

        elif item['id_material'] in estoque_insumos[:,0]:
            mascara = (estoque_insumos[:,0] == item['id_material'])

            estoque_insumos[mascara, 1] = int(estoque_insumos[mascara, 1]) - (int(item['quantidade']) * qtd_item)

        else:
            insumo_atulizar = livro_de_receita[index_itens[item['nome_material']]]['receita']
            
            mascara_insumo = (estoque_insumos[:, 0] == insumo_atulizar[0]['id_material'])
        
            estoque_insumos[mascara_insumo, 1] = int(estoque_insumos[mascara_insumo, 1]) - (int(insumo_atulizar[0]['quantidade']) * qtd_item * int(item['quantidade']))

    return 'Estoque atulizado com Sucesso!'


def adicionar_item_finalizado(estoque_itens_finais, id_item, nome, qtd_item):

    if id_item in estoque_itens_finais[:, 0]:

        mascara = (estoque_itens_finais[:, 0] == id_item)

        estoque_itens_finais[mascara, 1] = int(estoque_itens_finais[mascara, 1]) + qtd_item

    else:
        estoque_itens_finais = np.concatenate((estoque_itens_finais, [[id_item, qtd_item, nome]]), axis=0)
    
    return estoque_itens_finais


def para_criacao(item, livro_de_receitas, index_itens):
    ingredientes = livro_de_receitas[index_itens[item]]['receita']

    i = 0

    criar = f'''Para criar um {item} você precisa de:
'''
    for ingrediente in ingredientes:

        try:
            if ingrediente['id_material'] == livro_de_receitas[index_itens[ingrediente['nome_material']]]['id_produto']:

                itens_ingredientes = livro_de_receitas[index_itens[ingrediente['nome_material']]]['receita']

                criar += f'{i+1} - {ingrediente['nome_material']} (x{ingrediente['quantidade']}):\n'

                for item in itens_ingredientes:

                    criar += f' • {item['nome_material']} (x{item['quantidade']})\n'

        except KeyError:
            criar += f'{i+1} - {ingrediente['nome_material']} (x{ingrediente['quantidade']}) \n'

        i += 1

    return criar


# No seu arquivo de utils (craft_utils.py)

def nao_criou(estoque_finalizados, estoque_insumos, item, livro_de_receitas, index_itens, qtd_item):
    ingredientes = livro_de_receitas[index_itens[item]]['receita']
    motivo = f'Infelizmente, não foi possível criar o {item}, pois há ingredientes faltando:\n'

    for ingrediente in ingredientes:
        id_material = ingrediente['id_material']
        qtd_necessaria = int(ingrediente['quantidade']) * qtd_item
        nome_material = ingrediente['nome_material']
        
        # Verifica se o material está no estoque de finalizados
        if id_material in estoque_finalizados[:, 0]:
            if not tem_quantidade_suficiente(estoque_finalizados, id_material, qtd_necessaria):
                mascara = (estoque_finalizados[:, 0] == id_material)
                qtd_atual = estoque_finalizados[mascara][0, 1]
                motivo += f'• {nome_material}: Precisa de {qtd_necessaria}, mas só tem {qtd_atual}.\n'
        
        # Se não, verifica se está no estoque de insumos
        elif id_material in estoque_insumos[:, 0]:

            if not tem_quantidade_suficiente(estoque_insumos, id_material, qtd_necessaria):
                mascara = (estoque_insumos[:, 0] == id_material)
                qtd_atual = estoque_insumos[mascara][0, 1]
                motivo += f'• {nome_material}: Precisa de {qtd_necessaria}, mas só tem {qtd_atual}.\n'
        
        # Se não está em nenhum, é um item que precisa ser craftado (caso do Graveto)
        # ou simplesmente não existe.
        else:
            # Indica que falta o material.
            motivo += f'• {nome_material}: Você não tem este item no estoque para usar como material.\n'

    return motivo


def ver_estoque(estoque, nome_estoque):
    
    tabela_estoque = f'=========ESTOQUE DO {nome_estoque.upper()}=========\n'

    for item in estoque:
        tabela_estoque += f'ID: {item[0]} | {item[2]} (x{item[1]})\n'

    tabela_estoque += '==============================================='

    return tabela_estoque


def remover_estoque(estoque, id, quantidade):
    mascara = (estoque[:, 0] == id)

    if mascara.any():
        if tem_quantidade_suficiente(estoque, id, quantidade):
            estoque[mascara, 1] = int(estoque[mascara, 1]) - quantidade
            return f'Foram removidos {quantidade} de {estoque[mascara, 2][0]}'
        else:
            return f'Não possível remover {estoque[mascara, 2][0]}.\nPois só tem como remover {estoque[mascara, 1][0]} itens que é o que tem no estoque e você que remover {quantidade}.'
    
    return f'Não foi possível remover item, pois o id {id} não existe!'