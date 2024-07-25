'''Exemplo de indivíduo
Aula de 1 dia apenas
4 aulas por dia
Não há aulas repetidas no mesmo dia
Aulas não podem ser simultâneas para um mesmo professor.
Aulas não podem ser simultâneas para uma mesma turma.
Cada sala deve ter apenas uma aula por vez.
Turma [0] e Horario [1] não seram alterados
Algoritmo mudará somente matéria[2], professor[3] e sala[4]

[["1º Ano", 1º Horario, "Matemática", "Prof. A", "Sala 101"], 
["1º Ano", 2º Horario, "História", "Prof. B", "Sala 102"],
["1º Ano", 3º Horario, "Geografia", "Prof. C", "Sala 101"], 
["1º Ano", 4º Horario, "Química", "Prof. D", "Sala 103"],
["2º Ano", 1º Horario, "História", "Prof. E", "Sala 105"], 
["2º Ano", 2º Horario, "Geografia", "Prof. F", "Sala 106"],
["2º Ano", 3º Horario, "Física", "Prof. A", "Sala 105"], 
["2º Ano", 4º Horario, "Biologia", "Prof. B", "Sala 106"],
["3º Ano", 1º Horario, "Química", "Prof. C", "Sala 103"], 
["3º Ano", 2º Horario, "Biologia", "Prof. D", "Sala 104"]]
["3º Ano", 3º Horario, "Física", "Prof. E", "Sala 103"],
["3º Ano", 4º Horario, "Geografia", "Prof. F", "Sala 104"]]
'''


import random
import itertools
from scipy import special as sc
import pprint

# Constantes e parâmetros do experimento
NUM_CLASSES = 3  # Número de turmas (1º Ano, 2º Ano, 3º Ano)
NUM_PERIODS = 4  # Número de horários por dia (1º Horário, 2º Horário, 3º Horário, 4º Horário)
POPULATION_SIZE = 10  # Tamanho da população de soluções
MIXING_NUMBER = 2  # Número de pais usados para cruzamento
MUTATION_RATE = 0.05  # Taxa de mutação

# Listas de disciplinas, professores e salas
subjects = ["Matemática", "História", "Geografia", "Química", "Física", "Biologia"]
teachers = ["Prof. A", "Prof. B", "Prof. C", "Prof. D", "Prof. E", "Prof. F"]
rooms = ["Sala 101", "Sala 102", "Sala 103", "Sala 104", "Sala 105", "Sala 106"]

# Função de pontuação de aptidão - Quão boa é uma solução?
def fitness_score(schedule):
    conflicts = 0

    for class_index in range(NUM_CLASSES):
        seen_subjects = set()

        for period in range(NUM_PERIODS):
            subject = schedule[class_index][period][0]

            if subject in seen_subjects:
                conflicts += 1  # Conflito se a mesma disciplina aparece mais de uma vez para a mesma turma
            seen_subjects.add(subject)

    for period in range(NUM_PERIODS):
        seen_teachers = set()
        seen_rooms = set()
        seen_subjects = set()

        for class_index in range(NUM_CLASSES):
            subject = schedule[class_index][period][0]
            teacher = schedule[class_index][period][1]
            room = schedule[class_index][period][2]

            if subject in seen_subjects:
                conflicts += 1  # Conflito se a mesma disciplina está sendo ensinada ao mesmo tempo em diferentes turmas
            if teacher in seen_teachers:
                conflicts += 1  # Conflito se o mesmo professor está dando mais de uma aula ao mesmo tempo
            if room in seen_rooms:
                conflicts += 1  # Conflito se a mesma sala está sendo usada para mais de uma aula ao mesmo tempo

            seen_subjects.add(subject)
            seen_teachers.add(teacher)
            seen_rooms.add(room)

    return -conflicts  # Queremos minimizar os conflitos

# Função de seleção de pais com base na pontuação de aptidão
def selection(population):
    parents = []
    min_score = min(fitness_score(ind) for ind in population)
    normalized_scores = [(fitness_score(ind) - min_score + 1) for ind in population]  # Normaliza os scores para serem positivos

    for ind, norm_score in zip(population, normalized_scores):
        if random.randrange(0, max(normalized_scores)) < norm_score:
            parents.append(ind)
    return parents

# Função de crossover - Combina características de cada solução usando um ponto de cruzamento
def crossover(parents):
    cross_points = random.sample(range(NUM_PERIODS), MIXING_NUMBER - 1)
    offsprings = []
    permutations = list(itertools.permutations(parents, MIXING_NUMBER))

    for perm in permutations:
        offspring = []
        start_pt = 0
        for parent_idx, cross_point in enumerate(cross_points):
            for class_index in range(NUM_CLASSES):
                parent_part = perm[parent_idx][class_index][start_pt:cross_point]
                if len(offspring) <= class_index:
                    offspring.append(parent_part)
                else:
                    offspring[class_index].extend(parent_part)
            start_pt = cross_point

        for class_index in range(NUM_CLASSES):
            last_parent = perm[-1][class_index]
            parent_part = last_parent[start_pt:]
            offspring[class_index].extend(parent_part)

        offsprings.append(offspring)

    return offsprings

# Função de mutação - Cria diversidade na população
def mutate(schedule):
    for class_index in range(NUM_CLASSES):
        for period in range(NUM_PERIODS):
            if random.random() < MUTATION_RATE:
                schedule[class_index][period] = [
                    random.choice(subjects),
                    random.choice(teachers),
                    random.choice(rooms)
                ]
    return schedule

# Imprime a solução encontrada
def print_found_goal(population, to_print=True):
    for ind in population:
        score = fitness_score(ind)
        if to_print:
            print('\nSchedule:')
            pprint.pprint(ind)
            print(f'Score: {score}')
        if score == 0:  # Sem conflitos
            if to_print:
                print('Solution found\n')
            return True
    if to_print:
        print('Solution not found\n')
    return False

# Função para implementar a evolução
def evolution(population):
    parents = selection(population)
    offsprings = crossover(parents)
    offsprings = list(map(mutate, offsprings))

    new_gen = offsprings + population
    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind), reverse=True)[:POPULATION_SIZE]

    return new_gen

# Gera a população inicial (soluções)
def generate_population():
    population = []
    for _ in range(POPULATION_SIZE):
        schedule = []
        for _ in range(NUM_CLASSES):
            class_schedule = []
            for _ in range(NUM_PERIODS):
                class_schedule.append([
                    random.choice(subjects),
                    random.choice(teachers),
                    random.choice(rooms)
                ])
            schedule.append(class_schedule)
        population.append(schedule)
    return population

# Executa o experimento
generation = 0
population = generate_population()

# Loop até encontrar a solução
while not print_found_goal(population):
    print(f'Generation: {generation}')
    print_found_goal(population)
    population = evolution(population)
    generation += 1
