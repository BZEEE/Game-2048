import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0
        
        self._grid = self.createGrid(row, col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells
                 
        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):
        
        board = []
        for i in range(row):
            row = []
            for j in range(col):
                row.append(0)
            board.append(row)
            
        return board
    
    
    def setCell(self, cell, val):
        rowIndex = cell // 4
        colIndex = cell % 4
        self._grid[rowIndex][colIndex] = val
    
        """
        This function should take two arguments cell and val and assign
        the cell of the grid numbered 'cell' the value in val.
        
        This function does not need to return anything.
        
        You should use this function to change values of the grid.
        """
    

    def getCell(self, cell):
        rowIndex = cell // 4
        colIndex = cell % 4        
        return self._grid[rowIndex][colIndex]
    
            

    def assignRandCell(self, init=False):
    
        """
        This function assigns a random empty cell of the grid 
        a value of 2 or 4.
        
        In __init__() it only assigns cells the value of 2.
        
        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned 
        a value of 4
        """
        
        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):
    
        """
        This function draws the grid representing the state of the game
        grid
        """
        
        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)
        print()
    
    
    def updateEmptiesSet(self):
    
        """
        This function should update the list of empty cells of the grid.
        """
        self.emptiesSet = []
        for i in range(self.row):
            for j in range(self.col):
                if self._grid[i][j] == 0:
                    num = (self.col * i) + j
                    self.emptiesSet.append(num)
    
    
    def collapsible(self):
        # checks if any tiles adjacent to each other are equal in value
        check = False
        if self._grid[self.row-1][0] == self._grid[self.row-1][1] or self._grid[self.row-1][1] == self._grid[self.row-1][2] or self._grid[self.row-1][2] == self._grid[self.row-1][3]:
            check = True
        for i in range(self.row-1):
            for j in range(self.col-1):
                if self._grid[i][j] == self._grid[i][j+1]:
                    check = True
                if self._grid[i][j] == self._grid[i+1][j]:
                    check = True
            if self._grid[i][self.row-1] == self._grid[i+1][self.row-1]:
                check = True
        
        """
        This function should test if the grid of the game is collapsible
        in any direction (left, right, up or down.)
        
        It should return True if the grid is collapsible.
        It should return False otherwise.
        """
        
        if len(self.emptiesSet) != 0 or check:
            return True
        else:
            return False
        
    
    


    def collapseRow(self, lst):
    
        """
        This function takes a list lst and collapses it to the LEFT.
        
        This function should return two values:
        1. the collapsed list and
        2. True if the list is collapsed and False otherwise.
        """
        original = tuple(lst)
        k = 0
        blankShift = []
        while k < len(lst):
            if lst[k] == 0:
                blank = lst.pop(k)
                blankShift.append(blank)
                k -= 1
            k += 1
        lst += blankShift
            
        i = 0
        while lst[i] != 0 and i < len(lst)-1:
            if lst[i] == lst[i+1]:
                add = lst.pop(i+1)
                lst[i] += add
                self.score += lst[i]
                lst.append(0)
            i += 1
                
        return lst, list(original) != lst


    def collapseLeft(self):
    
        """
        This function should use collapseRow() to collapse all the rows 
        in the grid to the LEFT.
        
        This function should return True if any row of the grid is collapsed 
        and False otherwise.
        """
        i = 0
        boolArray = []
        for row in self._grid:
            collapsedRow = self.collapseRow(row)
            self._grid[i] = collapsedRow[0]
            boolArray.append(collapsedRow[1])
            i += 1
        
        if True in boolArray:
            return True
        else:
            return False
            
    def collapseRight(self):
    
        """
        This function should use collapseRow() to collapse all the rows 
        in the grid to the RIGHT.
        
        This function should return True if any row of the grid is collapsed 
        and False otherwise.
        """
        i = 0
        boolArray = []
        for row in self._grid:
            row.reverse()
            collapsedRow = self.collapseRow(row)
            collapsedRow[0].reverse()
            self._grid[i] = collapsedRow[0]
            boolArray.append(collapsedRow[1])
            i += 1
        
        if True in boolArray:
            return True
        else:
            return False          


    def collapseUp(self):
    
        """
        This function should use collapseRow() to collapse all the columns
        in the grid to UPWARD.
        
        This function should return True if any column of the grid is 
        collapsed and False otherwise.
        """
        boolArray = []
        for i in range(self.col):
            column = []
            for j in range(self.row):
                column.append(self._grid[j][i])
                
            newColumn = self.collapseRow(column)
            boolArray.append(newColumn[1])
            
            for k in range(self.row):
                self._grid[k][i] = newColumn[0][k]
                
        
        if True in boolArray:
            return True
        else:
            return False        


    def collapseDown(self):

        """
        This function should use collapseRow() to collapse all the columns
        in the grid to DOWNWARD.
        
        This function should return True if any column of the grid is 
        collapsed and False otherwise.
        """

        boolArray = []
        for i in range(self.col):
            column = []
            for j in range(self.row):
                column.append(self._grid[j][i])
            
            column.reverse()    
            newColumn = self.collapseRow(column)
            newColumn[0].reverse()
            boolArray.append(newColumn[1])
            
            for k in range(self.row):
                self._grid[k][i] = newColumn[0][k]
                
        
        if True in boolArray:
            return True
        else:
            return False        



class Game():
    def __init__(self, row=4, col=4, initial=2):
    
        """
        Creates a game grid and begins the game
        """
        
        self.game = Grid(row, col, initial)
        self.play()
    
    
    def printPrompt(self):
        
        """
        Prints the instructions and the game grid with a move prompt
        """
    
        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")
        
        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):
    
        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}
        
        stop = False
        collapsible = True
        
        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')
            
            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()
                
                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()
                    
                collapsible = self.game.collapsible()
                 
        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')


def main():
    game = Game()

main()
