
"""
Solve the 8-puzzle using various search algorithms, including
two Best-First algorithms: (1) MisplacedTiles and (2) ManhattenDistance
as heuristics.

# originally implemented in Python v2.x by Kelsey Hichens '13
# converted to v3.x (mdl, 08/01/2012)
      % 2to3 -w code.py

# this code is mostly unfinished (mdl, 02/18/2025)

# this code is now finished (aws, 03/06/2025)
"""
import timeit
import queue
from BoardClass import *

#=====================================================
def main() -> None:
    """Main function to run the 8-puzzle solver."""

    
    # Create a new Board instance
    b = BoardClass()
    b.initializePuzzleBoard()

    # print starting board
    print("\nStarting Board")
    print(b)

    # algorithm menu
    print("\nChoose the search algorithm:")
    print("1. A* Search")
    print("2. Best First Search")
    print("3. Depth First Search")
    
    choice = input("Enter the number of your choice: ")

    if choice == '1':
        alg = ASTAR
    elif choice == '2':
        alg = BestFS
    elif choice == '3':
        alg = DepthFS
    else:
        print("Invalid choice. Defaulting to A* Search.")
        alg = ASTAR

    # Run algorithm
    if alg(b):
        print("YES")
    else:
        print("DANG!")
    

    #Run algorithm comparison comment path printer
    #algComparer(3)
    #BFSvsASTAR(10)





#=====================================================
def ASTAR(startingBoard: BoardClass) -> bool:
    """Solves 8puzzle by A* Search and print the path to console and stats to a csv file"""

    # Open csv and write header
    FOUT = open("resultsASTAR.csv", 'w')
    FOUT.write("ASTAR Search Stats\n")
    FOUT.write("Board Number, Queue Size, Visted List Size, Time(milliseconds)\n")
    
    
    # Create a PriorityQueue instance
    # each item PUSHED (put) onto the Queue will be a tuple:  (TotalCostScore, tieBreakerValue, theNode)
    Q = queue.PriorityQueue()	
    # tie breaker value/ board number
    numberOfItemsAddedToQueue = 0

    # Push the starting board onto the empty queue and visited list
    Q.put( (startingBoard.Cost, numberOfItemsAddedToQueue, startingBoard) )
    numberOfItemsAddedToQueue += 1
    visited = [startingBoard]

    # helper variables
    foundSolution = False
    nextTry = 0
    maxQueueSize = 0

    # start the timer
    startTime = timeit.default_timer()

    while not Q.empty():
        # check timer write stats to csv
        elapsedTime = timeit.default_timer() - startTime
        FOUT.write("%d,%d,%d,%.12f\n" % (nextTry, Q.qsize(), len(visited), elapsedTime*1000))
        
        # Track max queue size
        maxQueueSize = max(maxQueueSize, Q.qsize())

        # Get the node with the lowest Cost score
        currentCost, tieBreaker, currentNode = Q.get()

        # Check if the current node has been visited before
        for board in visited:
            if currentNode.sameBoard(board): continue

        # not visited? visit it
        visited.append(currentNode)

        # Check if the current node is the goal
        if currentNode.isGoal():
            foundSolution = True
            print("ASTAR: Solution found!")
            
            # Trace back the path from the goal to the start
            print("Path: \n")
            stack = []
            while currentNode:
                stack.append(currentNode)
                currentNode = currentNode.Parent
            while stack:
                board = stack.pop()
                print(str(board) + "\n")
            
             
            FOUT.write("Max Queue Size: %d\n" % maxQueueSize)
            print("ASTAR: Max Queue Size: %d\n" % maxQueueSize)

            FOUT.close()
            return foundSolution

        # Generate Children
        children = currentNode.createChildrenBoards()

        # check if children is in visited list, if not add to queue, else skip
        for child in children:
            isVisited = False
            for board in visited:
                if child.sameBoard(board):
                    isVisited = True
                    break

            if not isVisited:
                Q.put((child.Cost, numberOfItemsAddedToQueue, child))
                numberOfItemsAddedToQueue += 1
                
        # Progress counter/ program stopper
        nextTry += 1
        if nextTry >= 10000:
            print("ASTAR is bad... giving up")
            FOUT.write("Max Queue Size: %d\n" % maxQueueSize)
            print("ASTAR: Max Queue Size: %d\n" % maxQueueSize)
            FOUT.close()

            return foundSolution
        if nextTry % 1000 == 0:
            print(f"ASTAR still searching... {nextTry} boards explored")


    # code broken?!?
    print("No Solution ... ???")
    FOUT.close()

    return foundSolution


#=====================================================
def BestFS(startingBoard: BoardClass) -> bool:
    """Solve 8puzzle by Best First Search and print the path to console and stats to a csv file"""

    # Open csv and write header
    FOUT = open("resultsBFS.csv", 'w')
    FOUT.write("Best First Search Stats\n")
    FOUT.write("Board Number, Queue Size, Visted List Size, Time(milliseconds)\n")
    
    # Create a PriorityQueue instance
    # each item PUSHED (put) onto the Queue will be a tuple:  (heuristicScore, tieBreakerValue, theNode)
    Q = queue.PriorityQueue()	
    numberOfItemsAddedToQueue = 0

    # Push the starting board onto the empty queue and visited list
    Q.put( (startingBoard.Heuristic, numberOfItemsAddedToQueue, startingBoard) )
    numberOfItemsAddedToQueue += 1
    visited = [startingBoard]

    # helper variables
    foundSolution = False
    nextTry = 0
    maxQueueSize = 0

    # start the timer
    startTime = timeit.default_timer()

    while not Q.empty():
        # check timer write stats to csv
        elapsedTime = timeit.default_timer() - startTime
        FOUT.write("%d,%d,%d,%.12f\n" % (nextTry, Q.qsize(), len(visited), elapsedTime*1000))

        # Track max queue size
        maxQueueSize = max(maxQueueSize, Q.qsize())

        # Get the node with the lowest heuristic score
        currentHeuristic, tieBreaker, currentNode = Q.get()

        # Check if the current node has been visited before
        for board in visited:
            if currentNode.sameBoard(board): continue

        # not visited? visit it
        visited.append(currentNode)

        # Check if the current node is the goal
        if currentNode.isGoal():
            foundSolution = True
            print("BFS: Solution found!")
            
            # Trace back the path from the goal to the start
            print("Path: \n")
            stack = []
            while currentNode:
                stack.append(currentNode)
                currentNode = currentNode.Parent
            while stack:
                board = stack.pop()
                print(str(board) + "\n")
            
            FOUT.write("Max Queue Size: %d\n" % maxQueueSize)
            print("BFS: Max Queue Size: %d\n" % maxQueueSize)

            FOUT.close()
            return foundSolution

        # Generate Children
        children = currentNode.createChildrenBoards()

        # check if children is in visited list, if not add to queue, else skip
        for child in children:
            isVisited = False
            for board in visited:
                if child.sameBoard(board):
                    isVisited = True
                    break

            if not isVisited:
                Q.put((child.Heuristic, numberOfItemsAddedToQueue, child))
                numberOfItemsAddedToQueue += 1

        # Progress counter/ program stopper
        nextTry += 1
        if nextTry >= 10000:
            print("BFS is bad... giving up")
            FOUT.write("Max Queue Size: %d\n" % maxQueueSize)
            print("BFS: Max Queue Size: %d\n" % maxQueueSize)
            FOUT.close()

            return foundSolution
        if nextTry % 1000 == 0:
            print(f"BFS still searching... {nextTry} boards explored")


    # code broken?!?
    print("No Solution ... ???")
    FOUT.close()

    return foundSolution


#=====================================================
def DepthFS(startingBoard: BoardClass) -> bool:
    """Solve 8puzzle by DFS(up, right, down, left) and print the path to console and stats to a csv file"""

    # Open csv and write header
    FOUT = open("resultsDFS.csv", 'w')
    FOUT.write("Depth First Search Stats\n")
    FOUT.write("Board Number, Stack Size, Visted List Size, Time(milliseconds)\n")

    # Create a stack/ visted list and push the starting board onto it
    stack = []
    stack.append(startingBoard)
    visited = [startingBoard]

    # helper variables
    foundSolution = False
    nextTry = 0
    maxStackSize = 0

    # start the timer
    startTime = timeit.default_timer()

    while stack:
        # check timer write stats to csv
        elapsedTime = timeit.default_timer() - startTime
        FOUT.write("%d,%d,%d,%.12f\n" % (nextTry, len(stack), len(visited), elapsedTime*1000))

        # Track max stack size
        maxStackSize = max(maxStackSize, len(stack))

        # Get the 'last in' node from the top of the stack
        currentNode = stack.pop()

        # Check if the current node has been visited before
        for board in visited:
            if currentNode.sameBoard(board): continue

        # not visited? visit it
        visited.append(currentNode)

        # Check if the current node is the goal
        if currentNode.isGoal():
            foundSolution = True
            print("DFS: Solution found!")
            
            # Trace back the path from the goal to the start
            print("Path: \n")
            path = []
            while currentNode:
                path.append(currentNode)
                currentNode = currentNode.Parent
            while path:
                board = path.pop()
                print(str(board) + "\n")
            
            FOUT.write("Max Stack Size: %d\n" % maxStackSize)
            print("DFS: Max Stack Size: %d\n" % maxStackSize)
            
            FOUT.close()
            return foundSolution

        # Generate Children
        children = currentNode.createChildrenBoards()

        # check if children is in visited list, if not add to stack, else skip
        for child in children:
            isVisited = False
            for board in visited:
                if child.sameBoard(board):
                    isVisited = True
                    break

            if not isVisited:
                stack.append(child)

        # Progress counter/ program stopper
        nextTry += 1
        if nextTry >= 10000:
            print("DFS is bad... giving up")
            FOUT.write("Max Stack Size: %d\n" % maxStackSize)
            print("DFS: Max Stack Size: %d\n" % maxStackSize)
            FOUT.close()

            return foundSolution
        if nextTry % 1000 == 0:
            print(f"DFS still searching... {nextTry} boards explored")

    # code broken?!?
    print("No Solution ... ???")
    FOUT.close()

    return foundSolution


#=====================================================
def algComparer(numTrials: int) -> None:
    """Run the 8-puzzle solver using all three algorithms and compare the run times."""

    # Open csv and write header
    FOUT1 = open("RunTimes.csv", 'w')
    FOUT1.write("Run Time(milliseconds) - Algorithm Comparison\n")
    FOUT1.write("Trial Number, ASTAR(time, outcome), BestFS(time, outcome), DepthFS(time, outcome)\n")

    for i in range(numTrials):
        # Create a new Board instance
        b = BoardClass()
        b.initializePuzzleBoard()

        # start ASTAR the timer
        ASTAROutcome = "Failed"
        startTimeASTAR = timeit.default_timer()
        if ASTAR(b):
            elapsedTimeASTAR = timeit.default_timer() - startTimeASTAR
            ASTAROutcome = "Success"
        else:
            elapsedTimeASTAR = timeit.default_timer() - startTimeASTAR

        # start BestFS the timer
        BFSOutcome = "Failed"
        startTimeBestFS = timeit.default_timer()
        if BestFS(b):
            elapsedTimeBestFS = timeit.default_timer() - startTimeBestFS
            BFSOutcome = "Success"
        else:
            elapsedTimeBestFS = timeit.default_timer() - startTimeBestFS

        # start DepthFS the timer
        DFSOutcome = "Failed"
        startTimeDepthFS = timeit.default_timer()
        if DepthFS(b): 
            elapsedTimeDepthFS = timeit.default_timer() - startTimeDepthFS
            DFSOutcome = "Success"
        else:
            elapsedTimeDepthFS = timeit.default_timer() - startTimeDepthFS

        # write run times to csv
        FOUT1.write("%d,%.12f,%s,%.12f,%s,%.12f,%s\n" % (i, elapsedTimeASTAR*1000, ASTAROutcome, elapsedTimeBestFS*1000, BFSOutcome, elapsedTimeDepthFS*1000, DFSOutcome))
    


#=====================================================
def BFSvsASTAR(numTrials: int) -> None:
    """Run the 8-puzzle solver using BFS/ASTAR and compare the run times. DFS not included due to being too slow."""

    # Open csv and write header
    FOUT1 = open("BFSvsASTAR.csv", 'w')
    FOUT1.write("Run Time(milliseconds) - ASTAR vs BestFS Comparison\n")
    FOUT1.write("Trial Number, ASTAR(time, outcome), BestFS(time, outcome)\n")

    for i in range(numTrials):
        # Create a new Board instance
        b = BoardClass()
        b.initializePuzzleBoard()

        # start ASTAR the timer
        ASTAROutcome = "Failed"
        startTimeASTAR = timeit.default_timer()
        if ASTAR(b):
            elapsedTimeASTAR = timeit.default_timer() - startTimeASTAR
            ASTAROutcome = "Success"
        else:
            elapsedTimeASTAR = timeit.default_timer() - startTimeASTAR

        # start BestFS the timer
        BFSOutcome = "Failed"
        startTimeBestFS = timeit.default_timer()
        if BestFS(b):
            elapsedTimeBestFS = timeit.default_timer() - startTimeBestFS
            BFSOutcome = "Success"
        else:
            elapsedTimeBestFS = timeit.default_timer() - startTimeBestFS

        # write run times to csv
        FOUT1.write("%d,%.12f,%s,%.12f,%s\n" % (i, elapsedTimeASTAR*1000, ASTAROutcome, elapsedTimeBestFS*1000, BFSOutcome))

#=====================================================

#-----------\
# START HERE \
#-----------------------------------------------------------
if __name__ == '__main__':
    main()

#-----------------------------------------------------
