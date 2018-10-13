import os.path
import time
from collections import deque

#CONSTANTES
NAME_FILE_IN = 'in'
NAME_FILE_OUT = 'out'
VETOR_MOVIMENTOS_POSSIVEIS_3x3 = [-3, 3, -1, 1] #Movimentos possíveis em uma jogada. Ordem [Baixo, Cima, Esquerda, Direita].
SOLUCAO_NPUZZLE = '0,1,2,3,4,5,6,7,8'
movimentos_ja_feitos_vertpretos = []
#CONSTANTES

#Obtem todos os movimentos possiveis
#param: estado atual
#excecao: movimentos que já não são permitidos
def retornar_acoes_possiveis(param, excecao):
    queue_movimentos_possiveis = deque()
    posicao_valor_zero = 0
    param_split = param.split(',')
    
    #Obtendo a posição do valor [zero] no puzzle
    for p in param_split:
        if(p == '0'):
            break
        posicao_valor_zero += 1
        
    for v in VETOR_MOVIMENTOS_POSSIVEIS_3x3:
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
                vetor_param_split[posicao_valor_zero] = conteudo_y.replace('\n','').replace('\t','').replace(' ','')
                vetor_param_split[posicao_valor_zero + (v)] = conteudo_x.replace('\n','').replace('\t','').replace(' ','')   
                movimento = (','.join(vetor_param_split))
                if(excecao.__contains__(movimento) == False):
                    queue_movimentos_possiveis.append(movimento)

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
    if((movimento == SOLUCAO_NPUZZLE) == False):
        movimentos_ja_feitos_vertpretos.append(movimento)

def merge_list_queue(queue1, queue2):
    nova_queue = deque()

    while(queue1):
            nova_queue.append(queue1.popleft())
    while(queue2):
        elemento = queue2.popleft()
        if(nova_queue.__contains__(elemento) == False):
            nova_queue.append(elemento)
      
    return nova_queue

def validar_input(param):
    param_split = param.split(',')
    lista_elementos = []
    try:
        if(len(param_split) == 9):
            for p in param_split:
                if(p == '' or ((int(p) >= 0 and int(p) <= 8) == False) or (lista_elementos.__contains__(p) == True)):            
                    return False
                else:
                    lista_elementos.append(p)
            return True
        if(len(param_split) == 16):
            for p in param_split:
                if(p == '' or ((int(p) >= 0 and int(p) <= 15) == False) or (lista_elementos.__contains__(p) == True)):            
                    return False
                else:
                    lista_elementos.append(p)
            return True
    except ValueError:    
        return False
    
    return False

def ler_input():
    try:
        if(os.path.exists(NAME_FILE_IN) == False):
            print('MSG: O arquivo [in] não existe no diretório, por favor crie o arquivo e tente novamente.')
        else:
            file_object = open(NAME_FILE_IN, 'r')  
            line = file_object.readline().replace('\n','').replace('\t','').replace(' ','')
            
            if(validar_input(line)):
                return line 

        print('MSG: O ARQUIVO DE ENTRADA ESTÁ INCORRETO, VERFIQUE PARA CONTINUAR')        
        return ''
    except FileNotFoundError:
        print('MSG: Arquivo [in] não encontrado no diretório')
        return ''

def salvar_resultado_out(custo):
    try:
        file = open(NAME_FILE_OUT,'w') 
        file.write('Custo Total: ' + str(custo))
        file.close()
    except: 
        print('MSG: Houve um erro ao salvar o arquivo [out] no diretório')   

def main():
    #Variaveis locais
    passos_para_soluacao = 0
    achou_solucao = False
    tem_solucao = True
    movimentos_possiveis_vertbrancos = deque()
    movimentos_possiveis_aux = deque()
    #Variaveis locais

    start = time.time()
    time.clock()
    movimento_raiz = ler_input()
    
    if(movimento_raiz != ''):   
        if((movimento_raiz == SOLUCAO_NPUZZLE) == False):
            movimentos_possiveis_aux.append(movimento_raiz)     

            while ((tem_solucao == True) and (achou_solucao == False)):
                print('EXECUTANDO PASSO: ' + str(passos_para_soluacao + 1))
                print('Ainda em execução...')                
                
                movimentos_possiveis_vertbrancos = movimentos_possiveis_aux.copy()
                movimentos_possiveis_aux = []

                if(movimentos_possiveis_vertbrancos == False): #Is empty
                    tem_solucao = False
                    break
               
                #Verifica se os movimentos [verticies brancos] são a solução, se não, visitam os vertices adjacentes
                while(movimentos_possiveis_vertbrancos):
                    m = movimentos_possiveis_vertbrancos.popleft()
                    
                    if(verificar_se_movimento_ja_feito(m) == False):
                        movimentos_possiveis_aux = merge_list_queue(movimentos_possiveis_aux, retornar_acoes_possiveis(m, movimentos_ja_feitos_vertpretos))
                        adicionar_movimento_ja_feito(m) #Adiciona os vertices de cor Preta
                        print("OPÇÃO PASSO " + str(passos_para_soluacao) + ': ' + m)
                                
                if(movimentos_possiveis_aux.__contains__(SOLUCAO_NPUZZLE)): #Verifica se a solução já foi encontrada
                    achou_solucao = True
                    print(SOLUCAO_NPUZZLE)

                passos_para_soluacao += 1
        else:
            passos_para_soluacao = 0

        print('FIM')  
        print('------------------------------------------------------------------------------------')

        if(tem_solucao == True):
            salvar_resultado_out(passos_para_soluacao)
            print('NÚMERO DE PASSOS NECESSÁRIOS PARA SOLUÇÃO DO N-PUZZLE: ' + str(passos_para_soluacao))
        else:
            salvar_resultado_out(0)
            print('NÃO FOI POSSÍVEL ENCONTRAR SOLUÇÃO PARA O N-PUZZLE')
    else:        
        print('------------------------------------------------------------------------------------')    
        print('FIM')   

    print("Tempo Gasto (seg): " + str(time.time() - start))

if __name__ == "__main__":
    main()