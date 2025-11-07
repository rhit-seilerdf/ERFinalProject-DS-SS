import numpy as np
import matplotlib.pyplot as plt

class Microbial():

    def __init__(self, fitnessFunction, popsize, genesize, recombProb, mutatProb, demeSize, generations):
        self.fitnessFunction = fitnessFunction
        self.popsize = popsize
        self.genesize = genesize
        self.recombProb = recombProb
        self.mutatProb = mutatProb
        self.demeSize = int(demeSize/2)
        self.generations = generations
        self.tournaments = generations*popsize
        self.pop = np.random.rand(popsize,genesize)*2 - 1
        self.fitness = np.zeros(popsize)
        self.avgHistory = np.zeros(generations)
        self.bestHistory = np.zeros(generations)
        self.gen = 0

    def showFitness(self):
        plt.plot(self.bestHistory)
        plt.plot(self.avgHistory)
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.title("Best and average fitness")
        plt.show()
        return self.bestHistory

    def fitStats(self):
        self.bestind = self.pop[np.argmax(self.fitness)]
        bestfit = np.max(self.fitness)
        avgfit = np.mean(self.fitness)
        print(self.gen,": ",avgfit," ",bestfit)
        self.avgHistory[self.gen]=avgfit
        self.bestHistory[self.gen]=bestfit
        return avgfit, bestfit, self.bestind

    def run(self):
        # Calculate all fitness once
        for i in range(self.popsize):
            self.fitness[i] = self.fitnessFunction(self.pop[i])[0]
        # Evolutionary loop
        for g in range(self.generations):
            self.gen = g
            # Report statistics every generation
            self.fitStats()
            for i in range(self.popsize):
                # Step 1: Pick 2 individuals
                a = np.random.randint(0,self.popsize-1)
                b = np.random.randint(a-self.demeSize,a+self.demeSize-1)%self.popsize   ### Restrict to demes
                while (a==b):   # Make sure they are two different individuals
                    b = np.random.randint(a-self.demeSize,a+self.demeSize-1)%self.popsize   ### Restrict to demes
                # Step 2: Compare their fitness
                if (self.fitness[a] > self.fitness[b]):
                    winner = a
                    loser = b
                else:
                    winner = b
                    loser = a
                # Step 3: Transfect loser with winner 
                r = np.random.random(self.genesize)
                newind = np.array([self.pop[winner][k] if r[k] >= self.recombProb else self.pop[loser][k] for k in range(self.genesize)])
                self.pop[loser] = newind
                # Step 4: Mutate loser and make sure new organism stays within bounds
                self.pop[loser] += np.random.normal(0.0,self.mutatProb,size=self.genesize)
                self.pop[loser] = np.clip(self.pop[loser],-1,1)
                # Step 5: Update fitness
                self.fitness[winner] = self.fitnessFunction(self.pop[winner])[0]
                self.fitness[loser] = self.fitnessFunction(self.pop[loser])[0]
