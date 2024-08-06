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
        
    # ToDo: Busca binária por atributo em arquivo sequencial
    def search_field(self, filename, value, field):
        pass

    # ToDo: Insere registro em arquivo sequencial
    # Ordena record_sort_value pelo atributo sort_field
    # Indexa com base na tupla index: (type, field, filename)
    #   type:   0 = índice numérico
    #           1 = índice patrícia
    #   field:  nome do atributo a ser indexado
    #   filename:   nome do arquivo de índice a ser utilizado
    def insert_record(self, filename, record, record_sort_value, sort_field, index):

        # Vai até o final do arquivo
        self.datafiles[filename].seek(0, 2)

        # Se o arquivo não for vazio, compara registro a ser inserido com o último registro
        if self.datafiles[filename].tell() > 0:
            self.datafiles[filename].seek(sort_field.offset - sizeof(record), 2)

            # Se o registro a ser inserido for maior, insere após o último registro
            if record_sort_value >= int.from_bytes(self.datafiles[filename].read(sort_field.size)[:2], byteorder='little', signed=False):
                self.datafiles[filename].seek(0, 2)
                self.datafiles[filename].write(record)

            # ToDo: Senão, faz busca binária para achar posição a inserir e insere após mover registros sequentes
            else:
                pass

        # Se o arquivo for vazio, insere registro "no final"
        else:
            self.datafiles[filename].write(record)
        
    # Fecha arquivo de dados
    def close_datafile(self, filename):
        self.datafiles[filename].close()

    # Fecha arquivo de índice
    def close_indexfile(self, filename):
        self.indexfiles[filename].close()