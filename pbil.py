from numpy import array, empty
from random import random
from math import isclose, log

class PBIL_knapsack_problem:
    def __init__(self, lr=0.1, N=100, M=200, num_of_iter=1000, mut_prob=0.01, mut_shift=0.005, penalty_rate=140):
        """
        Attr:
            lr (float): learning rate
            N (int): size of population after selection
            M (int): size of population before selection
            num_of_iter (int): Number of iterations
            mut_prob (float): Probability of each element in solution mutation
            mut_shift (float): Scale of mutation
            penalty_rate(float): Scale of the penalty function
            num_of_elements (int): number of items
            values (list): values of items
            weights (list): weights of items
            knapsack_capacity (float):
        """
        self.lr = lr
        self.N = N
        self.M = M
        self.num_of_iter = num_of_iter
        self.mut_prob = mut_prob
        self.mut_shift = mut_shift
        self.penalty_rate = penalty_rate

    def get_data(self, dataset, knapsack_capacity):
        """
        Function that gets data about knapsack and items

        Args:
            dataset (list): list of items - item: tuple - consist of two float numbers (value, weight)
            knapsack_capacity (float): maximum weight of items in knapsack
        """
        self.num_of_elements = len(dataset)
        self.values = []
        self.weights = []
        for val, wei in dataset:
            self.values.append(val)
            self.weights.append(wei)
        self.knapsack_capacity = knapsack_capacity

    def solve_knapsack_problem(self):
        """
        Function that solves knapsack problem

        Return:
            (float): sum of the values of the items in the knapsack
        """
        probability_vec = empty(self.num_of_elements)
        probability_vec.fill(0.5)

        for _ in range(self.num_of_iter):
            if self.is_stop_condition(probability_vec):
                break
            population_P = empty([self.M, self.num_of_elements])
            for member in population_P:
                for i in range(self.num_of_elements):
                    if random() < probability_vec[i]:
                        member[i] = 1
                    else:
                        member[i] = 0
            population_O = self.selection(population_P)
            population_O = population_O.T

            for i, prob in enumerate(probability_vec):
                probability_vec[i] = (1 - self.lr) * prob + self.lr * sum(population_O[i]) / self.N

            self.mutation(probability_vec)

        return self.get_best_from_population(probability_vec)

    def get_best_from_population(self, solution):
        """
        Function that creates final population in the algorythm cycle
            the best is chosen as the answer of the knapsack problem

        Args:
            solution (array): list containing info whether items are in the knapsack
        Return:
            (float): sum of the values of the items in the best knapsack
        """
        population_P = empty([self.M, self.num_of_elements])
        for member in population_P:
            for i in range(self.num_of_elements):
                if random() < solution[i]:
                    member[i] = 1
                else:
                    member[i] = 0
        population_O = self.selection(population_P)

        return self.calculate_quality(population_O[0], final=True)


    def is_stop_condition(self, probability_vec):
        """
        Function that checks if all values of probability_vec is close to 0 or 1

        Args:
            probability_vec (list): list contains probability of putting items into knapsack

        Return:
            (bool): True if all values of probability_vec is close to 0 or 1, else False
        """
        for prob in probability_vec:
            if not (isclose(prob, 0) or isclose(prob, 1)):
                return False
        return True

    def selection(self, population):
        """
        Function that selects the best solutions based on a threshold selection

        Args:
            population (array): list contains solutions of the knapsack problem

        Return:
            (array): list contains N best solutions from population
        """
        population_with_quality = []
        selected_population = []

        for memeber in population:
            quality = self.calculate_quality(memeber)
            population_with_quality.append((quality, memeber))

        population_with_quality.sort(reverse=True, key=lambda x: x[0])
        for i in range(self.N):
            selected_population.append(population_with_quality[i][1])

        return array(selected_population)

    def calculate_quality(self, solution, final=False):
        """
        Function that calculates the quality of solution

        Args:
            solution (array): list containing info whether items are in the knapsack
            final (bool): says if its last calculation before return a solution

        Return:
            (float): sum of the values of the items in the knapsack
        """
        total_weight = 0
        total_value = 0
        for i in range(self.num_of_elements):
            if isclose(1, solution[i]):
                total_weight += self.weights[i]
                total_value += self.values[i]
        if total_weight > self.knapsack_capacity:
            if final:
                return self.return_valid_solution(solution, total_weight, total_value)
            return total_value - self.penalty_function(total_weight)
        else:
            return total_value

    def return_valid_solution(self, solution, total_weight, total_value):
        """
        Function that returns valid knapsack if the capasity is exceeded
            takes out item by item until the weight limit is fulfilled

        Args:
            solution (array): list containing info whether items are in the knapsack
            total_weight (float): weight of overloaded knapsack
            total_value (float): value of overloaded knapsack
        Return:
            (float): value of valid knapsack
        """
        i = 0
        while(total_weight > self.knapsack_capacity):
            solution[i] = 0
            total_weight -= self.weights[i]
            total_value -= self.values[i]
            i += 1
        return total_value

    def penalty_function(self, total_weight):
        """
        Function that penalizes the solution where the sum of the weights is greater than
            the capacity of the backpack

        Args:
            total_weight (float): sum of the weights

        Return:
            (float): penalty based on the logarithm of overcapacity
        """
        return log(total_weight - self.knapsack_capacity + 1) * self.penalty_rate

    def mutation(self, probability_vec):
        """
        Function that mutates solution

        Args:
            probability_vec (list): list contains probability of putting items into knapsack
        """
        for i, prob in enumerate(probability_vec):
            if random() < self.mut_prob:
                random_prob = 1 if (random() > 0.5) else 0
                probability_vec[i] = (1 - self.mut_shift) * prob + self.mut_shift * random_prob
