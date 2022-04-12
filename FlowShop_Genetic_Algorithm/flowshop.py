
import sys
import time
import random
from pandas import DataFrame
import numpy as np


allFiles = ['tai20_5.txt','tai20_10.txt','tai20_20.txt',
                     #'tai50_5.txt','tai50_10.txt','tai50_20.txt',
                     #'tai100_5.txt','tai100_10.txt','tai100_20.txt',
                     #'tai200_10.txt'
            ] 

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

def cleanFilterInstance(value):
    if value != '' and value != ' ':
        return int(value)

def getFirstInstanceOfFile(file):
    firstInstance = [];
    for index, line in enumerate(list(open(file))):
        if index <= 2: continue
        if index > 2 and line.startswith('number'):
            break
        firstInstance.append(list(map(lambda a: int(a),filter(cleanFilterInstance,line.strip().split(" ")))))   
    return firstInstance 

def merge_list_into_tuple(key_list, list_value):
    return sorted(list(zip(key_list, list_value)))

#ler a primeira instância de cada um dos dez arquivos, armazenar em uma lista e retornar essa lista
def lerInstancias(files):
    return [getFirstInstanceOfFile(file) for file in files]

def generate_random_solution(size_of_solution, number_of_solutions):
    return [random.sample(range(1, size_of_solution+1), size_of_solution) for _ in range(number_of_solutions)]
    
#criar uma lista de soluções aleatórias (podem definir outro critério se desejarem) com o tamanho repassado
def criarPopulacaoInicial(instance, size):
    return generate_random_solution(len(instance[0]), size)
     
#usar a função makespan para avalaiar a aptidão de cada elemento da população
def avaliarPop(population, instance):
    fitness_array = []
    for solution in population:
        fitness = makespan(instance, solution)
        if isinstance(fitness, str):
            fitness = sys.maxsize
        fitness_array.append(fitness)
    return fitness_array  
    #return [makespan(instance, solution) for solution in population]

#retorna a melhor solucao dentre a populacao atual
def retornaMelhorSolucao(populacao, aptidaoPop):
    best = merge_list_into_tuple(aptidaoPop, populacao)[0]
    return {'solucao':best[1], 'aptidao':best[0], 'tempoFinal': 0}

#função deve retornar quais elementos serão recombinados e com quem (pode fazer uso da aptidao ou não para o critério de seleção)
def selecionarPop(populacao, aptidaoPop):
    selected_people = merge_list_into_tuple(aptidaoPop, populacao)
    return [i[1] for i in selected_people[:int(len(selected_people)/2)]] 

def get_random_pos(list_):
    return random.randrange(len(list_))
    
#função deve usar o operador de recombinacao (definido pelo grupo_ para gerar novas soluções filhas)
def recombinacao(populacaoSelecionada):
    solutions = []
    for i in range(0,len(populacaoSelecionada) - 1, 2):
        current_solution = populacaoSelecionada[i]
        next_solution = populacaoSelecionada[i+1]
        random_pos = get_random_pos(current_solution)
        #to concatenate two list ex: res = [*l1, *l2]
        solutions.extend([[*current_solution[:random_pos], *next_solution[random_pos:]], [*next_solution[:random_pos], *current_solution[random_pos:]]]) 
    return solutions

#função deve usar o operador de mutacao (definido pelo grupo) para modificar as soluções filhas (não precisa ser todas)
def mutacao(novasSolucoes):
    mutation_rate = 1 / 100
    for solution in novasSolucoes:
        rand_pos = get_random_pos(solution)
        current_item = solution
        while True:
            random_item = random.randint(1, len(solution))
            if random_item != current_item:
                solution[rand_pos] = random_item
                break
    return novasSolucoes

#função deve criar uma nova população com as soluções novas (eliminando as antigas ou usando outro critério de seleção desejado)
def selecionarNovaGeracao(populacaoAtual, novasSolucoes):
    return [*generate_random_solution(len(populacaoAtual[0]), int(len(populacaoAtual) / 2)), *novasSolucoes]
    
#computar o lower bound, upper bound, valores médios e desvios (tanto para aptidão quanto para o tempo de execução) para cada instância
#salvar em formato de tabela (pode ser um CSV) em um arquivo
def salvarRelatorio(relatorios):
    solutions = []
    lower_bound_f, upper_bound_f, mean_f, deviation_f = [], [], [], []
    lower_bound_t, upper_bound_t, mean_t, deviation_t = [], [], [], []
    
    for relatorio in relatorios:
        all_fitness = relatorio['all_fitness']
        all_times = relatorio['all_times']
        
        solutions.append(relatorio['solucao'])
        
        lower_bound_f.append(min(all_fitness))
        upper_bound_f.append(max(all_fitness))
        mean_f.append(np.mean(all_fitness))
        deviation_f.append(float("{:.5f}".format(np.std(all_fitness))))
        
        lower_bound_t.append(min(all_times))
        upper_bound_t.append(max(all_times))
        mean_t.append(np.mean(all_times))
        deviation_t.append(float("{:.5f}".format(np.std(all_times))))
    
    report_data = {
        'solutions': solutions,
        'lower_bound_f': lower_bound_f,
        'upper_bound_f': upper_bound_f,
        'mean_f': mean_f,
        'deviation_f': deviation_f,
        'lower_bound_t': lower_bound_t,
        'upper_bound_t': upper_bound_t,
        'mean_t': mean_t,
        'deviation_t': deviation_t,
    }
    

    res = DataFrame(report_data)
    print(res)

def format_print(data):
    print('\n'.join('{}: {}'.format(*val) for val in enumerate(data)))
   
def main():
    listaInstancias = lerInstancias(allFiles)
    relatorio = [{} for _ in range(len(listaInstancias))]

    for instancia in listaInstancias:
        tamanhoPop = 100
        tempoMaximo = 1
        index_of_instance = listaInstancias.index(instancia)
        melhoresSolucoes = relatorio[index_of_instance]
        
        all_fitness, all_times = [], []
        best_aof_all = {'solucao':[], 'aptidao':sys.maxsize, 'tempoFinal':0}
        for _ in range (10):
            melhorSolucao = {'solucao':[], 'aptidao':sys.maxsize, 'tempoFinal':0}
            tempoInicial = time.time()
            populacao = criarPopulacaoInicial(instancia, tamanhoPop)
            criterioParada2 = 1
            while True:
                if tempoMaximo <= time.time() - tempoInicial:
                    break
                               
                aptidaoPop = avaliarPop(populacao, instancia)
                melhorSolucaoAtual = retornaMelhorSolucao(populacao, aptidaoPop)
                
                prev_fitness = melhorSolucao['aptidao']
                if melhorSolucao['aptidao'] > melhorSolucaoAtual['aptidao']:
                    melhorSolucao = melhorSolucaoAtual  
                
                if melhorSolucao['aptidao'] == prev_fitness:
                    criterioParada2 += 1
                else: criterioParada2 = 0    
                
                populacaoSelecionada = selecionarPop(populacao, aptidaoPop)
                novasSolucoes = recombinacao(populacaoSelecionada)
                novasSolucoes = mutacao(novasSolucoes)
                populacao = selecionarNovaGeracao(populacao, novasSolucoes)
               
                if criterioParada2 == 10: #critério de parada a ser definida
                    break
                
            melhorSolucao['tempoFinal'] =  float("{:.5f}".format(time.time() - tempoInicial))
            all_fitness.append(melhorSolucao['aptidao'])
            all_times.append(melhorSolucao['tempoFinal'])   
            
            if melhorSolucao['aptidao'] < best_aof_all['aptidao']:
                best_aof_all = melhorSolucao
                 
            best_aof_all['all_fitness'] = all_fitness
            best_aof_all['all_times'] = all_times   
        relatorio[index_of_instance] = best_aof_all
    salvarRelatorio(relatorio)

if __name__ == "__main__":
    main()
