import math

def strip_non_alpha_non_space(s):
    ret_string = ""
    for c in s:
        if ord(c) == 32 or (ord(c) >= 65 and ord(c) <= 90) or (ord(c) >= 97 and ord(c) <= 122):
            ret_string += c
    return ret_string

class DocumentReader:

    def __init__(self, filename):

        self.filename = filename
        f = open(filename, 'r')

        lines = f.readlines()

        self.documents = []
        self.lines = []

        for line in lines:

            self.lines.append(line)

            word_line = []
            lowercase_line = strip_non_alpha_non_space(line)
            for word in lowercase_line.split(' '):
                if word != '':
                    word_line.append(word)
            self.documents.append(word_line)


def hash_function_i(i):
    def hash_function(x):
        return hash(str(x) + str(i))
    return hash_function

class HashFunctionFamily:

    def __init__(self, n_hash_functions):

        self.hash_functions = []

        for i in range(0, n_hash_functions):
            self.hash_functions.append(hash_function_i(i))


def get_min_hash_array(document, hash_function_family):

    ret = []

    for hash_function in hash_function_family.hash_functions:

        min_hash = None
        for word in document:
            hash_value = hash_function(word)
            if min_hash is None or hash_value < min_hash:
                min_hash = hash_value

        ret.append(min_hash)

    return ret


def get_min_hash_arrays(documents, hash_function_family):

    ret = []

    for document in documents:
        ret.append(get_min_hash_array(document, hash_function_family))

    return ret


def get_min_hash_arrays_buckets(documents, hash_function_family):

    min_hash_arrays = []

    min_hash_arrays_buckets = []
    for i in range(0, len(hash_function_family.hash_functions)):
        min_hash_arrays_buckets.append({})

    for i in range(0, len(documents)):

        min_hash_array = get_min_hash_array(documents[i], hash_function_family)
        for j in range(0, len(hash_function_family.hash_functions)):
            if min_hash_array[j] not in min_hash_arrays_buckets[j]:
                min_hash_arrays_buckets[j][min_hash_array[j]] = [i]
            else:
                min_hash_arrays_buckets[j][min_hash_array[j]].append(i)

        min_hash_arrays.append(min_hash_array)

    return min_hash_arrays_buckets, min_hash_arrays


def approx_intersection_len(hash_array_a, hash_array_b):

    ret = 0
    for i in range(0, len(hash_array_a)):
        if hash_array_a[i] == hash_array_b[i]:
            ret += 1
    return ret


def approx_union_len(hash_array_a, hash_array_b):

    ret = 0
    for i in range(0, len(hash_array_a)):
        if hash_array_a[i] == hash_array_b[i]:
            ret += 1
        else:
            ret += 2
    return ret


def approximate_jacquard_distance(document_a_index, document_b_index, min_hash_arrays):

    min_hash_array_a = min_hash_arrays[document_a_index]
    min_hash_array_b = min_hash_arrays[document_b_index]

    intersection_len_float = float(approx_intersection_len(min_hash_array_a, min_hash_array_b))
    union_len_float = float(approx_union_len(min_hash_array_a, min_hash_array_b))

    return 1.0 - intersection_len_float / union_len_float



def real_intersection_len(document_a, document_b):

    set_a = set(document_a)
    set_b = set(document_b)

    intersection = set_a.intersection(set_b)
    return len(intersection)


def real_union_len(document_a, document_b):

    set_a = set(document_a)
    set_b = set(document_b)

    union = set_a.union(set_b)
    return len(union)


def real_jacquard_distance(document_a, document_b):

    intersection_len_float = float(real_intersection_len(document_a, document_b))
    union_len_float = float(real_union_len(document_a, document_b))

    return 1.0 - intersection_len_float / union_len_float


class NearestNeighbours:


    def __init__(self, k):

        self.k = k
        self.nearest_neighbours = []


    def try_insert(self, index, distance):

        if len(self.nearest_neighbours) < self.k:
            self.insert(index, distance)
        else:
            _, max_dist = self.nearest_neighbours[self.k-1]
            if distance < max_dist:
                self.insert(index, distance)


    def insert(self, index, distance):

        finished = False
        i = 0
        while not finished and i < self.k:

            if i < len(self.nearest_neighbours):
                _, current_dist = self.nearest_neighbours[i]
                if distance < current_dist:
                    j = len(self.nearest_neighbours) - 2
                    while j >= i:
                        self.nearest_neighbours[j+1] = self.nearest_neighbours[j]
                        j -= 1
                    self.nearest_neighbours[i] = (index, distance)
                    finished = True
            else:
                self.nearest_neighbours.append((index, distance))
            i += 1


def get_approx_nearest_neighbours(document_index, k, min_hash_arrays, max_index=10000):

    nearest_neighbours = NearestNeighbours(k)

    for i in range(0, len(min_hash_arrays)):
        if i < max_index and i != document_index:
                approx_distance = approximate_jacquard_distance(document_index, i, min_hash_arrays)
                nearest_neighbours.try_insert(i, approx_distance)

    return nearest_neighbours


def get_real_nearest_neighbours(document_index, k, documents, max_index=10000):

    nearest_neighbours = NearestNeighbours(k)

    for i in range(0, len(documents)):
        if i < max_index and i != document_index:
                approx_distance = real_jacquard_distance(documents[document_index], documents[i])
                nearest_neighbours.try_insert(i, approx_distance)

    return nearest_neighbours


def get_approx_nearest_neighbours_buckets(document_index, k, min_hash_arrays_buckets, min_hash_arrays, max_index=10000):

    nearest_neighbours = NearestNeighbours(k)

    candidate_indexes = []

    for i in range(0, len(min_hash_arrays_buckets)):
        for key, value in min_hash_arrays_buckets[i].items():
            if document_index in value:
                for j in value:
                    if j != document_index and j not in candidate_indexes:
                        candidate_indexes.append(j)


    return nearest_neighbours


def get_recall_k_document(approx_nearest_neighbours, real_nearest_neighbours):

    approx_nearest = []
    for index, dist in approx_nearest_neighbours.nearest_neighbours:
        approx_nearest.append(index)

    real_nearest = []
    for index, dist in real_nearest_neighbours.nearest_neighbours:
        real_nearest.append(index)

    intersection = set(approx_nearest).intersection(set(real_nearest))

    return float(len(intersection)) / float(len(approx_nearest))


def get_recall_k(min_hash_arrays, documents, k, max_index=300):

    buff = 0.0
    n_processed = 0

    for i in range(0, len(documents)):
        if i <= max_index:
            approx_nearest_neighbours = get_approx_nearest_neighbours(i, k, min_hash_arrays)
            real_nearest_neighbours = get_real_nearest_neighbours(0, k, documents)
            recall_k_document = get_recall_k_document(approx_nearest_neighbours, real_nearest_neighbours)
            buff += recall_k_document
            n_processed += 1

    return float(buff) / float(n_processed)


def get_approx_nearest_neighbours_document_indexes(document_index, documents, min_hash_arrays, k):

    ret = []
    approx_nearest_neighbours = get_approx_nearest_neighbours(document_index, k, min_hash_arrays)
    for index, value in approx_nearest_neighbours.nearest_neighbours:
        ret.append(index)
    return ret


def get_real_nearest_neighbours_document_indexes(document_index, documents, min_hash_arrays, k):

    ret = []
    real_nearest_neighbours = get_real_nearest_neighbours(document_index, k, documents)
    for index, value in real_nearest_neighbours.nearest_neighbours:
        ret.append(index)
    return ret


def list_intersection(list1, list2):

    ret = []
    for i in list1:
        if i in list2:
            ret.append(i)

    return ret


def inverse_index(documents):

    ret = {}

    for i in range(0, len(documents)):
        for word in documents[i]:
            if word not in ret:
                ret[word] = [i]
            elif i not in ret[word]:
                ret[word].append(i)

    return ret


def tf_idx(documents):

    ret = []

    N = len(documents)

    inv_idx = inverse_index(documents)
    for i in range(0, len(documents)):
        vector = []
        unique_words = []
        for word in documents[i]:
            if word not in unique_words:
                unique_words.append(word)
        for word in unique_words:
            n_in_doc = 0
            for w in documents[i]:
                if w == word:
                    n_in_doc += 1
            tf = float(n_in_doc) / float(len(documents[i]))
            dfx = len(inv_idx[word])
            w = tf * math.log(float(N) / float(dfx))
            vector.append((word, w))
        ret.append(vector)

    return ret
