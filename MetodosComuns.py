# import queue
import Constantes as const
# import os.path
# from collections import deque

# #Obtem todos os movimentos possiveis
#     #param: estado atual
#     #excecao: movimentos que já não são permitidos
# def possibilidades_acoes(param, excecao):
#     queue_movimentos_possiveis = queue.Queue()
#     posicao_valor_zero = 0
#     param_split = param.split(',')
    
#     #Obtendo a posição do valor [zero] no puzzle
#     for p in param_split:
#         if(p == '0'):
#             break
#         posicao_valor_zero += 1
        
#     for v in const.vetor_movimentos_possiveis_3x3:
#         vetor_param_split = param_split.copy()
#         movimentos_validos = True

#         if(posicao_valor_zero + (v) >= 0 and posicao_valor_zero + (v) <= 8):
            
#             #Verifica se o movimento a ser feito é lateral
#             if(v == (1) or v == (-1)) :
#                movimentos_validos = validar_possibilidade_movimento_lateral(posicao_valor_zero, v, 3)

#             #Adiciona a nova possibiidade de movimento    
#             if(movimentos_validos == True):
#                 conteudo_x = vetor_param_split[posicao_valor_zero]
#                 conteudo_y = vetor_param_split[posicao_valor_zero + (v)]
#                 vetor_param_split[posicao_valor_zero] = conteudo_y.replace('\n','').replace('\t','')
#                 vetor_param_split[posicao_valor_zero + (v)] = conteudo_x.replace('\n','').replace('\t','')   
#                 movimento = (','.join(vetor_param_split))
#                 if(excecao.__contains__(movimento) == False):
#                     queue_movimentos_possiveis.put(movimento)

#     return queue_movimentos_possiveis

# #Valida se é possível fazer os movimentos laterais, ou seja, mexer a peça para esquerda ou para direita
# def validar_possibilidade_movimento_lateral(posicao_zero, operacao, tamanho_matriz):
#     resultado = posicao_zero + (operacao)

#     if (tamanho_matriz == 3): # Jogo com Matriz 3X3
#         if(posicao_zero <= 2 and resultado <= 2):
#             return True
#         if((posicao_zero >= 3 and posicao_zero <= 5) and (resultado >= 3 and resultado <= 5)):
#             return True
#         if((posicao_zero >= 6 and posicao_zero <= 8) and (resultado >= 6 and resultado <= 8)):
#             return True
        
#         return False

# def merge_queue(queue1, queue2):
#     nova_queue = deque()
#     queue1.reverse()

#     while(queue1):
#         nova_queue.append(queue1.pop())       
#     while(queue2.empty() == False):
#         elemento = queue2.get()
#         if(nova_queue.__contains__(elemento) == False):
#             nova_queue.append(elemento)
            
#     return nova_queue

# def ler_input():
#     file_object = open(const.name_file_in, 'r')  
#     return file_object.readline()       

# def salvar_out(custo):
#    file = open(const.name_file_out,'w') 
#    file.write('Custo Total: ' + str(custo))
#    file.close()