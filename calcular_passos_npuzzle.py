from collections import deque
import os.path
import time
import sys

#CONSTANTES
VETOR_MOVIMENTOS_POSSIVEIS = [-3, 3, -1, 1] #Movimentos possíveis em uma jogada. Ordem [Baixo, Cima, Esquerda, Direita].
SOLUCAO_NPUZZLE = '0,1,2,3,4,5,6,7,8'
TAMANHO_PUZZLE = 3
movimentos_ja_feitos_vertpretos = set()
#CONSTANTES

#Obtem todos os movimentos possiveis. [queue] fila para adicionar os movimentos; [param]: estado atual; [excecao]: movimentos que já não são permitidos
def retornar_acoes_possiveis(queue, param, excecao):
    posicao_valor_zero = 0
    param_split = param.split(',')
    
    #Obtendo a posição do valor [zero] no puzzle
    for p in param_split:
        if(p == '0'):
            break
        posicao_valor_zero += 1
    
    for v in VETOR_MOVIMENTOS_POSSIVEIS:
        vetor_param_split = param_split.copy()
        movimentos_validos = True
        
        if(posicao_valor_zero + (v) >= 0 and posicao_valor_zero + (v) <= (TAMANHO_PUZZLE * TAMANHO_PUZZLE) - 1):
            
            #Verifica se o movimento a ser feito é lateral
            if(v == (1) or v == (-1)) :
               movimentos_validos = validar_possibilidade_movimento_lateral(posicao_valor_zero, v, TAMANHO_PUZZLE)

            #Adiciona a nova possibiidade de movimento    
            if(movimentos_validos == True):
                conteudo_x = vetor_param_split[posicao_valor_zero]
                conteudo_y = vetor_param_split[posicao_valor_zero + (v)]
                vetor_param_split[posicao_valor_zero] = conteudo_y.replace('\n','').replace('\t','').replace(' ','')
                vetor_param_split[posicao_valor_zero + (v)] = conteudo_x.replace('\n','').replace('\t','').replace(' ','')   
                movimento = (','.join(vetor_param_split))
                if(verificar_se_movimento_ja_feito(movimento) == False):
                    queue.append(movimento)      

    return queue
    
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
    else: # Jogo com Matriz 4X4
        if(posicao_zero <= 3 and resultado <= 3):
            return True
        if((posicao_zero >= 4 and posicao_zero <= 7) and (resultado >= 4 and resultado <= 7)):
            return True
        if((posicao_zero >= 8 and posicao_zero <= 11) and (resultado >= 8 and resultado <= 11)):
            return True
        if((posicao_zero >= 12 and posicao_zero <= 15) and (resultado >= 12 and resultado <= 15)):
            return True
    return False

#Similar a comparação se o vertice está PRETO no BFS
def verificar_se_movimento_ja_feito(movimento):
    if(movimento in movimentos_ja_feitos_vertpretos):
        return True
    return False

#Similar a coloração do vertice de PRETO no BFS
def adicionar_movimento_ja_feito(movimento):     
    if((movimento == SOLUCAO_NPUZZLE) == False):
        movimentos_ja_feitos_vertpretos.add(movimento)

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

def config_ambiente(tamanho):
    global SOLUCAO_NPUZZLE
    global VETOR_MOVIMENTOS_POSSIVEIS
    global TAMANHO_PUZZLE

    if(tamanho == 9):
        SOLUCAO_NPUZZLE = '0,1,2,3,4,5,6,7,8'
        VETOR_MOVIMENTOS_POSSIVEIS = [-3, 3, -1, 1]
        TAMANHO_PUZZLE = 3
    else:
        SOLUCAO_NPUZZLE = '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'
        VETOR_MOVIMENTOS_POSSIVEIS = [-4, 4, -1, 1]
        TAMANHO_PUZZLE = 4

def ler_input(caminho):    
        if(os.path.exists(caminho) == False):
            print('MSG: O ARQUIVO DE ENTRADA NAO EXISTE NO CAMINHO INFORMADO: ' + caminho)            
        else:
            file_object = open(caminho, 'r')  
            line = file_object.readline().replace('\n','').replace('\t','').replace(' ','')
            
            if(validar_input(line)):
                config_ambiente(len(line.split(',')))
                return line
            else:
                print('MSG: O ARQUIVO DE ENTRADA ['+ caminho + '] NÃO E VALIDO')     
        return ''

def salvar_resultado_out(caminho, resultado):
    try:
        file = open(caminho,'w') 
        file.write('Custo Total: ' + str(resultado))
        file.close()
    except: 
        print('MSG: Houve um erro ao salvar o arquivo [out] no diretório')   

def calcular_passos(raiz):
    achou_solucao = False
    passos_para_soluacao = 0
    num_vertices_adjacentes = 0
    Queue_movimentos_possiveis_vertbrancos = deque()    
    
    if((raiz == SOLUCAO_NPUZZLE) == False):
        Queue_movimentos_possiveis_vertbrancos.append(raiz)     
        print('------------------------------------------------------------------------------')
            
        while (Queue_movimentos_possiveis_vertbrancos and achou_solucao == False): #is not empty
            print('EXECUTANDO PASSO: ' + str(passos_para_soluacao + 1) + ' - QTD NOS: ' + str(len(movimentos_ja_feitos_vertpretos)) , end='\r')
            num_vertices_adjacentes = len(Queue_movimentos_possiveis_vertbrancos) #Contador para saber qts nos adjacentes visitar

            while(Queue_movimentos_possiveis_vertbrancos and num_vertices_adjacentes > 0): #Obtêm os vértices ADJACENTES dos vertices da Fila                    
                mov = Queue_movimentos_possiveis_vertbrancos.popleft()
                
                if(verificar_se_movimento_ja_feito(mov) == False):
                    Queue_movimentos_possiveis_vertbrancos = retornar_acoes_possiveis(Queue_movimentos_possiveis_vertbrancos, mov, movimentos_ja_feitos_vertpretos)
                    adicionar_movimento_ja_feito(mov) #Adiciona os vertices JÁ visitados [Cor Preta]
                
                num_vertices_adjacentes += -1
            
            passos_para_soluacao += 1
            if(Queue_movimentos_possiveis_vertbrancos.__contains__(SOLUCAO_NPUZZLE)): #Verificando se achou a solução
                achou_solucao = True
                break
    else:
        achou_solucao = True

    print('QUANTIDADE DE NOS(POSSIBILIDADES) VISITADOS: ' + str(len(movimentos_ja_feitos_vertpretos)), end='\n')
    
    if(achou_solucao == True):
        return passos_para_soluacao
    else:
        return -1 #Não tem solução

def main():           
    #VARIAVEIS
    raiz = ler_input(sys.argv[1])
    start = time.time()
    time.clock()  
    #VARIAVEIS   

    if(raiz != ''):
        passos_para_soluacao = calcular_passos(raiz) #Calcula o numero de passos para a solução

        print('------------------------------------------------------------------------------')
        if(passos_para_soluacao >= 0):
            salvar_resultado_out(sys.argv[2], passos_para_soluacao)
            print('SOLUCAO: ' + SOLUCAO_NPUZZLE)
            print('SOLUCAO: NUMERO DE PASSOS NECESSARIOS PARA SOLUCAO DO N-PUZZLE: ' + str(passos_para_soluacao))
        else:
            salvar_resultado_out(sys.argv[2], -1)
            print('SOLUCAO: NAO FOI POSSIVEL ENCONTRAR SOLUCAO PARA O N-PUZZLE')
    else:
        print('------------------------------------------------------------------------------')

    print("Tempo Gasto (seg): " + str(time.time() - start))             
    
if __name__ == "__main__":   
    main()

