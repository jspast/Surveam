class Database:
    def __init__(self):
        self.files = {}

    def create_file(self, name):
        self.files[name] = open(name, 'wb')

    def insert_record(self, filename, record):
        self.files[filename].write(record)

    def close_file(self, filename):
        self.files[filename].close()
