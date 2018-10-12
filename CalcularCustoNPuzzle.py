import os.path
import queue
from collections import deque

name_file_in = 'in'
name_file_out = 'out'
vetor_movimentos_possiveis_3x3 = [-3, 3, -1, 1] #Movimentos possíveis em uma jogada. Ordem [Baixo, Cima, Esquerda, Direita].
movimentos_ja_feitos = []
movimentos_fazer = queue.Queue()
SOLUCAO_NPUZZLE = '0,1,2,3,4,5,6,7,8'

#Obtem todos os movimentos possiveis
    #param: estado atual
    #excecao: movimentos que já não são permitidos
def possibilidades_acoes(param, excecao):
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

def verificar_se_movimento_ja_feito(movimento):
    if(movimentos_ja_feitos.__contains__(movimento)):
        return True
    return False

def adicionar_movimento_ja_feito(movimento):     
    if( (movimento == SOLUCAO_NPUZZLE) == False):
        movimentos_ja_feitos.append(movimento)
   
    print(movimento)

def merge_queue(q1, q2):
    nova_queue = deque()
    q1.reverse()

    while(q1):
        nova_queue.append(q1.pop())       
    while(q2.empty() == False):
        elemento = q2.get()
        if(nova_queue.__contains__(elemento) == False):
            nova_queue.append(elemento)
            
    return nova_queue

def salvar_resultado(custo):
   file = open(name_file_out,'w') 
   file.write('Custo Total: ' + str(custo))
   file.close()

def main():

    #Variaveis locais
    passos_para_soluacao = 0
    achou_solucao = False
    movimentos_possiveis_vertbrancos = deque()

    if(os.path.exists(name_file_in) == False):
        print('O arquivo [in] não existe no diretório, por favor crie o arquivo e tente novamente.')
    else: 
        file_object = open(name_file_in, 'r')  
        movimento_raiz = file_object.readline()       

        if( (movimento_raiz == SOLUCAO_NPUZZLE) == False):

            movimentos_fazer.put(movimento_raiz)                
            
            while (achou_solucao == False):
                passos_para_soluacao += 1
                movimentos_possiveis_vertbrancos = []

                while (movimentos_fazer.empty() == False):
                    movimento = movimentos_fazer.get()                
                    movimentos_possiveis_vertbrancos = merge_queue(movimentos_possiveis_vertbrancos, possibilidades_acoes(movimento, movimentos_ja_feitos))
                    adicionar_movimento_ja_feito(movimento)
            
                print('EXECUTANDO PASSO: ' + str(passos_para_soluacao))
                print('Ainda em execução...')

                movimentos_possiveis_vertbrancos.reverse()
                                
                while(movimentos_possiveis_vertbrancos):
                    m = movimentos_possiveis_vertbrancos.pop()
                    
                    if(m == SOLUCAO_NPUZZLE):
                        achou_solucao = True
                        break   

                    if(verificar_se_movimento_ja_feito(m) == False):
                        movimentos_fazer.put(m)
    print('FIM')  
    print('------------------------------------------------------------------------------------')         
    print('NÚMERO DE PASSOS NECESSÁRIOS PARA SOLUÇÃO DO N-PUZZLE: ' + str(passos_para_soluacao))

if __name__ == "__main__":
    main()