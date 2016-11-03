import random
import matplotlib.pyplot as plt
from string import punctuation

def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

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



class R_reservoir_sampling:

    def __init__(self, k):

        self.i = 0
        self.k = k
        self.reservoir = [-1]*k


    def sample(self, word):

        if self.i < self.k:
            self.reservoir[self.i] = (word, self.i)
        else:
            j = random.randint(1, self.i)
            if j < self.k:
                self.reservoir[j] = (word, self.i)
        self.i += 1


    def print_reservoir(self):

        for word, position in self.reservoir:
            print(str(position) + "\t\t\'" + word + "\'")


    def get_positions(self):

        positions = []
        for word, position in self.reservoir:
            positions.append(position)
        return positions


    def plot_sorted_positions(self):

        positions = self.get_positions()
        sorted_positions = sorted(positions)
        plt.plot(sorted_positions)
        plt.show()


    def fill_reservoir_from_word_stream(self, word_stream):

        for word in word_stream.get_words():
            self.sample(word)


    def plot_word_count_histogram(self, word_stream):

        unique_reservoir_words = []
        for word, position in self.reservoir:
            if word not in unique_reservoir_words:
                unique_reservoir_words.append(word)

        words = word_stream.get_words()
        counts_words = []
        for word in unique_reservoir_words:
            counts_words.append((words.count(word), word))

        sorted_counts_words = sorted(counts_words)
        reversed_counts_words = sorted_counts_words[::-1]

        counts = []
        for count, word in reversed_counts_words:
            counts.append(count)
        plt.plot(counts)
        plt.show()


    def plot_against_word_count(self, word_stream, word_count):

        unique_reservoir_words = []
        for word, position in self.reservoir:
            if word not in unique_reservoir_words:
                unique_reservoir_words.append(word)

        words = word_stream.get_words()
        counts_words = []
        for word in unique_reservoir_words:
            counts_words.append((words.count(word), word))

        sorted_counts_words = sorted(counts_words)
        reversed_counts_words = sorted_counts_words[::-1]

        counts = []
        for count, word in reversed_counts_words:
            counts.append(count)
        plt.plot(counts)

        clipped_values = word_count.get_clipped_values()
        plt.plot(clipped_values)

        plt.show()


class Hash_bucket:

    def __init__(self):

        self.min_hash_set = False
        self.min_hash = None
        self.count = 0
        self.word = None


    def try_insert(self, word, word_hash):

        if not self.min_hash_set:
            self.min_hash = word_hash
            self.min_hash_set = True
            self.word = word
            self.count = 1

        else:
            if self.word == word:
                self.count += 1
            else:
                if word_hash < self.min_hash:
                    self.min_hash = word_hash
                    self.word = word
                    self.count = 1


    def get_values(self):

        return (self.count, self.min_hash, self.word)


class Hash_bucket_counter:

    def __init__(self, n_buckets):

        self.buckets = []
        self.n_buckets = n_buckets
        for i in range(0, self.n_buckets):
            self.buckets.append(Hash_bucket())


    def try_insert(self, word):

        word_hash = hash(word)
        bucket_index = word_hash % self.n_buckets
        self.buckets[bucket_index].try_insert(word, word_hash)


    def try_insert_from_word_stream(self, word_stream):

        for word in word_stream.get_words():
            self.try_insert(word)


    def print_counter(self):

        values = []
        for bucket in self.buckets:
            values.append(bucket.get_values())

        sorted_values = sorted(values)
        reversed_values = sorted_values[::-1]

        clipped_values = []
        for i in range(100):
            clipped_values.append(reversed_values[i])

        print(clipped_values)


    def plot_word_count_histogram(self):

        values = []
        for bucket in self.buckets:
            count, min_hash, word = bucket.get_values()
            values.append(count)

        sorted_values = sorted(values)
        reversed_values = sorted_values[::-1]
        clipped_values = []
        for i in range(100):
            clipped_values.append(reversed_values[i])

        plt.plot(clipped_values)
        plt.show()
