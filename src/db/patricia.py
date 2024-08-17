import os

class Nodo:
    def __init__(self, index, filhos):
        self.index = index
        self.filhos = filhos

# Pega uma string qualquer e convete ela em uma sequencia binaria
def string_to_binary(s):
    return ''.join(format(ord(char), '08b') for char in s)

# Pega uma sequencia binaria e converte para uma string
def binary_to_string(binary_str):
    # Split the binary string into chunks of 8 bits
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    # Convert each 8-bit chunk to its corresponding ASCII character
    string = ''.join([chr(int(char, 2)) for char in chars])
    return string

# Pega a raiz da PATRICIA  e um indice (chave) e devolve as folhas do nodo com esse indice (array)
def get_leaves_by_index(nodo, target_index):
    if nodo.index == target_index:
        return collect_leaves(nodo)
    
    for filho in nodo.filhos:
        if isinstance(filho, Nodo):
            result = get_leaves_by_index(filho, target_index)
            if result is not None:
                return result
    return None

# Auxiliar da get_leaves_by_index
def collect_leaves(nodo):
    leaves = []
    if isinstance(nodo, Nodo):
        for filho in nodo.filhos:
            if isinstance(filho, Nodo):
                leaves.extend(collect_leaves(filho))
            else:
                leaves.append(filho)
    return leaves

# Insere um valor na folha do nodo que tem o indice passado como argumento
def insert_value_in_leaf(nodo, target_index, value):
    if nodo.index == target_index:
        for i in range(len(nodo.filhos)):
            if nodo.filhos[i] == 0:
                nodo.filhos[i] = value
                return True
        if len(nodo.filhos) < 2:
            nodo.filhos.append(value)
        return True
    
    for filho in nodo.filhos:
        if isinstance(filho, Nodo):
            if insert_value_in_leaf(filho, target_index, value):
                return True
    return False


def printa_nodos(nodo):
    if(isinstance(nodo.filhos[0], int)):
        print(nodo.filhos[0])
    else:
        printa_nodos(nodo.filhos[0])
    print(nodo.index)
    if(isinstance(nodo.filhos[1], int)):
        print(nodo.filhos[1])
    else:
        printa_nodos(nodo.filhos[1])

def printa_arvore_grafica(nodo, indent="", last=True):
    if isinstance(nodo, Nodo):
        print(indent + ("└── " if last else "├── ") + f"Index: {nodo.index}")
        indent += "    " if last else "│   "
        for i, filho in enumerate(nodo.filhos):
            if isinstance(filho, Nodo):
                printa_arvore_grafica(filho, indent, last=(i == len(nodo.filhos) - 1))
            else:
                print(indent + ("└── " if i == len(nodo.filhos) - 1 else "├── ") + f"Leaf: {filho}")
    else:
        print(indent + "Leaf: " + str(nodo))

def simplifica_arvore(nodo):
    if isinstance(nodo, int):
        return 0

    # Simplify the left child
    if isinstance(nodo.filhos[0], Nodo) and isinstance(nodo.filhos[1], int):
        nodo.index = nodo.filhos[0].index
        nodo.filhos[1] = nodo.filhos[0].filhos[1]
        nodo.filhos[0] = nodo.filhos[0].filhos[0]
        simplifica_arvore(nodo)
        return

    # Simplify the right child
    elif isinstance(nodo.filhos[1], Nodo) and isinstance(nodo.filhos[0], int):
        nodo.index = nodo.filhos[1].index
        nodo.filhos[0] = nodo.filhos[1].filhos[0]
        nodo.filhos[1] = nodo.filhos[1].filhos[1]
        simplifica_arvore(nodo)
        return

    # Recursively simplify both children
    simplifica_arvore(nodo.filhos[0])
    simplifica_arvore(nodo.filhos[1])

def insere_nodo(nodo, num):
    num_str = str(num)  # Ensure the key is an 8-character string
    controle = True
    buffer_nodo = nodo
    salva_nodo = nodo
    i = 1

    while controle:
        digito = int(num_str[i])
        if i != nodo.index:
            controle = False
        else:
            if isinstance(nodo.filhos[digito], int):
                nodo.filhos[digito] = Nodo(num, [0, 0])
                break
            elif (len(str(nodo.filhos[digito].index)) >= 9):
                controle = False
        if (controle and isinstance(nodo.filhos[digito], Nodo)):
            nodo = nodo.filhos[digito]
            i += 1
        else:
            controle = False
    if (not controle):
        while (len(str(nodo.filhos[int(num_str[nodo.index])].index)) < 9):
            nodo = nodo.filhos[int(num_str[nodo.index])]
        buffer_nodo = nodo.filhos[int(num_str[nodo.index])]

        j = 1
        while j < 9 and str(buffer_nodo.index)[j] == num_str[j]:
            j += 1

        nodo = salva_nodo 
        while(nodo.filhos[int(num_str[nodo.index])].index < j):
            nodo = nodo.filhos[int(num_str[nodo.index])]

        if j < 9:
            if num_str[j] == '1':
                nodo.filhos[int(num_str[nodo.index])] = Nodo(j, [Nodo(nodo.filhos[int(num_str[nodo.index])].index, [nodo.filhos[int(num_str[nodo.index])].filhos[0], nodo.filhos[int(num_str[nodo.index])].filhos[1]]), Nodo(num, [0, 0])])
            else:
                nodo.filhos[int(num_str[nodo.index])] = Nodo(j, [Nodo(num, [0, 0]), Nodo(nodo.filhos[int(num_str[nodo.index])].index, [nodo.filhos[int(num_str[nodo.index])].filhos[0], nodo.filhos[int(num_str[nodo.index])].filhos[1]])])

raiz = Nodo(1,[0,0])