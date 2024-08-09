from ctypes import *

datafile_ext = ".dat"
indexfile_ext = ".idx"

class Database:
    def __init__(self):
        self.datafiles = {}
        self.indexfiles = {}

    # ToDo: Carrega/Cria arquivo de dados
    def create_datafile(self, name):
        self.datafiles[name] = open(name + datafile_ext, 'wb+')

    # ToDo: Carrega/Cria arquivo de índice
    def create_indexfile(self, name):
        self.indexfiles[name] = open(name + indexfile_ext, 'wb+')
        
    # Busca binária por id único em arquivo sequencial, retorna posição do id no arquivo ou posição onde seria inserido
    def search_id(self, filename, id, id_field, record_size):
        self.datafiles[filename].seek(0, 2)
        end = self.datafiles[filename].tell() // record_size
        start = 0

        while start <= end:
            middle = start + (end - start) // 2

            self.datafiles[filename].seek(id_field.offset + middle * record_size, 0)
            middle_value = int.from_bytes(self.datafiles[filename].read(id_field.size)[:id_field.size], byteorder='little', signed=False)

            if middle_value < id:
                start = middle + 1
            else:
                end = middle - 1

        return start

    # Devolve true se existe registro com o id no arquivo sequencial e false caso contrário
    def id_exists(self, filename, id, id_field, record_size):
        record_num = self.search_id(filename, id, id_field, record_size)

        record = self.get_record(filename, record_num, record_size)

        if record == -1:
            return False

        if int.from_bytes(record[id_field.offset:id_field.offset + id_field.size], byteorder='little', signed=False) == id:
            return True
        else:
            return False

    # Dada uma posição num no arquivo, devolve o registro nesta posição ou -1 se posição inválida
    def get_record(self, filename, num, record_size):
        pos = num * record_size
        self.datafiles[filename].seek(0, 2)
        if pos > self.datafiles[filename].tell():
            return -1
        else:
            self.datafiles[filename].seek(pos, 0)
            return self.datafiles[filename].read(record_size)

    # Retorna o último ID do arquivo ou -1 se for vazio
    def last_id(self, filename, id_field, record_size):
        # Vai até o final do arquivo
        self.datafiles[filename].seek(0, 2)

        # Se o arquivo não for vazio, retorna o último ID
        if self.datafiles[filename].tell() >= record_size:
            self.datafiles[filename].seek(id_field.offset - record_size, 2)

            return int.from_bytes(self.datafiles[filename].read(id_field.size)[:id_field.size], byteorder='little', signed=False)
        
        # Senão, retorna -1
        else:
            return -1

    # Insere registro em arquivo sequencial
    # Ordena record_sort_value pelo atributo sort_field
    # ToDo: Indexa com base na tupla index: (type, field, filename)
    #   type:   0 = índice numérico
    #           1 = índice patrícia
    #   field:  nome do atributo a ser indexado
    #   filename:   nome do arquivo de índice a ser utilizado
    def insert_record(self, filename, record, record_sort_value, sort_field, index):

        # Se o registro a ser inserido for maior que o último, insere no final do arquivo
        if record_sort_value >= self.last_id(filename, sort_field, sizeof(record)):
            self.datafiles[filename].seek(0, 2)
            self.datafiles[filename].write(record)

        # Senão, faz busca binária para achar posição a inserir e insere após mover registros sequentes
        else:
            num = self.search_id(filename, record_sort_value, sort_field, sizeof(record))
            pos = num * sizeof(record)

            self.datafiles[filename].seek(0, 2)
            end = self.datafiles[filename].tell()

            self.datafiles[filename].seek(pos, 0)
            data = self.datafiles[filename].read(end - pos)
            self.datafiles[filename].seek(pos + sizeof(record), 0)
            self.datafiles[filename].write(data)
            self.datafiles[filename].seek(pos, 0)
            self.datafiles[filename].write(record)
        
    # Fecha arquivo de dados
    def close_datafile(self, filename):
        self.datafiles[filename].close()

    # Fecha arquivo de índice
    def close_indexfile(self, filename):
        self.indexfiles[filename].close()