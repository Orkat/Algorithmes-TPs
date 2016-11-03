from random import randint
import matplotlib.pyplot as plt

def fill_hash_table(n, k):
    hash_table = []
    for i in range(0, n):
        hash_table.append([])
    for i in range(0, k):
        hash_table[randint(0, n-1)].append(i)
    return hash_table


def get_collision_histogram(hash_table):
    ret = []
    for row in hash_table:
        row_length = len(row)
        while (row_length > len(ret) - 1):
            ret.append(0)
        ret[row_length] += 1
    return ret


def get_n_elements_without_collisions(hash_table):
    ret = 0
    for row in hash_table:
        if len(row) == 1:
            ret += 1
    return ret


def get_none_collision_table(N, K):
    values = []
    for k in range(0, K):
        hash_table = fill_hash_table(N, k)
        values.append(get_n_elements_without_collisions(hash_table))
    return values


def plot_number_of_no_collisions(N, K):
    values = get_none_collision_table(N, K)
    plt.figure(figsize=(20,10))
    plt.plot(values)
    plt.show()
    return values


def get_theoretical_none_collision_table(N, K):
    values = []
    for k in range(0, K):
        values.append(k*(1 - 1/float(N))**(k-1))
    return values


def plot_empirical_and_theoretical_no_collisions(N, K, empirical_values):
    theoretical_values = get_theoretical_none_collision_table(N, K)
    plt.figure(figsize=(20,10))
    plt.plot(empirical_values)
    lines = plt.plot(theoretical_values)
    plt.setp(lines, linewidth=5, color='black')
    plt.show()
    return theoretical_values


def get_n_rows_with_p_elements(hash_table, p):
    ret = 0
    for row in hash_table:
        if len(row) == p:
            ret += 1
    return ret


def get_n_rows_with_collision(hash_table):
    ret = 0
    for row in hash_table:
        if len(row) >= 2:
            ret += 1
    return ret


def get_p_collision_table(N, K, p):
    values = []
    for k in range(0, K):
        hash_table = fill_hash_table(N, k)
        values.append(get_n_rows_with_p_elements(hash_table, p))
    return values


def get_at_least_one_collision_table(N, K):
    values = []
    for k in range(0, K):
        hash_table = fill_hash_table(N, k)
        values.append(get_n_rows_with_collision(hash_table))
    return values


def get_list_collision_table(N, K, P):
    ret = []
    for p in range(1, P+1):
        ret.append(get_p_collision_table(N, K, p))
    return ret


def factorial(n):
    ret = 1
    for i in range(1, n + 1):
        ret *= i
    return ret


def binomial(n, p):
    return factorial(n)/(factorial(n - p)*factorial(p))


def get_theoretical_at_least_one_collision_table(N, K):
    values = []
    for k in range(0, K):
        values.append(N - N*(1.0 - 1.0/float(N))**(k) - k*(1.0 - 1.0/float(N))**(k-1) )
    return values

def get_theoretical_p_collision_table(N, K, p):
    values = []
    for k in range(0, K):
        values.append(binomial(k, p)*((1/float(N))**(p-1))*(1 - 1/float(N))**(k-p))
    return values


def get_theoretical_list_collision_table(N, K, P):
    ret = []
    for p in range(1, P+1):
        ret.append(get_theoretical_p_collision_table(N, K, p))
    return ret


def plot_empirical_and_theoretical_p_collisions(N, K, P):

    empirical_values = get_list_collision_table(N, K, P)
    theoretical_values = get_theoretical_list_collision_table(N, K, P)

    plt.figure(figsize=(20,10))

    for p in range(0, P):
        plt.plot(empirical_values[p])
        lines = plt.plot(theoretical_values[p])
        plt.setp(lines, linewidth=5, color='green')

    plt.show()

    return empirical_values, theoretical_values


def plot_empirical_at_least_one_collision(N, K):

    empirical_values = get_at_least_one_collision_table(N, K)
    theoretical_values = get_theoretical_at_least_one_collision_table(N, K)

    plt.figure(figsize=(20,10))

    plt.plot(empirical_values)
    lines = plt.plot(theoretical_values)
    plt.setp(lines, linewidth=5, color='black')

    plt.show()

    return empirical_values, theoretical_values

def get_dictionary_set(filename):

    dictionary = set()
    text_file = open(filename)

    lines = text_file.readlines()
    for line in lines:
        for word in line.split(' '):
            if word != '':
                dictionary.add(word)

    return dictionary



def fill_hash_table_dictionary(N, dictionary, hash_function):

    hash_table = []
    for i in range(0, N):
        hash_table.append([])

    for string in list(dictionary):
        hashed_string = hash_function(string, N)
        hash_table[hashed_string].append(string)

    return hash_table

def plot_hash_table_dictionary(dictionary, hash_function, initial, step, final):

    values = []
    i = initial
    while i < final :
        hash_table = fill_hash_table_dictionary(i, dictionary, hash_function)
        values.append(get_n_rows_with_collision(hash_table))
        i += step

    plt.figure(figsize=(20,10))
    plt.plot(values)
    plt.show()
