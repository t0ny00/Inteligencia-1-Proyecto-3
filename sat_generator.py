import sys





class SatCreator():

    def __init__(self,rows,columns,matrix):
        self.rows = rows
        self.columns = columns
        self.matrix = matrix


    def generator():
        pass

    def getMatrix(self):
        return self.matrix

    def toStr(self):
        return str(self.rows) + " " + str(self.columns) + " " + str(self.getMatrix())

def strMatrixToLists(matrix):
    lista = []
    for elem in matrix:
        if elem == '': continue
        act_list = []
        for actual in elem:
            if actual == '\n':
                continue
            elif actual == '.':
                act_list.append(-1)
            else:
                act_list.append(int(actual))
        lista.append(act_list)
    return lista



if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: python sat_generator.py [input file]")
        exit(0)
    file = open(args[1],'r')
    for line in file:
        parsed = line.split(' ')
        rows     = int(parsed[0])
        columns = int(parsed[1])
        matrix  = strMatrixToLists(parsed[2:])
        sat_creator = SatCreator(rows,columns,matrix)
        print(sat_creator.toStr())


