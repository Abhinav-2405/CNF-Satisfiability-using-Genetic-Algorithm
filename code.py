from CNF_Creator import *
import random, time, math

cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence

population = []
initial = time.time()
pop_size = 20
maxFitness = 0
elitism_ratio = 0.6
bestModel = []
used_letters = set()
def generate_sentence(mVal):
    cnfC = CNF_Creator(n=50) # n is number of symbols in the 3-CNF sentence
    sentence = cnfC.CreateRandomSentence(m = mVal) # m is number of clauses in the 3-CNF sentence
    # print('Random sentence : ',sentence)
    # sentence = cnfC.ReadCNFfromCSVfile()
    # print('\nSentence from CSV file : ',sentence)
    return sentence


# print(f"Sentence length is {len(sentence)}")

sentence = generate_sentence(1) # generates the sentence

def generate_population(n, pop_size):

    print(pop_size, n)
    for i in range(0, pop_size):
        cur_list = []
        for _ in range(0, n):
            cur_list.append(bool(random.getrandbits(1)))
        population.append(cur_list)


#to change
generate_population(50, pop_size)


# print(used_letters)
def calculateFitness(state, sentence):
    mappings = {}
    for boolVal, digit in zip(state, range(1, 51)):
        mappings[digit] = boolVal
    
    cnt = 0
    for clause in sentence:
        curr = False
        for number in clause:
            if(number > 0):
                curr = curr or mappings[number]
            else:
                curr = curr or not mappings[-number]
            
        if(curr == True):
            cnt = cnt + 1
    
    numOfClauses = len(sentence)
    return 100*(cnt / numOfClauses)

def calculateWeights(population, sentence):
    weights = []
    for state in population:
        weights.append(calculateFitness(state, sentence))
    return weights

def mutate(child, probability):
    for i in range(0, len(child)):
        if (random.uniform(0, 1) > probability):
            child[i] = not child[i]
    return child
        
def ga(population):
    global maxFitness, bestModel
    while(True):
        if(time.time() - initial >= 45):
            return
        weights = calculateWeights(population, sentence)
        maxFitness = max(maxFitness, max(weights))

        parent_passed = math.floor(elitism_ratio*pop_size)
        children = pop_size - parent_passed
        temp = sorted(zip(weights, population), reverse = True)
        weights = [t[0] for t in temp]
        population = [t[1] for t in temp]
        bestModel = population[0]
        population2 = []
        for i in range(0, children):
            parent1, parent2 = weighted_random_choice(population, weights, 2)
            child = reproduce(parent1, parent2)

            #to change (add)
            
            if(maxFitness >= 100.0):
                # print(maxFitness)
                return
            child = mutate(child, 0.015)
            
            population2.append(child)

        population = population[ : parent_passed]
        population.extend(population2)
        
        #to change  (remove , then add)
        
        #if enough time has elapsed or some individual is good enough break

def weighted_random_choice(population, weights, num):
    n = len(weights)
    vals = [x  for x in range(0, n)]
    x = random.choices(population= vals, weights= weights, k = 1)
    y = random.choices(population= vals, weights= weights, k = 1)
    return [population[x[0]], population[y[0]]]

def reproduce(parent1, parent2):
    n = len(parent1)
    c = random.randint(0, n - 1)
    return parent1[: c - 1] + parent2[c - 1: ]

print("hello")
ga(population)
for i in range(0, pop_size):
    x = calculateFitness(population[i], sentence)
#   print(x)
    maxFitness = max(maxFitness, x)

# print(f"Max Fitness : {maxFitness}%")
ans = []
for val, boolVal in zip(range(1, 51), bestModel):
    if(boolVal == True):
        ans.append(val)
    else:
        ans.append(-val)

# print(ans)
# print(time.time() - initial)


pop_size = 20
elitism_ratio = 0.6
ans = []
time_ans = []
for m in range(100, 301, 20):
    tot = 0
    time_used = 0
    for i in range(0, 10):
        maxFitness = 0
        bestModel = []
        boolAns = []
        sentence = generate_sentence(m)  # m is number of clauses in the 3-CNF sentence
        initial = time.time()
        ga(population)

        time_used += time.time() - initial
        # print(f"Max Fitness : {maxFitness}%")
        for val, boolVal in zip(range(1, 51), bestModel):
            boolAns.append(boolVal)

        tot += maxFitness 
    tot /= 10
    time_used /= 10
    ans.append(tot)
    time_ans.append(time_used)
print(f"Avg is {tot}")
print(ans)
print(time_ans)
