import os.path
import sys
import time
from collections import deque

#CONSTANTES
VETOR_MOVIMENTOS_POSSIVEIS_3x3 = [-3, 3, -1, 1] #Movimentos possíveis em uma jogada. Ordem [Baixo, Cima, Esquerda, Direita].
SOLUCAO_NPUZZLE_3x3 = '0,1,2,3,4,5,6,7,8'
movimentos_ja_feitos_vertpretos = set()
#CONSTANTES

#Obtem todos os movimentos possiveis
#param: estado atual
#excecao: movimentos que já não são permitidos
def retornar_acoes_possiveis(queue, param, excecao):
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
        
        return False

#Similar a comparação se o vertice está PRETO no BFS
def verificar_se_movimento_ja_feito(movimento):
    if(movimento in movimentos_ja_feitos_vertpretos):
        return True
    return False

#Similar a coloração do vertice de PRETO no BFS
def adicionar_movimento_ja_feito(movimento):     
    if((movimento == SOLUCAO_NPUZZLE_3x3) == False):
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

def ler_input(caminho):    
        if(os.path.exists(caminho) == False):
            print('MSG: O ARQUIVO DE ENTRADA NÃO EXISTE NO CAMINHO INFORMADO: ' + caminho)            
        else:
            file_object = open(caminho, 'r')  
            line = file_object.readline().replace('\n','').replace('\t','').replace(' ','')
            
            if(validar_input(line)):
                return line        
        return ''

def salvar_resultado_out(caminho, resultado):
    try:
        file = open(caminho,'w') 
        file.write('Custo Total: ' + str(resultado))
        file.close()
    except: 
        print('MSG: Houve um erro ao salvar o arquivo [out] no diretório')   

def main():        
    #Variaveis locais
    passos_para_soluacao = 0
    achou_solucao = True
    movimentos_possiveis_vertbrancos = deque()
    movimentos_possiveis_aux = deque()
    #Variaveis locais

    start = time.time()
    time.clock()
    movimento_raiz = ler_input(sys.argv[1])
    
    if(movimento_raiz != ''):   
        if((movimento_raiz == SOLUCAO_NPUZZLE_3x3) == False): #Verifica se a entrada já é a solução
            movimentos_possiveis_vertbrancos.append(movimento_raiz)     
            achou_solucao = False
            print('------------------------------------------------------------------------------')
            
            while (movimentos_possiveis_vertbrancos and (achou_solucao == False)): 
                print('EXECUTANDO PASSO: ' + str(passos_para_soluacao + 1) + ' - QTD NÓS: ' + str(len(movimentos_possiveis_vertbrancos)) , end='\r')
                                              
                while(movimentos_possiveis_vertbrancos): #Obtêm os vértices ADJACENTES dos vertices da Fila                    
                    mov = movimentos_possiveis_vertbrancos.popleft()
                    
                    if(verificar_se_movimento_ja_feito(mov) == False):
                        movimentos_possiveis_aux = retornar_acoes_possiveis(movimentos_possiveis_aux, mov, movimentos_ja_feitos_vertpretos)
                        adicionar_movimento_ja_feito(mov) #Adiciona os vertices JÁ visitados [Cor Preta]
                        # print("OPÇÃO PASSO " + str(passos_para_soluacao) + ': ' + mov)   

                passos_para_soluacao += 1
                movimentos_possiveis_vertbrancos = movimentos_possiveis_aux.copy()#Adiciona os vertices adjacentes na FILA 
                movimentos_possiveis_aux = deque()

                if(movimentos_possiveis_vertbrancos.__contains__(SOLUCAO_NPUZZLE_3x3)):
                    achou_solucao = True
                    print('SOLUÇÃO: ' + SOLUCAO_NPUZZLE_3x3)                   
     
        print('------------------------------------------------------------------------------')
        if(achou_solucao == True):
            salvar_resultado_out(sys.argv[2], passos_para_soluacao)
            print('NÚMERO DE PASSOS NECESSÁRIOS PARA SOLUÇÃO DO N-PUZZLE: ' + str(passos_para_soluacao))
        else:
            salvar_resultado_out(sys.argv[2], 0)
            print('NÃO FOI POSSÍVEL ENCONTRAR SOLUÇÃO PARA O N-PUZZLE')
    
    print("Tempo Gasto (seg): " + str(time.time() - start))

if __name__ == "__main__":
    main()