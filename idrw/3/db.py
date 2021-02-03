class Db:
    def __init__(self, dictionary):
        self.__dict__ = dictionary

def record(name, dictionary):
    globals()[name]=Db(dictionary)
