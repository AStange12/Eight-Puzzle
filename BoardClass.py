# BoardClass.py
""" Class for instances of 8puzzle Boards
"""

import string

class BoardClass():
    """NxN board to solve [(N^2)-1]-puzzle"""

    # class members (all instances use these same values)
    N = 3

    GOAL  = [ [0, 1, 2], [3, 4, 5], [6, 7, 8] ]

    # used with Manhattan Distance heuristic only:
    # hash table of (row,col) locations for each tile
    # (set in initializeBoard() below)
    # e.g.  BoardClass.GoalTiles[0] = [0,0]
    GoalTiles = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]

    #=====================================================
    def __init__(self) -> None:
        """Constructor to initialize the board and its attributes"""
        
        # setup board (set bogus values)
        self.Board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        # (X,Y) = current location of the EMPTY TILE (0)
        self.X = -1   # ROW
        self.Y = -1   # COL

        # set bogus values for Parent, PathLength, Heuristic, Cost
        import math
        self.Parent = None
        self.PathLength = math.inf
        self.Heuristic = math.inf
        self.Cost = math.inf

    #=====================================================
    def copyCTOR(self) -> 'BoardClass':
        """Creates a copy of the current board"""

        newBoard = BoardClass()
        newBoard.Board = []

        # copy the boards data
        for nextRow in self.Board:
            newRow = []
            for nextTile in nextRow:
                newRow.append(nextTile)
            newBoard.Board.append(newRow)
        newBoard.X = self.X
        newBoard.Y = self.Y
        newBoard.Parent = self.Parent
        newBoard.PathLength = self.PathLength
        newBoard.Heuristic = self.Heuristic
        newBoard.Cost = self.Cost

        return newBoard

    #=====================================================
    def initializePuzzleBoard(self) -> None:
        """Initialize a random solvable puzzle board and set goal tile locations."""
        
        # set (row,col) locations for each tile in the GOAL
        for row in range(0, BoardClass.N):
            for col in range(0, BoardClass.N):
                BoardClass.GoalTiles[BoardClass.GOAL[row][col]] = [row, col]

        # Generate/initialize a random solvable 8-puzzle board
        import numpy as np
        # generates till board is solvable
        while True:
            # generate a random 1D array of numbers 0 to 8
            puzzle1d = np.arange(BoardClass.N * BoardClass.N)
            np.random.shuffle(puzzle1d)
            # reshape to matrix
            self.Board = puzzle1d.reshape((BoardClass.N, BoardClass.N))
            # find the empty tile
            for i in range(BoardClass.N):
                for j in range(BoardClass.N):
                    if self.Board[i][j] == 0:
                        self.X = i
                        self.Y = j
            # check if solvable
            if self.isSolvable():
                break

        # easy (4 moves)
        # self.Board = [[3, 1, 2], [4, 7, 5], [6, 8, 0]]

        # starting location of OPEN (0) tile
        # self.X = 2
        # self.Y = 2

        # medium
        
        #self.Board = [ [3, 2, 5], [4, 1, 8], [6, 0, 7] ]
        #self.X = 2
        #self.Y = 1

        # hard
        # self.Board = [ [1, 4, 5], [3, 0, 2], [6, 7, 8] ]
        # self.X = 1
        # self.Y = 1

        # Sample Boards
        # Board 1
        #self.Board = [[6, 2, 1], [3, 8, 5], [4, 0, 7]]
        #self.X = 2
        #self.Y = 1

        # Board 2
        #self.Board = [[6, 1, 2], [7, 8, 4], [3, 0, 5]]
        #self.X = 2
        #self.Y = 1

        # Board 3
        #self.Board = [[1, 7, 5], [6, 0, 2], [4, 3, 8]]
        #self.X = 1
        #self.Y = 1


        # Check empty tile in right spot and set default values for Parent, PathLength, Heuristic, Cost
        assert (self.Board[self.X][self.Y] == 0)
        self.PathLength = 0
        self.computeDistanceFromGoal()
        self.Cost = self.Heuristic + self.PathLength

    #=====================================================
    def createChildrenBoards(self) -> list['BoardClass']:
        """ Creates the set of potential children Boards from the current Board """

        # get the current location of the empty tile
        row = self.X
        col = self.Y

        assert( (row >=0 and row < BoardClass.N)
                and
                (col >=0 and col < BoardClass.N) )

        newChildrenBoards = []

        # UP(NORTH): slide empty (0) space up
        if ( row != 0 ):
            #print("Try North ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row-1][col], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row-1][col]
            newBoard.X = row-1
            newBoard.PathLength = self.PathLength + 1
            newBoard.computeDistanceFromGoal()
            newBoard.Cost = newBoard.Heuristic + newBoard.PathLength
            newChildrenBoards.append( newBoard )

        # RIGHT(EAST): slide empty (0) space to right
        if ( col != (self.N - 1) ):
            #print("Try East ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row][col+1], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row][col+1]
            newBoard.Y = col+1
            newBoard.PathLength = self.PathLength + 1
            newBoard.computeDistanceFromGoal()
            newBoard.Cost = newBoard.Heuristic + newBoard.PathLength
            newChildrenBoards.append( newBoard )

        # DOWN(SOUTH): slide empty (0) space down
        if ( row != (self.N - 1) ):
            #print("Try South ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row+1][col], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row+1][col]
            newBoard.X = row+1
            newBoard.PathLength = self.PathLength + 1
            newBoard.computeDistanceFromGoal()
            newBoard.Cost = newBoard.Heuristic + newBoard.PathLength
            newChildrenBoards.append( newBoard )

        # LEFT(WEST): slide empty (0) space to left
        if ( col != 0 ):
            #print("Try West ...")
            newBoard = self.copyCTOR()
            newBoard.Parent = self
            newBoard.Board[row][col-1], newBoard.Board[row][col] = newBoard.Board[row][col], newBoard.Board[row][col-1]
            newBoard.Y = col-1
            newBoard.PathLength = self.PathLength + 1
            newBoard.computeDistanceFromGoal()
            newBoard.Cost = newBoard.Heuristic + newBoard.PathLength
            newChildrenBoards.append( newBoard )

        return newChildrenBoards

    #=====================================================
    def computeDistanceFromGoal(self) -> None:
        """Computes the Manhatten Distance from the Goal board,
        where Manhatten Distance = (sum of misplaced distances for all tiles)"""

        sum = 0

        for row in range(BoardClass.N):
            for col in range(BoardClass.N):
                curTile = self.Board[row][col]

                goalRow, goalCol = BoardClass.GoalTiles[curTile]
                sum += (abs(row - goalRow) + abs(col - goalCol))

        self.Heuristic = sum
    #===================================================== 
    '''
    def computeDistanceFromGoal(self) -> None:
        """Computes the number of misplaced tiles from the Goal board"""
        numberMisplaced = 0

        for row in range(BoardClass.N):
            for col in range(BoardClass.N):
                if (self.Board[row][col] != BoardClass.GOAL[row][col]):
                    numberMisplaced += 1
        
        self.Heuristic = numberMisplaced
    '''
    #=====================================================
    def __str__(self) -> str:
        """ Prints the current Board positions """

        print("-------------")
        print("| %d | %d | %d |" % (self.Board[0][0], self.Board[0][1], self.Board[0][2]))
        print("-------------")
        print("| %d | %d | %d |" % (self.Board[1][0], self.Board[1][1], self.Board[1][2]))
        print("-------------")
        print("| %d | %d | %d |" % (self.Board[2][0], self.Board[2][1], self.Board[2][2]))
        print("-------------")

        return ""

    #=====================================================
    def sameBoard(self, otherBoard: 'BoardClass') -> bool:
        """Check if two boards are exactly identical in tile placement;
        (note that this is different from metric of __eq__
        """

        for row in range(BoardClass.N):
            for col in range(BoardClass.N):
                if (self.Board[row][col] != otherBoard.Board[row][col]): return False

        return True
    
    #=====================================================
    def isGoal(self) -> bool:
        """Check if the current board is the Goal board
        """

        for row in range(BoardClass.N):
            for col in range(BoardClass.N):
                if (self.Board[row][col] != BoardClass.GOAL[row][col]): return False

        return True

    #=====================================================
    def isSolvable(self) -> bool:
        """Check if the current board is solvable
        """

        # Flatten the 2D board array into a 1D array
        arr = [tile for row in self.Board for tile in row]

        # Count the number of inversions
        inv_count = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != 0 and arr[i] != 0 and arr[i] > arr[j]:
                    inv_count += 1

        # Check if the number of inversions is even
        return (inv_count % 2 == 0)




    """ if you use a priority queue, you probably won't need to implement the
        RELATIONAL operators below; however, if you do need to compare two boards:
        if (Board1 > Board2):   # test by Board1.Heuristic < Board2.Heuristic
        then you must implement each relational operator
    """

    #=====================================================
    def __eq__(self, other: 'BoardClass') -> bool:

        return self.Heuristic == other.Heuristic

   #===================================================== NOT USED
    def __ne__(self, other):

        same = False  # assume the worst




        return same

    #=====================================================
    def __lt__(self, other):

        same = False  # assume the worst




        return same

    #=====================================================
    def __le__(self, other):

        same = False  # assume the worst




        return same
