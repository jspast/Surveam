from db.data import *

def print_category_list(list):
    for category in list:
        print(category[0])
        for item in category[1]:
            print("{:50s}{:>8s}{:>10s}".format(item[0][:50],item[1],item[2]))
        print('')

if __name__ == "__main__":

    # Carrega dados de arquivo csv
    if len(sys.argv) > 2 and sys.argv[1] == '-i':
        try:
            with open(sys.argv[2], newline='') as csvfile:
                db = open_database()
                load_data(db, csvfile)
                close_database(db)

        except FileNotFoundError:
            print("Arquivo csv não encontrado")
            sys.exit()

    elif len(sys.argv) > 3 and sys.argv[1] == '-g':
        if len(sys.argv) == 4:
            prefix = ''
        else:
            prefix = sys.argv[4]
        db = open_database()
        print_category_list(get_categories(db, sys.argv[2], int(sys.argv[3]), prefix))

    # Imprime mensagem de ajuda
    else:
        print("Para carregar dados de arquivo csv, use:\n", sys.argv[0], "-i <nome_do_arquivo>")
        print("Para obter dados de uma plataforma P em um momento M com um prefixo de categoria opcional, use:\n", sys.argv[0], "-g P M prefixo")
        sys.exit()
