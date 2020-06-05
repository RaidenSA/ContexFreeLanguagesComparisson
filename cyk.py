import os

# PATH_TO_GRAMMAR = 'input.txt'
err = 0
tree = ''

class Tree:
    used = set()
    globalIndex = 0

    def __init__(self, value, i, j, mom=None, dad=None):
        self.i = i
        self.j = j
        self.mom = mom
        self.dad = dad
        self.value = value

        self.globalIndex = str(Tree.globalIndex)
        Tree.globalIndex += 1

    def __int__(self):
        return 1

    def __str__(self):
        return self.value + ' ' + str(self.i + 1) + ' ' + str(self.j + 1)

    def print(self):
        if self.mom:

            Tree.used.add(self.mom[0].globalIndex)
            Tree.used.add(self.dad[0].globalIndex)

            return str(self) + ' -> ' + str(self.mom[0]) + ' and ' + str(self.dad[0])
        else:
            return str(self) + ' -> base'


def loadGrammar(relative_path):
    err = 0
    global_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_path)
    try:
        savefile = open(global_path, 'r')
    except FileNotFoundError:
        try:
            savefile = open(relative_path, 'r')
        except FileNotFoundError:
            err = 1

    term = []
    non_term = []

    letter2number = dict()
    number2letter = dict()
    letter2number['S'] = 0
    number2letter['0'] = 'S'

    if (not err):
        while True:
            try:
                line = savefile.readline().replace(' ', '').replace('\n', '')

                starting = line[0]
                if starting.isupper() and not starting in letter2number:
                    cur_len = len(letter2number)
                    letter2number[starting] = len(letter2number)
                    number2letter[str(cur_len)] = starting

                assert (starting.isupper())
                assert (line[1:3] == '->')

                right = line[3:].split('|')

                for var in right:
                    if var.islower():
                        term.append((starting, var))
                    else:
                        non_term.append((starting, var))

            except IndexError:
                break
    if (not err):
        savefile.close()
    return term, non_term, letter2number, number2letter


def cyk(term, non_term, letter2number, string, number2letter):
    global tree
    n = len(string)
    P = [[[False] * len(letter2number) for i in range(n)] for j in range(n)]

    write_operations = 0
    read_operations = 0

    for i in range(n):
        for (A, b) in term:
            # read from term
            read_operations += 1

            if b == string[i]:
                write_operations += 1
                P[0][i][letter2number[A]] = [Tree(A, 0, i)]
            # read string[i]
            read_operations += 1

    for i in range(1, n):
        for j in range(n - i):
            for k in range(i):
                for (A, BC) in non_term:
                    # read from non_term
                    read_operations += 1

                    if P[k][j][letter2number[BC[0]]] and P[i - k - 1][j + k + 1][letter2number[BC[1]]]:
                        if P[i][j][letter2number[A]]:
                            P[i][j][letter2number[A]] += [Tree(A, i, j, P[k][j][letter2number[BC[0]]],
                                                               P[i - k - 1][j + k + 1][letter2number[BC[1]]])]
                        else:
                            P[i][j][letter2number[A]] = [Tree(A, i, j, P[k][j][letter2number[BC[0]]],
                                                              P[i - k - 1][j + k + 1][letter2number[BC[1]]])]
                        write_operations += 1

                    if P[k][j][letter2number[BC[0]]]:  # both conditions of if, 2 read ops
                        read_operations += 2
                    else:  # fast bool operations! so only one
                        read_operations += 1

    # printing table
    Tree.used.add(str(Tree.globalIndex - 1))
    rules = []

    max_in_a_line = 0
    for Pi in P:
        for Pij in Pi:
            max_in_a_line = max(max_in_a_line, sum(list(map(int, map(bool, Pij)))))

    for Pi in P[::-1]:
        for Pij in Pi:

            # making rules and elements
            A = ['']
            for k in range(len(Pij)):
                if Pij[k] and (Pij[k][0].globalIndex in Tree.used):
                    for rule in Pij[k]:
                        rules.append(rule.print())
                    A[0] = A[0] + number2letter[str(k)] + ' '

            # adding lining spaces
            if A[0] != '':
                A[0] = A[0][:-1]
                while len(A[0]) < (2 * max_in_a_line - 1):
                    A[0] += '  '
                # print(A, end = ' ')
                tree += str(A)
            else:
                # print(' ' * (2 * max_in_a_line + 3), end = ' ')
                tree += str(' ' * (2 * max_in_a_line + 3)) + ' '
        # print()
        tree += '\n'
    for letter in string:
        # print(letter + ' ' * (2 * max_in_a_line + 2), end = ' ')
        tree += str(letter + ' ' * (2 * max_in_a_line + 2)) + ' '
    # print('\n')
    tree += '\n' + '\n'

    for rule in rules[::-1]:
        tree += str(rule) + '\n'
        # print(rule)
    return P[n - 1][0][0], write_operations, read_operations


def start(word, path_to_grammar):
    global tree
    term, non_term, letter2number, number2letter = loadGrammar(path_to_grammar)
    string = word
    tree = ''
    rez, write_op, read_op = cyk(term, non_term, letter2number, string, number2letter)
    if (write_op == 0):
        out = "\nЭтого файла не существует - " + str(path_to_grammar)
    else:
        if rez:
            out = '\nСтрока выводима из грамматики\n'
        else:
            out = '\nСтрока не выводима из грамматики\n'
        out += str(read_op) + ' операций считывания памяти\n'
        out += str(write_op) + ' операций записи в память\n' + '\n'
        out += tree
    return out

