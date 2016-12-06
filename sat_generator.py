import sys

class SatCreator():

    def __init__(self,rows,columns,matrix):
        self.rows = rows
        self.columns = columns
        self.matrix = matrix
        self.n_vars = (self.rows+1)*self.columns + (self.columns+1)*self.rows
        self.header = "p cnf %d " % (self.n_vars)
        self.sat = ""
        self.sat_counter = 0


    def claus_generator(self):
        for i,row in enumerate(self.matrix):
            for j,column in enumerate(row):
                if   column == 0:
                    self.addZeroClause(i,j)
                elif column == 1:
                    self.addOneClause(i,j)
                elif column == 2:
                    self.addTwoClause(i,j)
                elif column == 3:
                    self.addThreeClause(i,j)
                elif column == 4:
                    self.addFourClause(i,j)
                elif column == -1:
                    self.addEmptyClause(i,j)

    def getMatrix(self):
        return self.matrix

    def addZeroClause(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        self.sat += "-%d 0\n" % (up)
        self.sat += "-%d 0\n" % (down)
        self.sat += "-%d 0\n" % (left)
        self.sat += "-%d 0\n" % (right)
        self.sat_counter += 4

    def addOneClause(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        self.sat += "-%d -%d 0\n" % (up,down)
        self.sat += "-%d -%d 0\n" % (up,left)
        self.sat += "-%d -%d 0\n" % (up,right)
        self.sat += "%d %d %d %d 0\n" % (up,down,left,right)
        self.sat += "-%d -%d 0\n" % (down,left)
        self.sat += "-%d -%d 0\n" % (down,right)
        self.sat += "-%d -%d 0\n" % (left,right)
        self.sat_counter += 7

    def addTwoClause(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        self.sat += "-%d -%d -%d 0\n" % (up,down,left)
        self.sat += "-%d -%d -%d 0\n" % (up,down,right)
        self.sat += "-%d -%d -%d 0\n" % (up,left,right)
        self.sat += "%d %d %d 0\n" % (up,down,left)
        self.sat += "%d %d %d 0\n" % (up,down,right)
        self.sat += "%d %d %d 0\n" % (up,left,right)
        self.sat += "-%d -%d -%d 0\n" % (down,left,right)
        self.sat += "%d %d %d 0\n" % (down,left,right)
        self.sat_counter += 8

    def addThreeClause(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        self.sat += "-%d -%d -%d -%d 0\n" % (up,down,left,right)
        self.sat += "%d %d 0\n" % (up,down)
        self.sat += "%d %d 0\n" % (up,left)
        self.sat += "%d %d 0\n" % (up,right)
        self.sat += "%d %d 0\n" % (down,left)
        self.sat += "%d %d 0\n" % (down,right)
        self.sat += "%d %d 0\n" % (left,right)
        self.sat_counter += 7

    def addFourClause(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        self.sat += "%d 0\n" % (up)
        self.sat += "%d 0\n" % (down)
        self.sat += "%d 0\n" % (left)
        self.sat += "%d 0\n" % (right)
        self.sat_counter += 4

    def addEmptyClause(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        self.sat += "%d -%d 0\n" % (up,up)
        self.sat += "%d -%d 0\n" % (down,down)
        self.sat += "%d -%d 0\n" % (left,left)
        self.sat += "%d -%d 0\n" % (right,right)
        self.sat_counter += 4

    def addNeigthborClause(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        self.sat += "-%d %d %d %d 0\n" % (up,left,up-1,left-self.columns)
        self.sat += "-%d %d %d %d 0\n" % (up,right,right-self.columns,up+1)


    def getCoordValues(self,i,j):
        up      = i*self.columns + j + 1
        down    = (i + 1)*self.columns + j +  1
        left    = (self.rows + 1)*i + j + 1 + (self.columns)*(self.rows+1)
        right   = left + 1
        return (up,down,left,right)

    def getSat(self):
        return self.header + str(self.sat_counter) + '\n' + self.sat

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
        sat_creator.claus_generator()
        print(sat_creator.getSat())


