from numpy import zeros, array, concatenate

class Dynamic_algorithm_knapsack_problem:
    def __init__(self):
        pass

    def get_data(self, dataset, knapsack_capacity):
        """
        Function that gets data about knapsack and items

        Args:
            dataset (list): list of items - item: tuple - consist of two float numbers (value, weight)

        Attr:
            knapsack_capacity (float): maximum weight of items in knapsack
            num_of_elements (int): number of items
            values (list): values of items
            weights (list): weights of items
        """
        self.num_of_elements = len(dataset)
        values = []
        weights = []
        for val, wei in dataset:
            values.append(val)
            weights.append(wei * 100)
        self.weights = concatenate((zeros(1), array(weights)))
        self.values = concatenate((zeros(1), array(values)))
        self.knapsack_capacity = knapsack_capacity

    def solve_knapsack_problem(self):
        """
        Function that solves knapsack problem

        Return:
            (float): sum of the values of the items in the knapsack
        """
        A = zeros([self.num_of_elements + 1, (self.knapsack_capacity + 1) * 100])

        for i in range(1, self.num_of_elements + 1):
            for j in range(1, (self.knapsack_capacity + 1) * 100):
                if self.weights[i] > j:
                    A[i][j] = A[i - 1][j]
                else:
                    A[i][j] = max(A[i - 1][j], A[i - 1][j - int(self.weights[i])] + self.values[i])

        return A[self.num_of_elements][self.knapsack_capacity * 100]
