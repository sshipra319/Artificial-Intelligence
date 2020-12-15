
import copy
import random
import sys
#import MiniMax

utility = {}
infinity = float('inf')

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
        self.depth = 1
        
    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    def getPieceCount(self):
        return sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printgameBoard(self):
        print(' -----------------')
        for i in range(6):
            print(' |'),
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print('| ')
        print(' -----------------')

    # Output current game status to file
    def printgameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r')
        self.gameFile.write('%s\r' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1
    
    # Place opponent players piece in the requested column
    def check_piece(self, column, opponent):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    self.gameBoard[i][column] = opponent
                    self.pieceCount += 1
                    return 1

    # The AI section. Currently plays randomly.
    def aiPlay(self):
        randColumn = self.minimax(int(self.depth))
        result = self.playPiece(randColumn)
        if not result:
            print('No Result')
        else:
            print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, randColumn+1))
            self.changeMove()
            
    # To change the player
    def changeMove(self):
      if self.currentTurn == 1:
        self.currentTurn = 2
      elif self.currentTurn == 2:
        self.currentTurn = 1


    # Calculate the number of 4-in-a-row each player has
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1


    # Implementation of Minimax algorithm
    def minimax(self, depth):
      currentState = copy.deepcopy(self.gameBoard)
      for i in range(7):
        if self.playPiece(i) != None:
          if self.pieceCount == 42 or depth == 0:
            self.gameBoard = copy.deepcopy(currentState)
            return i
          else:
            value = self.betaAlpha(self.gameBoard, -infinity, infinity, depth - 1)
            utility[i] = value
            self.gameBoard = copy.deepcopy(currentState)

      maxUtility = max([i for i in utility.values()])
      for i in range (7):
        if i in utility:
          if utility[i] == maxUtility:
            utility.clear()
            return i

    # Function returns the minimum value state
    def mini_value(self, node):
      primaryNode = copy.deepcopy(node)
      if self.currentTurn == 1:
        opponent = 2
      elif self.currentTurn == 2:
        opponent = 1
      newNodes = []
      for i in range(7):
        currentState = self.check_piece(i,opponent)
        if currentState != None:
          newNodes.append(self.gameBoard)
          self.gameBoard = copy.deepcopy(primaryNode)
      return newNodes

     # Function returns the maximum value state
    def maxi_value(self, node):
      primaryNode = copy.deepcopy(node)
      newNodes = []
      for i in range(7):
        currentState = self.playPiece(i)
        if currentState != None:
          newNodes.append(self.gameBoard)
          self.gameBoard = copy.deepcopy(primaryNode)
      return newNodes


    # Performs maximizing operations of alpha beta pruning
    def alphaBeta(self, node, alpha, beta, depth):
      val = -infinity
      newNodes =self.maxi_value(node)
      if newNodes == [] or depth == 0:
        self.countScore()
        return self.evalFunction(self.gameBoard)
      else:
        for n in newNodes:
          self.gameBoard = copy.deepcopy(n)
          val = max(val, self.betaAlpha(node, alpha, beta, depth - 1))
          if val >= beta:
            return val
          alpha = max(alpha, val)
        return val

    # Performs minimizing operations of alpha beta pruning
    def betaAlpha(self, node, alpha, beta, depth):
      val = infinity
      newNodes = self.mini_value(node)
      if newNodes == [] or depth == 0:
        self.countScore()
        return self.evalFunction(self.gameBoard)
      else:
        for n in newNodes:
          self.gameBoard = copy.deepcopy(n)
          val = min(val, self.alphaBeta(node, alpha, beta, depth-1))
          if val <= alpha:
            return val;
          beta = min(beta, val)
      return val       
    
      # To vertically check the streak
    def vertical(self, row, column, state, streak):
      count = 0
      for i in range(row, 6):
        if state[i][column] == state[row][column]:
          count += 1
        else:
          break;
      if count >= streak:
        return 1
      else:
        return 0

      # To horizontally check the streak
    def horizontal(self, row, column, state, streak):
      count = 0
      for j in range(column, 7):
        if state[row][j] == state[row][column]:
          count += 1
        else:
          break
      if column >= streak:
        return 1
      else:
        return 0

     #To daigonally check the streak
    def daigonal(self, row, column, state, streak):
      sum = 0
      count = 0
      j = column
      for i in range(row, 6):
        if j > 6:
          break
        elif state[i][j] == state[row][column]:
          count += 1
        else:
          break
        j+=1
      if count >= streak:
        sum += 1
      count = 0
      j = column
      for i in range(row, -1, -1):
        if j > 6:
          break
        elif state[i][j] == state[row][column]:
          count += 1
        else:
          break
        j += 1
      if count >= streak:
        sum += 1
      return sum


    def evaluation_function(self):
      if self.currentTurn == 1:
        opponent_color = 2
      elif self.currentTurn == 2:
        opponent_color = 1
      return opponent_color


     # To check the type of connect 4 whether it is vertical, horizontal or daigonal
    def streakCalculation(self, state, color, streak):
      count = 0
      for i in range(6):
        for j in range(7):
          if state[i][j] == color:
            count += self.vertical(i, j, state, streak)
            count += self.horizontal(i, j, state, streak)
            count += self.daigonal(i, j, state, streak)
      return count
     
     # Check the streak for computer player
    def computerEval(self, state):
      opponent_color = self.evaluation_function()
      fourComputers = self.streakCalculation(state, opponent_color, 4)
      threeComputers = self.streakCalculation(state, opponent_color, 3)
      twoComputers = self.streakCalculation(state, opponent_color, 2)
      return(fourComputers * 37044 + threeComputers * 882 + twoComputers * 21)
     
     # Check the streak for human player
    def playerEval(self, state):
      fourPlayers = self.streakCalculation(state, self.currentTurn, 4)
      threePlayers = self.streakCalculation(state, self.currentTurn, 3)
      twoPlayers = self.streakCalculation(state, self.currentTurn, 2)
      return(fourPlayers * 37044 + threePlayers * 882 + twoPlayers * 21)

    # Calculate the streak difference of computer and human 
    def evalFunction(self, state):
      self.playerEval(state)
      self.computerEval(state)
      return self.playerEval(state) - self.computerEval(state)

