#To run this project, esentially you must have this dependencies: pandas, numpy, xlsxwriter
#pip install pandas
#pip install numpy
#pip install xlsxwriter

import sys
import time
import random
import pandas as pd
import numpy as np


all_files = ['tai20_5.txt','tai20_10.txt','tai20_20.txt',
                     'tai50_5.txt','tai50_10.txt','tai50_20.txt',
                     'tai100_5.txt','tai100_10.txt','tai100_20.txt',
                     'tai200_10.txt'
            ] 

tamanhoPop = 100
mutation_rate = 5

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
def criarPopulacaoInicial(instance):
    return generate_random_solution(len(instance[0]), tamanhoPop)
     
#usar a função makespan para avalaiar a aptidão de cada elemento da população
def avaliarPop(population, instance):
    fitness_array = []
    for solution in population:
        fitness = makespan(instance, solution)
        if isinstance(fitness, str):
            fitness = sys.maxsize
        fitness_array.append(fitness)
    return fitness_array  
  
#retorna a melhor solucao dentre a populacao atual
def retornaMelhorSolucao(populacao, aptidaoPop):
    best = merge_list_into_tuple(aptidaoPop, populacao)[0]
    return {'solucao':best[1], 'aptidao':best[0], 'tempoFinal': 0}

#função deve retornar quais elementos serão recombinados e com quem (pode fazer uso da aptidao ou não para o critério de seleção)
def selecionarPop(populacao, aptidaoPop):
    selected_people = merge_list_into_tuple(aptidaoPop, populacao)
    return [i[1] for i in selected_people[:int(len(selected_people)/2)]] 

#generate random mumber as position
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
    if round(random.random(), 2) < mutation_rate / 100:
        for solution in novasSolucoes:
            rand_pos = get_random_pos(solution)
            while True:
                random_item = random.randint(1, len(solution))
                if random_item != solution[rand_pos]:
                    solution[rand_pos] = random_item
                    break         
    return novasSolucoes

#função deve criar uma nova população com as soluções novas (eliminando as antigas ou usando outro critério de seleção desejado)
def selecionarNovaGeracao(populacaoAtual, novasSolucoes):
    return [*generate_random_solution(len(populacaoAtual[0]), int(len(populacaoAtual) / 2)), *novasSolucoes]

def export_data(data):
    data = pd.DataFrame(data, index=[i for i in range(1,len(all_files)+1)])
 
    writer = pd.ExcelWriter('reports/flow_shop_report.xlsx', engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1')
    writer.save()
       
    data.to_csv('reports/flow_shop_report.csv')

    print('****** Reports created successfully ******')
      
#computar o lower bound, upper bound, valores médios e desvios (tanto para aptidão quanto para o tempo de execução) para cada instância
#salvar em formato de tabela (pode ser um CSV) em um arquivo
def salvarRelatorio(relatorios):
    instances_data, solutions = [], []
    lower_bound_f, upper_bound_f, mean_f, deviation_f = [], [], [], []
    lower_bound_t, upper_bound_t, mean_t, deviation_t = [], [], [], []
    
    for relatorio in relatorios:
        all_times = relatorio['all_times']
        all_fitness = relatorio['all_fitness']
                    
        solutions.append(relatorio['solucao'])
        
        lower_bound_f.append(round(min(all_fitness), 5))
        upper_bound_f.append(round(max(all_fitness),5))
        mean_f.append(round(np.mean(all_fitness), 5))
        deviation_f.append(round(np.std(all_fitness), 5))
        
        lower_bound_t.append(round(min(all_times), 5))
        upper_bound_t.append(round(max(all_times), 5))
        mean_t.append(round(np.mean(all_times), 5))
        deviation_t.append(round(np.std(all_times), 5))
        
        instances_data.append(f"({relatorio['n_jobs']} X {relatorio['n_machines']})")
    
    report_data = {
        'j X m ': instances_data, #características das instâncias ( jobs x machines)
        'Psize': [tamanhoPop for _ in range(len(all_files))], #tamanho da população usado para cada instância
        'sol': solutions,# as melhores soluções de cada instância
        'lbf': lower_bound_f, #o lower bound do fitness
        'ubf': upper_bound_f, # upper bound do fitness
        'mf': mean_f, #média do fitness
        'dpf': deviation_f, #desvio padrão do fitness
        'lbt': lower_bound_t, #lower bound do tempo
        'ubt': upper_bound_t, #upper bound do tempo
        'mt': mean_t, #média do tempo
        'dpt': deviation_t,#desvio padrão do tempo
    }
    export_data(report_data)

#for debugging structures
def format_print(data):
    print('\n'.join('{}: {}'.format(*val) for val in enumerate(data)))
   
def main():
    listaInstancias = lerInstancias(all_files)
    relatorio = [{} for _ in range(len(listaInstancias))]

    for instancia in listaInstancias:
        tempoMaximo = 1
        index_of_instance = listaInstancias.index(instancia)
            
        all_fitness, all_times = [], []
        best_of_all = {'solucao':[], 'aptidao':sys.maxsize, 'tempoFinal':0}
        
        for _ in range (10):
            melhorSolucao = {'solucao':[], 'aptidao':sys.maxsize, 'tempoFinal':0}
            tempoInicial = time.time()
            populacao = criarPopulacaoInicial(instancia)
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
            melhorSolucao['n_jobs'] = len(melhorSolucao['solucao'])
            melhorSolucao['n_machines'] = len(instancia)
           
            if melhorSolucao['aptidao'] < best_of_all['aptidao']:
                best_of_all = melhorSolucao
                
            best_of_all['all_fitness'] = all_fitness
            best_of_all['all_times'] = all_times    
        relatorio[index_of_instance] = best_of_all
    salvarRelatorio(relatorio)

if __name__ == "__main__":
    main()
