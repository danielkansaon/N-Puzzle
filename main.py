
import os.path

name_file_in = 'in'
name_file_out = 'out'
vetor_movimentos_3x3 = [-3, 3, -1, 1] #Movimentos possíveis em uma jogada. Ordem [Baixo, Cima, Esquerda, Direita].

def possibilidades_acoes(param):    
    print(param)
    lista_possibilidades = []
    posicao_valor_zero = 0
    param_split = param.split(',')
    
    for p in param_split:
        if(p == '0'):
            break
        posicao_valor_zero += 1
        
    for v in vetor_movimentos_3x3:
        vetor_param_split = param_split.copy()
        movimentos_validos = True

        if(posicao_valor_zero + (v) >= 0 & posicao_valor_zero + (v) <= 8):
            
            #Verifica se o movimento a ser feito é lateral
            if(v == 1 or v == -1):
               movimentos_validos = validar_possibilidade_movimento_lateral(posicao_valor_zero, v, 3)

            #Adiciona a nova possibiidade de movimento    
            if(movimentos_validos == True):
                conteudo_x = vetor_param_split[posicao_valor_zero]
                conteudo_y = vetor_param_split[posicao_valor_zero + (v)]
                vetor_param_split[posicao_valor_zero] = conteudo_y.replace('\n','').replace('\t','')
                vetor_param_split[posicao_valor_zero + (v)] = conteudo_x.replace('\n','').replace('\t','')
                lista_possibilidades.append(','.join(vetor_param_split))

    for p in lista_possibilidades:
         print(p)


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
 
def main():
    if(os.path.exists(name_file_in) == False):
        print('O arquivo [in] não existe no diretório, por favor crie o arquivo e tente novamente.')
    else: 
        file_object = open(name_file_in, 'r')  
        possibilidades_acoes(file_object.readline())

if __name__ == "__main__":
    main()

