import random

'''Exemplo de indivíduo
Aula de 1 dia apenas
4 aulas por dia
Não há aulas repetidas no mesmo dia
Aulas não podem ser simultâneas para um mesmo professor.
Aulas não podem ser simultâneas para uma mesma turma.
Cada sala deve ter apenas uma aula por vez.

[["1º Ano", 1º Horario, "Matemática", "Prof. A", "Sala 101"], 
["1º Ano", 2º Horario, "História", "Prof. B", "Sala 102"],
["1º Ano", 3º Horario, "Matemática", "Prof. C", "Sala 101"], 
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

# Dados das aulas
materias = ["Matemática", "Física", "Química", "Biologia", "História", "Geografia"]
turmas = ["1º Ano", "2º Ano", "3º Ano"]
professores = ["Prof. A", "Prof. B", "Prof. C", "Prof. D", "Prof. E", "Prof. F"]
salas = ["Sala 101", "Sala 102", "Sala 103", "Sala 104", "Sala 105", "Sala 106"]

# Constantes e parâmetros do experimento
NUM_DAYS = 5  # Número de dias na semana
NUM_PERIODS_PER_DAY = 4  # Número de períodos por dia
NUM_CLASSES = len(materias)  # Número de aulas (igual ao número de matérias)
POPULATION_SIZE = 10  # Tamanho da população de soluções
MIXING_NUMBER = 2  # Número de pais usados para cruzamento
MUTATION_RATE = 0.05  # Taxa de mutação

# Função de pontuação de aptidão - Quão boa é uma solução?
def fitness_score(schedule):
    score = 0
    for day in range(NUM_DAYS):
        for period in range(NUM_PERIODS_PER_DAY):
            current_class = schedule[day][period]
            if current_class is not None:
                current_turma = turmas[current_class % len(turmas)]
                current_professor = professores[current_class % len(professores)]
                current_sala = salas[current_class % len(salas)]
                for other_day in range(NUM_DAYS):
                    for other_period in range(NUM_PERIODS_PER_DAY):
                        if day == other_day and period == other_period:
                            continue
                        other_class = schedule[other_day][other_period]
                        if other_class is not None:
                            other_turma = turmas[other_class % len(turmas)]
                            other_professor = professores[other_class % len(professores)]
                            other_sala = salas[other_class % len(salas)]
                            if (current_turma == other_turma or 
                                current_professor == other_professor or 
                                current_sala == other_sala):
                                score -= 1  # Penaliza conflitos
    return score

# Função de seleção de pais com base na pontuação de aptidão
def selection(population):
    scores = [fitness_score(ind) for ind in population]
    total_score = sum(scores)
    if total_score == 0:  # Evitar divisão por zero
        probabilities = [1 / POPULATION_SIZE] * POPULATION_SIZE
    else:
        probabilities = [score / total_score for score in scores]
    parents = random.choices(population, weights=probabilities, k=POPULATION_SIZE)
    return parents

# Função de crossover - Combina características de cada solução usando um ponto de cruzamento
def crossover(parents):
    offsprings = []
    for _ in range(POPULATION_SIZE):
        parent1, parent2 = random.sample(parents, 2)
        cross_point = random.randint(0, NUM_DAYS * NUM_PERIODS_PER_DAY - 1)
        offspring = [None] * (NUM_DAYS * NUM_PERIODS_PER_DAY)
        offspring[:cross_point] = [parent1[i // NUM_PERIODS_PER_DAY][i % NUM_PERIODS_PER_DAY] for i in range(cross_point)]
        offspring[cross_point:] = [parent2[i // NUM_PERIODS_PER_DAY][i % NUM_PERIODS_PER_DAY] for i in range(cross_point, NUM_DAYS * NUM_PERIODS_PER_DAY)]
        offspring = [offspring[i:i + NUM_PERIODS_PER_DAY] for i in range(0, len(offspring), NUM_PERIODS_PER_DAY)]
        offsprings.append(offspring)
    return offsprings

# Função de mutação - Cria diversidade na população
def mutate(schedule):
    for day in range(NUM_DAYS):
        for period in range(NUM_PERIODS_PER_DAY):
            if random.random() < MUTATION_RATE:
                schedule[day][period] = random.randrange(NUM_CLASSES)
    return schedule

# Imprime a solução encontrada
def print_schedule(schedule):
    for day in range(NUM_DAYS):
        print(f"Dia {day + 1}:")
        for period in range(NUM_PERIODS_PER_DAY):
            class_index = schedule[day][period]
            if class_index is not None:
                print(f"  Período {period + 1}: {materias[class_index % len(materias)]}, {turmas[class_index % len(turmas)]}, {professores[class_index % len(professores)]}, {salas[class_index % len(salas)]}")
            else:
                print(f"  Período {period + 1}: Vago")
        print()

# Função para implementar a evolução
def evolution(population):
    parents = selection(population)
    offsprings = crossover(parents)
    offsprings = list(map(mutate, offsprings))
    new_gen = offsprings
    new_gen.extend(population)
    new_gen = sorted(new_gen, key=lambda ind: fitness_score(ind), reverse=True)[:POPULATION_SIZE]
    return new_gen

# Função para gerar a população inicial
def generate_population():
    population = []
    for _ in range(POPULATION_SIZE):
        schedule = [[random.randrange(NUM_CLASSES) for _ in range(NUM_PERIODS_PER_DAY)] for _ in range(NUM_DAYS)]
        population.append(schedule)
    return population

# Executa o experimento
generation = 0
population = generate_population()

while generation < 100:  # Define um limite para o número de gerações
    print(f'\nGeneration: {generation}')
    for i in range(POPULATION_SIZE):
        print(f'\nIndivíduo {i + 1}:')
        print_schedule(population[i])
    population = evolution(population)
    generation += 1
