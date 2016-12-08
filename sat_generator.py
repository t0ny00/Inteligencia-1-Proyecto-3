import sys

class SatCreator():

    def __init__(self,rows,columns,matrix):
        self.rows = rows
        self.columns = columns
        self.matrix = matrix
        self.n_vars = (self.rows+1)*self.columns + (self.columns+1)*self.rows + self.rows*self.columns + (self.rows*self.columns)**2
        self.header = "p cnf %d " % (self.n_vars)
        self.sat = ""
        self.sat_counter = 0
        self.walls = (self.rows+1)*self.columns + (self.columns+1)*self.rows
        self.reach = self.walls + self.rows*self.columns

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
                    #self.addEmptyClause(i,j)
                    pass
        self.addPerimeterClause()
        self.addReachableClause()
        self.addInnerReacheable()
        # self.test()

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

    def addPerimeterClause(self):
        #self.sat += 'perim\n'

        for j in range(self.columns):
            up, down, left, right = self.getCoordValues(0,j)
            z = self.walls + (j+1)
            self.sat += "%d %d 0\n" % (up,z)
            self.sat += "-%d -%d 0\n" % (z,up)
            self.sat_counter += 2
        for j in range(self.columns):
            up, down, left, right = self.getCoordValues(self.rows-1,j)
            z = self.walls + (self.rows-1)*self.columns + (j+1)
            self.sat += "%d %d 0\n" % (down,z)
            self.sat += "-%d -%d 0\n" % (z,down)
            self.sat_counter += 2
        for i in range(self.rows):
            up, down, left, right = self.getCoordValues(i,0)
            z = self.walls + i*self.columns + 1
            self.sat += "%d %d 0\n" % (left,z)
            self.sat += "-%d -%d 0\n" % (z,left)
            self.sat_counter += 2
        for i in range(self.rows):
            up, down, left, right = self.getCoordValues(i,self.columns-1)
            z = self.walls + i*self.columns + self.columns
            self.sat += "%d %d 0\n" % (right,z)
            self.sat += "-%d -%d 0\n" % (z,right)
            self.sat_counter += 2
        for i in range(1,self.rows-1):
            for j in range(1,self.columns-1):
                up, down, left, right = self.getCoordValues(i,j)
                z0 = self.walls + i*self.columns + j + 1
                z1 = z0 + 1
                z3 = z0 - 1
                z4 = z0 - self.columns
                z2 = z0 + self.columns
                self.sat += "-%d -%d -%d -%d -%d 0\n" % (z0,up,down,left,right)
                self.sat += "-%d -%d -%d -%d %d 0\n" % (up,right,down,z0,z3)
                self.sat += "-%d -%d -%d -%d %d 0\n" % (up,right,left,z0,z2)
                self.sat += "-%d -%d -%d %d %d 0\n" % (up,right,z0,z2,z3)
                self.sat += "-%d -%d -%d -%d %d 0\n" % (up,down,left,z0,z1)
                self.sat += "-%d -%d -%d %d %d 0\n" % (up,down,z0,z1,z3)
                self.sat += "-%d -%d -%d %d %d 0\n" % (up,left,z0,z1,z2)
                self.sat += "-%d -%d %d %d %d 0\n" % (up,z0,z1,z2,z3)
                self.sat += "%d %d -%d 0\n" % (up,z0,z4)
                self.sat += "-%d -%d -%d -%d %d 0\n" % (right,down,left,z0,z4)
                self.sat += "-%d -%d -%d %d %d 0\n" % (right,down,z0,z3,z4)
                self.sat += "-%d -%d -%d %d %d 0\n" % (right,left,z0,z2,z4)
                self.sat += "-%d -%d %d %d %d 0\n" % (right,z0,z2,z3,z4)
                self.sat += "%d %d -%d 0\n" % (right,z0,z1)
                self.sat += "-%d -%d -%d %d %d 0\n" % (down,left,z0,z1,z4)
                self.sat += "-%d -%d %d %d %d 0\n" % (down,z0,z1,z3,z4)
                self.sat += "%d %d -%d 0\n" % (down,z0,z2)
                self.sat += "-%d -%d %d %d %d 0\n" % (left,z0,z1,z2,z4)
                self.sat += "%d %d -%d 0\n" % (left,z0,z3)
                self.sat += "-%d %d %d %d %d 0\n" % (z0,z1,z2,z3,z4)
                self.sat_counter += 20

        # z = self.walls
        # for i in range(self.rows):
        #     for j in range(self.columns):
        #         up, down, left, right = self.getCoordValues(i,j)
        #         z += 1
        #         z1 = z + 1
        #         z3 = z - 1
        #         z4 = z - self.columns
        #         z2 = z + self.columns
        #         if (i != 0) : 
        #             self.sat += "-%d %d %d 0\n" % (z4,up,z)
        #             self.sat_counter += 1
        #         if (i != self.rows-1) : 
        #             self.sat += "-%d %d %d 0\n" % (z2,down,z)
        #             self.sat_counter += 1
        #         if (j != 0) : 
        #             self.sat += "-%d %d %d 0\n" % (z3,left,z)
        #             self.sat_counter += 1
        #         if (j != self.columns-1) : 
        #             self.sat += "-%d %d %d 0\n" % (z1,right,z)
        #             self.sat_counter += 1


    def addReachableClause(self):
        # self.sat += 'reach\n'

        r = self.reach + 1 
        for i in range(self.rows):
            for j in range(self.columns):
                self.sat += "%d 0\n" % (r)
                self.sat_counter += 1
                r += (self.rows*self.columns) + 1
        
        r = self.reach 
        for i in range(self.rows):
            for j in range(self.columns):
                for k in range(self.rows):
                    for l in range(self.columns):
                            r += 1
                            up, down, left, right = self.getCoordValues(k,l)
                            r2 = self.reach + (i*self.columns+j)*self.rows*self.columns+k*self.columns+l+1
                            if (k != 0 ) :
                                self.sat += "-%d %d %d 0\n" % (r,up,r2-self.columns)
                                self.sat_counter += 1
                            if (k != self.rows-1 ): 
                                self.sat += "-%d %d %d 0\n" % (r,down,r2+self.columns)
                                self.sat_counter += 1
                            if (l != 0 ) :
                                self.sat += "-%d %d %d 0\n" % (r,left,r2-1)
                                self.sat_counter += 1
                            if (l != self.columns-1 ): 
                                self.sat += "-%d %d %d 0\n" % (r,right,r2+1)
                                self.sat_counter += 1
                                
    def addInnerReacheable(self):
        for i in range(self.rows):
            for j in range(self.columns):
                for k in range(self.rows):
                    for l in range(self.columns):
                        z0 = self.walls + i*self.columns + j + 1
                        z1 = self.walls + k*self.columns + l + 1
                        r = self.reach + (i*self.columns+j)*self.rows*self.columns+k*self.columns+l+1
                        self.sat += "-%d -%d %d 0\n" % (z0,z1,r)
                        self.sat_counter += 1

    def addNeighbors(self,i,j):
        up, down, left, right = self.getCoordValues(i,j)
        #CLAUSES UP AND DOWN
        if up-1 == 0:
            #Esquina superior Izquierda
            self.sat += "-%d %d 0\n" % (up, left)
            self.sat += "-%d %d %d 0\n" % (up,right,up+1)
            self.sat_counter += 2
        elif up%self.columns == 0 && rigth-(self.columns+1) <= (self.row+1)*self.columns:
            #esquina superior derecha
            self.sat += "-%d %d 0\n" % (up, right)
            self.sat += "-%d %d %d 0\n" % (up,left,up-1)
            self.sat_counter += 2
        elif down%self.columns == 1 && rigth+(self.columns+1) > self.walls:
            #Esquina inferior izquierda
            self.sat += "-%d %d 0\n" % (down, left)
            self.sat += "-%d %d %d 0\n" % (down,right,down+1)
            self.sat_counter += 2
        elif down+1 > (self.rows+1)*self.columns:
            #Esquina Inferior Derecha
            self.sat += "-%d %d 0\n" % (down, right)
            self.sat += "-%d %d %d 0\n" % (down,left,down-1)
            self.sat_counter += 2
        elif i == 0:
            #Superior
            self.sat += "-%d %d %d 0\n" % (up, left, up-1)
            self.sat += "-%d %d %d 0\n" % (up, right, up+1)
            self.sat_counter += 2
        elif up%self.columns == 1:
            #IZQUIERDO
            self.sat += "-%d %d %d 0\n" % (up, left, left-(self.columns+1))
            self.sat += "-%d %d %d %d 0\n" % (up, right, right-(self.columns+1), up+1)
            self.sat_counter += 2
        elif up%self.columns == 0:
            #DERECHO
            self.sat += "-%d %d %d 0\n" % (up, right, right-(self.columns+1))
            self.sat += "-%d %d %d %d 0\n" % (up, left, left-(self.columns+1), up-1)
            self.sat_counter += 2
        else:
            #General
            self.sat += "-%d %d %d %d 0\n" % (up, left, up-1, left-(self.columns+1))
            self.sat += "-%d %d %d %d 0\n" % (up, right, right-(self.columns+1), up+1)
            self.sat_counter += 2

        if i == self.rows-1:
            #CASO DOWN
            self.sat += "-%d %d %d 0\n" % (down, left, down-1)
            self.sat += "-%d %d %d 0\n" % (down, right, down+1)
            self.sat_counter += 2


    def test(self):
        z = self.walls
        test =""
        for i in range(self.rows):
            for j in range(self.columns):
                z +=1
                test += " -" + str(z)
        test += " 0\n"
        self.sat += test
        self.sat_counter += 1

    def getCoordValues(self,i,j):
        up      = i*self.columns + j + 1
        down    = (i + 1)*self.columns + j +  1
        left    = (self.rows + 1)*self.columns + i*(self.columns+1)+j+1
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


