
#global import
import sys
import time

#Função que calcula a aptidao de uma solução dada uma instância para o problema flow shop sequencing
#A aptidão desse problema é o makespan, que deve ser minimizado
#param solucao deve ser uma lista de inteiros identificando as tarefas (de 1 até n onde n é o número de tarefas da instância)
#param instancia deve ser uma lista de listas m X n, onde m é o número de máquinas e n o número de tarefas, com inteiros identificando os tempos de cada tarefa em cada máquina


def makespan (instancia, solucao):
    nM = len(instancia)
    tempo = [0] * nM
    tarefa = [0] * len(solucao)
    for t in solucao:
        if tarefa[t-1] == 1:
            return "SOLUÇÃO INVÁLIDA: tarefa repetida!"
        else:
            tarefa[t-1] = 1
        for m in range (nM):
            if tempo[m] < tempo[m-1] and m!=0:
                tempo[m] = tempo[m-1] 
            tempo[m] += instancia[m][t-1] 
    return tempo[nM-1]

#ler a primeira instância de cada um dos dez arquivos, armazenar em uma lista e retornar essa lista
def lerInstancias(listaArquivos):
    pass

#criar uma lista de soluções aleatórias (podem definir outro critério se desejarem) com o tamanho repassado
def criarPopulacaoInicial(instancia, tamanho):
    pass

#usar a função makespan para avalaiar a aptidão de cada elemento da população
def avaliarPop(populacao):
    pass

#retorna a melhor solucao dentre a populacao atual
def retornaMelhorSolucao(populacao, aptidaoPop):
    pass

#função deve retornar quais elementos serão recombinados e com quem (pode fazer uso da aptidao ou não para o critério de seleção)
def selecionarPop(populacao, aptidaoPop):
    pass

#função deve usar o operador de recombinacao (definido pelo grupo_ para gerar novas soluções filhas
def recombinacao(populacaoSelecionada):
    pass

#função deve usar o operador de mutacao (definido pelo grupo) para modificar as soluções filhas (não precisa ser todas)
def mutacao(novasSolucoes):
    pass

def selecionarNovaGeracao(populacaoAtual, novasSolucoes):
    pass
#função deve criar uma nova população com as soluções novas (eliminando as antigas ou usando outro critério de seleção desejado)

#computar o lower bound, upper bound, valores médios e desvios (tanto para aptidão quanto para o tempo de execução) para cada instância
#salvar em formato de tabela (pode ser um CSV) em um arquivo
def salvarRelatorio(relatorio):
    pass

#Exemplo de uso do makespan
instancia = [[54, 83, 15],
             [79, 3, 11],
             [16, 89, 49],
             [66, 58, 31],
             [58, 56, 20]]
solucao1 = [1,2,3]
solucao2 = [2,1,3]
solucao3 = [3,1,2]
solucao4 = [3,1,3]
print (makespan(instancia,solucao1))
print (makespan(instancia,solucao2))
print (makespan(instancia,solucao3))
print (makespan(instancia,solucao4))

#TODO ler os arquivos
listaArquivos = []
criterioParada2 = 0 #TODO definir o critério de parada

X = 0 #TODO definir o valor do x e se possível remover essa declaração

listaInstancias = lerInstancias(listaArquivos)
relatorio = [dict() for instancia in range(listaInstancias)]
for instancia in range (listaInstancias):
    tamanhoPop = X
    tempoMaximo = X
    #Para cada instância executar todo o algoritmo 10 vezes
    melhoresSolucoes = relatorio[instancia]
    for it in range (10):
        melhorSolucao = {'solucao':[], 'aptidao':sys.maxint, 'tempoFinal':0}
        tempoInicial = time.time()
        populacao = criarPopulacaoInicial(instancia, tamanhoPop)
        while True:
            if tempoMaximo <= time.time() - tempoInicial:
                break
            if criterioParada2:
                break
            aptidaoPop = avaliarPop(populacao)
            melhorSolucaoAtual = retornaMelhorSolucao(populacao, aptidaoPop)
            if melhorSolucao['aptidao'] > melhorSolucaoAtual['aptidao']:
                melhorSolucao = melhorSolucaoAtual
            populacaoSelecionada = selecionarPop(populacao, aptidaoPop)
            novasSolucoes = recombinacao(populacaoSelecionada)
            novasSolucoes = mutacao(novasSolucoes)
            populacao = selecionarNovaGeracao(populacao, novasSolucoes)
        melhorSolucao['tempoFinal'] = time.time() - tempoInicial
        print(melhorSolucao)
        melhoresSolucoes = melhoresSolucoes | melhorSolucao
    relatorio[instancia] = melhoresSolucoes
salvarRelatorio(relatorio)