class TrieNode:
    def __init__(self, text = ''):
        self.text = text
        self.children = dict()
        self.is_word = False
        self.file_pos = None

class PrefixTree:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, file_pos):
        current = self.root
        for i, char in enumerate(word):
            if char not in current.children:
                prefix = word[0:i+1]
                current.children[char] = TrieNode(prefix)
            current = current.children[char]
        current.is_word = True
        current.file_pos = file_pos

    def find(self, word):
        '''
        Vai percorrendo a palavra até encontrar um nodo que corresponda à
        palavra, e retorna ele, se encontrar, senão, retorna None
        '''
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]

        if current.is_word:
            return current

    def starts_with(self, prefix):
        '''
        Retorna as posições de todas as palavras que começam com o prefixo dado
        '''
        positions = list()
        current = self.root
        for char in prefix:
            if char not in current.children:
                return list()
            current = current.children[char]

        self.__child_pos_for(current, positions)
        return positions

    def __child_pos_for(self, node, positions):
        '''
        Função auxiliar que vai percorrendo todos os filhos recursivamente
        adicionando eles, se forem palavras, adicionando as posições
        '''
        if node.is_word:
            positions.append(node.file_pos)
        for letter in node.children:
            self.__child_pos_for(node.children[letter], positions)

    def starts_with2(self, prefix):
        '''
        Retorna todas as palavras que começam com o prefixo dado
        '''
        words = list()
        current = self.root
        for char in prefix:
            if char not in current.children:
                return list()
            current = current.children[char]

        self.__child_words_for(current, words)
        return words

    def __child_words_for(self, node, words):
        '''
        Função auxiliar que vai percorrendo todos os filhos recursivamente
        adicionando eles, se forem palavras, adicionando as palavras
        '''
        if node.is_word:
            words.append(node.text)
        for letter in node.children:
            self.__child_words_for(node.children[letter], words)
