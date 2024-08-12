import csv, sys

from hashlib import blake2b

from ctypes import *

from database import Database

class Category(Structure):
    _fields_ = [("id", c_uint16),
                ("name", c_char * 61),
                ("platform", c_char)]
    _pack_ = 1

class Item(Structure):
    _fields_ = [("id", c_uint32),
                ("name", c_char * 58),
                ("id_category", c_uint16)]
    _pack_ = 1

class Moment(Structure):
    _fields_ = [("id", c_uint16),
                ("month", c_uint8),
                ("year", c_uint8)]
    _pack_ = 1

class Survey(Structure):
    _fields_ = [("id", c_uint64),
                ("popularity", c_int16),
                ("change", c_int16),
                ("id_moment", c_uint16),
                ("id_item", c_uint32)]
    _pack_ = 1

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
    db.create_datafile("category")
    db.create_datafile("item")
    db.create_datafile("moment")

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
            platform = row[1][0]

            # Define w para pc(Windows)
            if platform == 'p':
                platform = 'w'

        else:
            platform = "c"

        platform = platform.encode()

        # Processar strings de categoria (Remove texto entre parênteses)
        category_tmp = row[1 + platform_data].split('(')
        category = category_tmp[0].strip().encode()

        item = row[2 + platform_data].encode()

        # Codifica porcentagens como inteiros
        change = convert_percentage(row[3 + platform_data])
        popularity = convert_percentage(row[4 + platform_data])

        # Calcula id da categoria
        id_category = blake2b(digest_size=2)
        id_category.update(category)
        id_category.update(platform)
        id_category = id_category.digest()

        # Calcula id do item
        id_item = blake2b(digest_size=4)
        id_item.update(item)
        id_item.update(id_category)

        id_category = int.from_bytes(id_category)
        id_item = int.from_bytes(id_item.digest())

        # Calcula id do levantamento
        id_survey = id_moment * 10000000000 + id_item

        # Teste básico:
        print(str(id_moment) + ' ' + str(month) + ' ' + str(year) + ' ' + str(platform) + ' ' + category.decode() + ' ' + item.decode() + ' ' + str(popularity/100) + '% ' + str(change/100) + '%')

        # Inserir registros no banco de dados
        if db.id_exists("survey", id_survey, Survey.id, sizeof(Survey)) == False:
            survey_record = Survey(id=id_survey, id_moment=id_moment, popularity=popularity, change=change, id_item=id_item)
            db.insert_record("survey", survey_record, survey_record.id, Survey.id, [])

        if db.id_exists("category", id_category, Category.id, sizeof(Category)) == False:
            category_record = Category(id=id_category, name=category, platform=platform)
            db.insert_record("category", category_record, category_record.id, Category.id, [])

        if db.id_exists("item", id_item, Item.id, sizeof(Item)) == False:
            item_record = Item(id=id_item, name=item, id_category=id_category)
            db.insert_record("item", item_record, item_record.id, Item.id, [])

        if db.id_exists("moment", id_moment, Moment.id, sizeof(Moment)) == False:
            moment_record = Moment(id=id_moment, month=month, year=year)
            db.insert_record("moment", moment_record, moment_record.id, Moment.id, [])

    db.close_datafile("survey")
    db.close_datafile("category")
    db.close_datafile("item")
    db.close_datafile("moment")


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

