import csv, sys

from ctypes import *

from database import Database

class Category(Structure):
    _fields_ = [("id", c_uint8),
                ("name", c_char * 100),
                ("platform", c_char)]

class Item(Structure):
    _fields_ = [("id", c_uint16),
                ("name", c_char * 100),
                ("id_category", c_uint8)]

class Moment(Structure):
    _fields_ = [("id", c_uint16),
                ("month", c_uint8),
                ("year", c_uint8)]

class Survey(Structure):
    _fields_ = [("id_moment", c_uint16),
                ("popularity", c_int16),
                ("change", c_int16),
                ("id_item", c_uint16)]

# Converte string de formato "X.XXXX" ou "-X.XXXX" em inteiro
def convert_percentage(string):
    if string[0] == '-':
        return int(string[:2] + string[3:])
    else:
        return int(string[:1] + string[2:])

# Carrega dados do csv e insere no banco de dados
def load_data(file):

    # ToDo: carregar/criar arquivos do banco de dados
    db = Database()
    db.create_datafile("survey")

    # Verifica se há informação de plataforma no csv
    if file.readline().split(',')[1] == "platform":
        platform_data = 1
    else:
        platform_data = 0

    # Processa linhas do csv
    csvreader = csv.reader(file, delimiter=',')
    for row in csvreader:
        # row é uma lista de strings de cada linha do csv

        # Codificação de data
        year = int(row[0][2:-6])
        month = int(row[0][5:-3])
        id_moment = year * 100 + month
        
        # Codifica plataforma como caracter
        if platform_data == 1:
            plataform = row[1][0]

            # Define w para pc(Windows)
            if plataform == 'p':
                plataform = 'w'

        else:
            plataform = "c"

        # ToDo: processar strings de categoria
        category = row[1 + platform_data]

        item = row[2 + platform_data]

        # Codifica porcentagens como inteiros
        change = convert_percentage(row[3 + platform_data])
        popularity = convert_percentage(row[4 + platform_data])

        # Teste básico:
        print(str(id_moment) + ' ' + str(month) + ' ' + str(year) + ' ' + plataform + ' ' + category + ' ' + item + ' ' + str(popularity/100) + '% ' + str(change/100) + '%')

        # Inserir registros no banco de dados
        survey_record = Survey(id_moment=id_moment, popularity=popularity, change=change, id_item=0)
        db.insert_record("survey", survey_record, survey_record.id_moment, Survey.id_moment, [])

    db.close_datafile("survey")

if __name__ == "__main__":

    # Imprime mensagem de ajuda
    if len(sys.argv) == 1 or sys.argv[1][0] == '-':
        print("Use:", sys.argv[0], "arquivo")
        sys.exit()

    try:
        with open(sys.argv[1], newline='') as csvfile:
            load_data(csvfile)

    except FileNotFoundError:
        print("Arquivo csv não encontrado")
        sys.exit()