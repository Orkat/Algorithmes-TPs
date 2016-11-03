import random
import os
import sys
import json
import math

import matplotlib.pyplot as plt

def strip_non_alpha_non_space(s):
    ret_string = ""
    for c in s:
        if ord(c) == 32 or (ord(c) >= 65 and ord(c) <= 90) or (ord(c) >= 97 and ord(c) <= 122):
            ret_string += c
    return ret_string

class File_word_stream:

    def __init__(self, filename):

        self.words = []
        self.process_file(filename)


    def process_file(self, filename):

        f = open(filename)
        lines = f.readlines()
        n_lines = len(lines)
        i = 0
        for line in lines:
            lowercase_line = strip_non_alpha_non_space(line)
            for word in lowercase_line.split(' '):
                if word != '':
                    self.words.append(word)
            i += 1


    def get_words(self):

        return self.words


class WordCount:

    def __init__(self, word_stream):

        self.wordcount = {}
        for word in word_stream.get_words():
            if word not in self.wordcount:
                self.wordcount[word] = 1
            else:
                self.wordcount[word] += 1


    def get_wordcount(self):

        return self.wordcount


    def get_clipped_values(self):

        values = []
        for key, value in self.wordcount.items():
            values.append(value)
        values = sorted(values)
        reversed_values = values[::-1]

        clipped_values = []
        for i in range(100):
            clipped_values.append(reversed_values[i])

        return clipped_values


    def plot_wordcount_histogram(self):

        clipped_values = self.get_clipped_values()
        plt.plot(clipped_values)
        plt.show()

'''
_memomask = {}

def hash_function(n):
     mask = _memomask.get(n)

     if mask is None:
         random.seed(n)
         mask = _memomask[n] = random.getrandbits(32)

     def myhash(x):
         return hash(x) ^ mask
     return myhash
'''

def hash_function(n):

    def myhash(x):
        return hash(str(x) + str(n))
    return myhash

class CountMinSketch:

    def __init__(self, d, w):

        self.d = d
        self.w = w

        self.hash_functions = []
        for i in range(0, d):
            self.hash_functions.append(hash_function(i))

        self.matrix = []
        for i in range(0,d):
            self.matrix.append([])
            for j in range(0, w):
                self.matrix[i].append(0)


    def count_word(self, word, conservative=False):

        if conservative:

            min_i = None
            min_j = None
            min_value = None

            for i in range(0, self.d):

                hash_value = self.hash_functions[i](word) % self.w
                value = self.matrix[i][hash_value]

                if min_value is None:
                    min_i = i
                    min_j = hash_value
                    min_value = value

                elif value < min_value:
                    min_i = i
                    min_j = hash_value
                    min_value = value

            self.matrix[min_i][min_j] += 1

        else:
            for i in range(0, self.d):
                hash_value = self.hash_functions[i](word) % self.w
                self.matrix[i][hash_value] += 1



    def print_matrix(self):

        for i in range(0, self.d):
            for j in range(0, self.w):
                print(self.matrix[i][j], end = '')
                if j < self.w - 1:
                    print(" ", end = '')
                else:
                    print("")


    def from_word_stream(self, word_stream, conservative = False, verbose = False):

        words = word_stream.get_words()
        i = 0
        tick = 5*int(len(words)/100)
        k = 0
        for word in words:
            self.count_word(word, conservative)
            if verbose and i % tick == 0 :
                print(str(k) + " %")
                k += 5
            i += 1


    def estimate_count(self, word, verbose=False):

        values = []
        for i in range(0, self.d):
            hash_value = self.hash_functions[i](word) % self.w

            if verbose:
                print("hash value " + str(i) + " : " + str(hash_value))

            values.append(self.matrix[i][hash_value])

        if verbose:
            print(values)

        return min(values)


    def root_mean_squared_error(self, word_count, verbose=False):

        wordcount = word_count.get_wordcount()
        N = len(wordcount)
        buff = 0.0
        i = 0
        tick = int(N/100)
        k = 0
        for key, value in wordcount.items():
            xi = self.estimate_count(key)
            yi = value
            buff += float((xi - yi)*(xi - yi))
            if verbose and i % tick == 0 :
                print(str(k) + " %")
                k += 1
            i += 1
        buff = math.sqrt(buff)
        buff /= float(N)
        return buff


    def average_relative_error(self, word_count):

        wordcount = word_count.get_wordcount()
        N = len(wordcount)
        buff = 0.0
        for key, value in wordcount.items():
            xi = self.estimate_count(key)
            yi = value
            buff += float((xi - yi)*(xi - yi))/float(yi)
        buff = math.sqrt(buff)
        buff /= float(N)
        return buff


class ErrorBenchmark:

    def __init__(self, filename, min_d, max_d, min_w, max_w):

        self.filename = filename

        if os.path.exists(filename):
            f = open(filename, 'r')
            lines = f.readlines()

            json_data = json.loads(lines[0])
            self.min_d = json_data['min_d']
            self.max_d = json_data['max_d']
            self.min_w = json_data['min_w']
            self.max_w = json_data['max_w']

            self.values = []
            for i in range(1, len(lines)):
                json_data = json.loads(lines[i])
                d = int(json_data['d'])
                w = int(json_data['w'])
                rms = float(json_data['rms'])
                are = float(json_data['are'])
                self.values.append([d, w, rms, are])

        else:

            self.min_d = min_d
            self.max_d = max_d
            self.min_w = min_w
            self.max_w = max_w

            self.values = []

            self.write_file()


    def write_file(self):

        f = open(self.filename, 'w')

        json_data = {}
        json_data['min_d'] = self.min_d
        json_data['max_d'] = self.max_d
        json_data['min_w'] = self.min_w
        json_data['max_w'] = self.max_w

        f.write(json.dumps(json_data) + '\n')

        for element in self.values:
            json_data = {}
            json_data['d'] = element[0]
            json_data['w'] = element[1]
            json_data['rms'] = element[2]
            json_data['are'] = element[3]

            f.write(json.dumps(json_data) + '\n')


        f.close()


    def append_element_to_file(self, element):

        f = open(self.filename, 'a')

        json_data = {}
        json_data['d'] = element[0]
        json_data['w'] = element[1]
        json_data['rms'] = element[2]
        json_data['are'] = element[3]

        f.write(json.dumps(json_data) + '\n')

        f.close()


    def run_benchmark(self, word_stream, word_count, conservative=False):

        for element in self.values:
            d = element[0]
            w = element[1]
            print("benchmark already run for d=" + str(d) + " , w=" + str(w))


        d = self.min_d
        while d <= self.max_d:

            w = self.min_w
            while w <= self.max_w:

                run_pair = True
                for element in self.values:
                    if element[0] == d and element[1] == w:
                        run_pair = False

                if run_pair:

                    print("running benchmark for d=" + str(d) + " , w=" + str(w), end="")

                    count_min_sketch = CountMinSketch(d, w)
                    count_min_sketch.from_word_stream(word_stream, conservative)

                    rms = count_min_sketch.root_mean_squared_error(word_count)
                    are = count_min_sketch.average_relative_error(word_count)

                    element = [d, w, rms, are]
                    self.values.append(element)
                    self.append_element_to_file(element)

                    print(" , rms=" + str(rms) + " , are=" + str(are))

                    #print(count_min_sketch.estimate_count('test', True))
                    #count_min_sketch.print_matrix()

                w *= 2
            d += 1


    def plot_rms(self):

        handles = []

        d = self.min_d
        while d <= self.max_d:

            x_values = []
            y_values = []

            w = self.min_w
            while w <= self.max_w:

                found_element = False
                rms = 0.0
                for element in self.values:
                    if element[0] == d and element[1] == w:
                        found_element = True
                        rms = element[2]

                if found_element:
                    x_values.append(math.log(w, 2))
                    y_values.append(math.log(rms, 10))

                w *= 2

            if len(x_values) > 0 and len(y_values) > 0:
                label = "d=" + str(d)
                handle, = plt.plot(x_values, y_values, label=label)
                handles.append(handle)

            d += 1

        fig_size = [10, 9]
        plt.rcParams["figure.figsize"] = fig_size
        plt.xlabel('log base 2 of w', fontsize=18)
        plt.ylabel('log base 10 of rms', fontsize=18)
        plt.legend(handles)
        plt.show()


    def plot_are(self):

        handles = []

        d = self.min_d
        while d <= self.max_d:

            x_values = []
            y_values = []

            w = self.min_w
            while w <= self.max_w:

                found_element = False
                are = 0.0
                for element in self.values:
                    if element[0] == d and element[1] == w:
                        found_element = True
                        are = element[3]

                if found_element:
                    x_values.append(math.log(w, 2))
                    y_values.append(math.log(are, 10))

                w *= 2

            if len(x_values) > 0 and len(y_values) > 0:
                label = "d=" + str(d)
                handle, = plt.plot(x_values, y_values, label=label)
                handles.append(handle)

            d += 1

        fig_size = [10, 9]
        plt.rcParams["figure.figsize"] = fig_size
        plt.xlabel('log base 2 of w', fontsize=18)
        plt.ylabel('log base 10 of are', fontsize=18)
        plt.legend(handles)
        plt.show()
