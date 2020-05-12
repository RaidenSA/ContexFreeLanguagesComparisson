import os


#PATH_TO_GRAMMAR = 'input.txt'
err = 0

def loadGrammar(relative_path):
    flag = 0
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
    letter2number['S'] = 0
    if (not err):
        while True:
            try:
                line = savefile.readline().replace(' ', '').replace('\n', '')

                starting = line[0]
                if starting.isupper() and not starting in letter2number:
                    letter2number[starting] = len(letter2number)
                assert(starting.isupper())
                assert(line[1:3] == '->')

                right = line[3:].split('|')
            
                for var in right:
                    if var.islower():
                        term.append((starting, var))
                    else:
                        non_term.append((starting, var))

            except IndexError:
                break
    if (not err):
           # flag = 0
            savefile.close()
    return term, non_term, letter2number


def cyk(term, non_term, letter2number, string):
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
                P[0][i][letter2number[A]] = True
            # read string[i]
            read_operations += 1
    
    for i in range(1, n):
        for j in range(n - i):
            for k in range(i):
                for (A, BC) in non_term:
                    # read from non_term
                    read_operations += 1

                    if P[k][j][letter2number[BC[0]]] and P[i-k-1][j+k+1][letter2number[BC[1]]]:
                        P[i][j][letter2number[A]] = True
                        write_operations += 1

                    if P[k][j][letter2number[BC[0]]]: # both conditions of if, 2 read ops
                        read_operations += 2
                    else:                             # fast bool operations! so only one
                        read_operations += 1
    
    return P[n-1][0][0], write_operations, read_operations

def start(word, path_to_grammar):
    term, non_term, letter2number = loadGrammar(path_to_grammar)
    string = word
    rez, write_op, read_op = cyk(term, non_term, letter2number, string)
    if (write_op == 0):
        out = "\nЭтого файла не существует - " + str(path_to_grammar)
    else:
        if rez:
            out = '\nСтрока выводима из грамматики\n'
        else:
            out = '\nСтрока не выводима из грамматики\n'
        out += str(read_op) + ' операций считывания памяти\n'
        out += str(write_op) + ' операций записи в память\n'
    return out

