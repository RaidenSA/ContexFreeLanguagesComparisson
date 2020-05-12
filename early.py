import os


PATH_TO_GRAMMAR = 'input.txt'
#PATH_TO_GRAMMAR = 'D://input.txt'

write_operations = 0
read_operations = 0

def loadGrammar(relative_path):
    global_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), relative_path)
    err = 0
    try:
        savefile = open(global_path, 'r')
    except FileNotFoundError:
        try:
            savefile = open(relative_path, 'r')
        except FileNotFoundError:
            err = 1
    grammar = []
    if (not err):
        rules = savefile.read().split('\n')

        for line in rules:
            rule = line.replace(' ', '')#.replace('\n', '')

            starting = rule[0]

            assert(starting.isupper())
            assert(rule[1:3] == '->')

            right = rule[3:].split('|')
        
            for var in right:
                grammar.append(starting + var)

    if (not err):
            savefile.close()
    return grammar, err



def movePoint2right(rule):
    global read_operations

    i = rule.index('.')
    read_operations += len(rule)

    return rule[:i] + rule[i+1] + rule[i] + rule[i+2:]



def canMovePoint(rule):
    #so . is not last symb of rule
    #space separates rule and index

    global read_operations

    read_operations += rule.index('.')
    return rule[rule.index('.') + 1] != ' '


def scan(D, j, word):
    global write_operations
    global read_operations

    if j == 0:
        return D
    for rule in D[j-1]:                                                         #[A→α⋅aβ,i]∈Dj−1
        read_operations += 1

        a = word[j-1]
        read_operations += 1

        if a.islower() and a == rule[rule.index('.') + 1]:                      # a == wj−1
            read_operations += rule.index('.')

            newrule = movePoint2right(rule)
            D[j].add(newrule)                                                   #Dj  ∪= [A→αa⋅β,i]
            write_operations += 1
    return D


def complete(D, j, word):
    global write_operations
    global read_operations

    modified = False
    Djadd = set()
    for rule in D[j]:                                                           #[B→η ⋅,i]∈Dj
        read_operations += 1

        if not canMovePoint(rule):                                              
            i = int(rule[rule.index(' ') + 1:])
            read_operations += rule.index('.')

            B = rule[0]
            read_operations += 1
            # no need to check if B is upper or digit because all rules start in grammar start from upper

            for rule2 in D[i]:                                                  #[A→α⋅Bβ,j]∈Di
                read_operations += 1

                if rule2[rule2.index('.') + 1] == B:
                    read_operations += rule2.index('.')
                    
                    newrule = movePoint2right(rule2)

                    read_operations += 1
                    if newrule not in D[j]:
                        Djadd.add(newrule)                                      #Dj  ∪= [A→αB⋅β,k]
                        write_operations += 1

    for newrule in Djadd:
        D[j].add(newrule)
        write_operations += 1
        modified = True
    return D, modified


def predict(D, j, grammar, word):
    global write_operations
    global read_operations

    modified = False
    Djadd = set()
    for rule in D[j]:                                                           #[A→α⋅Bβ,i]∈Dj
        read_operations += 1

        if canMovePoint(rule):
            B = rule[rule.index('.') + 1]
            read_operations += rule.index('.')
            # no need to check if B is upper because all rules start in grammar start from upper

            for rule2 in grammar:                                               #(B→η)∈P
                read_operations += 1

                if rule2[0] == B:
                    read_operations += 1
                    newrule = B + '.' + rule2[1:] + ' ' + str(j)                  
                    read_operations += 1
                    if newrule not in D[j]:
                        Djadd.add(newrule)                                      #Dj  ∪= [B→⋅ η,j]
                        write_operations += 1

    for newrule in Djadd:
        D[j].add(newrule)
        write_operations += 1
        modified = True
    return D, modified


def earley(grammar, word):
    global write_operations
    global read_operations
    
    n = len(word)
    D = [set() for i in range(n+1)]

    D[0].add('Z.S 0')
    write_operations += 1
    
    for j in range(n+1):
       D = scan(D, j, word)

       Dj_changes = True
       while Dj_changes:
           D, mod1 = complete(D, j, word)
           D, mod2 = predict(D, j, grammar, word)
           Dj_changes = mod1 or mod2

    for j in range(len(D)):
        print('ZS. 0' in D[j], j, D[j])
    return 'ZS. 0' in D[n]


def start(word, path_to_grammar):
    global write_operations
    global read_operations
    write_operations = 0
    read_operations = 0
    grammar, err = loadGrammar(path_to_grammar)
    if (not err):
        rez = earley(grammar, word)
    if (err):
        out = "\nЭтого файла не существует - " + str(path_to_grammar)
    else:
        if rez:
            out = '\nСтрока выводима из грамматики\n'
        else:
            out = '\nСтрока не выводима из грамматики\n'
        out += str(read_operations) + ' операций считывания памяти\n'
        out += str(write_operations) + ' операций записи в память\n'
    return out

   # rez = earley(grammar, word)
   # if rez:
   #     print('String is reachable')
   # else:
   #     print('String is not reachable')
   # print(read_operations, 'memory read operations')
   # print(write_operations, 'memory write operations')


