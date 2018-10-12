import os.path
import queue
from collections import deque

#CONSTANTES
name_file_in = 'in'
name_file_out = 'out'
vetor_movimentos_possiveis_3x3 = [-3, 3, -1, 1] #Movimentos possíveis em uma jogada. Ordem [Baixo, Cima, Esquerda, Direita].
movimentos_ja_feitos_vertpretos = []
movimentos_fazer_vertcinzas = queue.Queue()
SOLUCAO_NPUZZLE = '0,1,2,3,4,5,6,7,8'
#CONSTANTES

#Obtem todos os movimentos possiveis
    #param: estado atual
    #excecao: movimentos que já não são permitidos
def retornar_acoes_possiveis(param, excecao):
    queue_movimentos_possiveis = queue.Queue()
    posicao_valor_zero = 0
    param_split = param.split(',')
    
    #Obtendo a posição do valor [zero] no puzzle
    for p in param_split:
        if(p == '0'):
            break
        posicao_valor_zero += 1
        
    for v in vetor_movimentos_possiveis_3x3:
        vetor_param_split = param_split.copy()
        movimentos_validos = True

        if(posicao_valor_zero + (v) >= 0 and posicao_valor_zero + (v) <= 8):
            
            #Verifica se o movimento a ser feito é lateral
            if(v == (1) or v == (-1)) :
               movimentos_validos = validar_possibilidade_movimento_lateral(posicao_valor_zero, v, 3)

            #Adiciona a nova possibiidade de movimento    
            if(movimentos_validos == True):
                conteudo_x = vetor_param_split[posicao_valor_zero]
                conteudo_y = vetor_param_split[posicao_valor_zero + (v)]
                vetor_param_split[posicao_valor_zero] = conteudo_y.replace('\n','').replace('\t','')
                vetor_param_split[posicao_valor_zero + (v)] = conteudo_x.replace('\n','').replace('\t','')   
                movimento = (','.join(vetor_param_split))
                if(excecao.__contains__(movimento) == False):
                    queue_movimentos_possiveis.put(movimento)

    return queue_movimentos_possiveis

#Valida se é possível fazer os movimentos laterais, ou seja, mexer a peça para esquerda ou para direita
def validar_possibilidade_movimento_lateral(posicao_zero, operacao, tamanho_matriz):
    resultado = posicao_zero + (operacao)

    if (tamanho_matriz == 3): # Jogo com Matriz 3X3
        if(posicao_zero <= 2 and resultado <= 2):
            return True
        if((posicao_zero >= 3 and posicao_zero <= 5) and (resultado >= 3 and resultado <= 5)):
            return True
        if((posicao_zero >= 6 and posicao_zero <= 8) and (resultado >= 6 and resultado <= 8)):
            return True
        
        return False

#Similar a comparação se o vertice está PRETO no BFS
def verificar_se_movimento_ja_feito(movimento):
    if(movimentos_ja_feitos_vertpretos.__contains__(movimento)):
        return True
    return False

#Similar a coloração do vertice de PRETO no BFS
def adicionar_movimento_ja_feito(movimento):     
    if( (movimento == SOLUCAO_NPUZZLE) == False):
        movimentos_ja_feitos_vertpretos.append(movimento)
   
    print(movimento)

def merge_list_queue(lista, queue):
    nova_queue = deque()
    lista.reverse()

    while(lista):
        nova_queue.append(lista.pop())       
    while(queue.empty() == False):
        elemento = queue.get()
        if(nova_queue.__contains__(elemento) == False):
            nova_queue.append(elemento)            
    return nova_queue

def ler_input():
    try:
        if(os.path.exists(name_file_in) == False):
            print('O arquivo [in] não existe no diretório, por favor crie o arquivo e tente novamente.')
        else:
            file_object = open(name_file_in, 'r')  
            return file_object.readline() 
        return ''
    except FileNotFoundError:
        print('Arquivo [in] não encontrado no diretório')
        return ''

def salvar_resultado_out(custo):
    try:
        file = open(name_file_out,'w') 
        file.write('Custo Total: ' + str(custo))
        file.close()
    except: 
        print('Houve um erro ao salvar o arquivo [out] no diretório')   

def main():
    #Variaveis locais
    passos_para_soluacao = 0
    achou_solucao = False
    tem_solucao = True
    movimentos_possiveis_vertbrancos = deque()
    movimentos_possiveis_aux = deque()
    #Variaveis locais

    movimento_raiz = ler_input()
    
    if(movimento_raiz != ''):   
        if((movimento_raiz == SOLUCAO_NPUZZLE) == False):
            movimentos_fazer_vertcinzas.put(movimento_raiz)                
            
            while ((tem_solucao == True) and (achou_solucao == False)):
                passos_para_soluacao += 1
                movimentos_possiveis_vertbrancos = []

                #Obtem os próximos movimentos a serem feitos
                while (movimentos_fazer_vertcinzas.empty() == False):
                    movimento = movimentos_fazer_vertcinzas.get()                
                    movimentos_possiveis_vertbrancos = merge_list_queue(movimentos_possiveis_vertbrancos,
                    retornar_acoes_possiveis(movimento, movimentos_ja_feitos_vertpretos))
                    adicionar_movimento_ja_feito(movimento)
            
                print('EXECUTANDO PASSO: ' + str(passos_para_soluacao))
                print('Ainda em execução...')
                movimentos_possiveis_vertbrancos.reverse()

                if(movimentos_possiveis_vertbrancos == False):
                    tem_solucao = False
                    break

                #Verifica se os movimentos [verticies brancos] são a solução do N-Puzzle
                while(movimentos_possiveis_vertbrancos):
                    m = movimentos_possiveis_vertbrancos.pop()
                    
                    if(m == SOLUCAO_NPUZZLE):
                        achou_solucao = True
                        break   
                    if(verificar_se_movimento_ja_feito(m) == False):
                        movimentos_fazer_vertcinzas.put(m)
        print('FIM')  
        print('------------------------------------------------------------------------------------')

        if(tem_solucao == True):
            salvar_resultado_out(passos_para_soluacao)
            print('NÚMERO DE PASSOS NECESSÁRIOS PARA SOLUÇÃO DO N-PUZZLE: ' + str(passos_para_soluacao))
        else:
            salvar_resultado_out(0)
            print('NÃO FOI POSSÍVEL ENCONTRAR SOLUÇÃO PARA O N-PUZZLE')
    else:
        print('FIM')  
        print('------------------------------------------------------------------------------------')

if __name__ == "__main__":
    main()