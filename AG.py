import math
import random
from scipy import special as sc
import itertools

# Constantes e parâmetros do experimento
NUM_QUEENS = 8  # Número de rainhas (e o tamanho do tabuleiro NxN)
POPULATION_SIZE = 10  # Tamanho da população de soluções
MIXING_NUMBER = 2  # Número de pais usados para cruzamento
MUTATION_RATE = 0.05  # Taxa de mutação

# Função de pontuação de aptidão - Quão boa é uma solução?
def fitness_score(seq):
    score = 0  # Inicializa a pontuação

    for row in range(NUM_QUEENS):  # Itera por cada linha do tabuleiro
        col = seq[row]  # Coluna da rainha na linha atual

        for other_row in range(NUM_QUEENS):  # Itera por cada linha novamente para comparar as rainhas
            if other_row == row:  # Ignora a mesma rainha
                continue
            if seq[other_row] == col:  # Rainhas na mesma coluna
                continue
            if other_row + seq[other_row] == row + col:  # Rainhas na mesma diagonal
                continue
            if other_row - seq[other_row] == row - col:  # Rainhas na outra diagonal
                continue
            score += 1  # Incrementa a pontuação se as rainhas não se atacam

    return score / 2  # Divide por 2 para evitar duplicação de contagem de pares

# Função de seleção de pais com base na pontuação de aptidão
def selection(population):
    parents = []  # Lista para armazenar os pais selecionados

    for ind in population:  # Itera por cada indivíduo na população
        max_value = int(sc.comb(NUM_QUEENS, 2) * 2)  # Calcula o valor máximo para a seleção
        if random.randrange(max_value) < fitness_score(ind):  # Seleciona pais com base na aptidão
            parents.append(ind)  # Adiciona o indivíduo à lista de pais

    return parents  # Retorna a lista de pais selecionados

# Função de crossover - Combina características de cada solução usando um ponto de cruzamento
def crossover(parents):
    cross_points = random.sample(range(NUM_QUEENS), MIXING_NUMBER - 1)  # Pontos de cruzamento aleatórios
    offsprings = []  # Lista para armazenar os descendentes

    permutations = list(itertools.permutations(parents, MIXING_NUMBER))  # Todas as permutações possíveis dos pais

    for perm in permutations:  # Itera por cada permutação
        offspring = []  # Lista para o descendente atual

        start_pt = 0  # Índice inicial do subsegmento

        for parent_idx, cross_point in enumerate(cross_points):  # Itera por cada ponto de cruzamento
            parent_part = perm[parent_idx][start_pt:cross_point]  # Sublista do pai
            offspring.append(parent_part)  # Adiciona a sublista ao descendente
            start_pt = cross_point  # Atualiza o índice inicial

        last_parent = perm[-1]  # Último pai na permutação
        parent_part = last_parent[cross_point:]  # Sublista do último pai
        offspring.append(parent_part)  # Adiciona a sublista ao descendente

        offsprings.append(list(itertools.chain(*offspring)))  # Achata e adiciona o descendente à lista

    return offsprings  # Retorna a lista de descendentes

# Função de mutação - Cria diversidade na população
def mutate(seq):
    for row in range(len(seq)):  # Itera por cada posição na sequência
        if random.random() < MUTATION_RATE:  # Verifica se ocorre mutação
            seq[row] = random.randrange(NUM_QUEENS)  # Muda a posição da rainha aleatoriamente

    return seq  # Retorna a sequência mutada

# Imprime a solução encontrada
def print_found_goal(population, to_print=True):
    for ind in population:  # Itera por cada indivíduo na população
        score = fitness_score(ind)  # Calcula a pontuação de aptidão
        if to_print:
            print(f'{ind}. Score: {score}')  # Imprime a sequência e a pontuação
        if score == sc.comb(NUM_QUEENS, 2):  # Verifica se a solução é ótima
            if to_print:
                print('Solution found\n')  # Imprime que a solução foi encontrada
            return True  # Retorna True se a solução foi encontrada

    if to_print:
        print('Solution not found\n')  # Imprime que a solução não foi encontrada
    return False  # Retorna False se a solução não foi encontrada

# Função para implementar a evolução
def evolution(population):
    parents = selection(population)  # Seleciona os pais
    offsprings = crossover(parents)  # Realiza o crossover para criar descendentes
    offsprings = list(map(mutate, offsprings))  # Aplica mutação nos descendentes

    new_gen = offsprings  # Inicia a nova geração com os descendentes

    for ind in population:  # Adiciona os indivíduos da geração anterior
        new_gen.append(ind)

    # Ordena pela pontuação de aptidão e mantém apenas os melhores indivíduos
    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind), reverse=True)[:POPULATION_SIZE]

    return new_gen  # Retorna a nova geração

# Gera a população inicial (soluções)
def generate_population():
    population = []  # Lista para armazenar a população

    for individual in range(POPULATION_SIZE):  # Gera indivíduos aleatórios
        new = [random.randrange(NUM_QUEENS) for idx in range(NUM_QUEENS)]
        population.append(new)  # Adiciona o novo indivíduo à população

    return population  # Retorna a população inicial

# Executa o experimento
generation = 0  # Inicializa o contador de gerações

population = generate_population()  # Gera a população inicial

# Loop até encontrar a solução
while not print_found_goal(population):
    print(f'Generation: {generation}')  # Imprime o número da geração
    print_found_goal(population)  # Imprime a população e verifica se a solução foi encontrada
    population = evolution(population)  # Evolui a população para a próxima geração
    generation += 1  # Incrementa o contador de gerações
