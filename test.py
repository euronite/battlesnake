import mcts

class NaughtsAndCrossesState():
    def __init__(self, board, mySnakeID):
        self.board = board
        self.currentPlayer = 1 
        self.mySnakeID = mySnakeID


    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        possibleActions = [] # choose from 4 cardinal directions

        # insert check for valid move

        return possibleActions

    def takeAction(self, action):
        # action is up down left or right
        newState = deepcopy(self)
        #Actually make the action here
        if currentPlayer == 1:
            
            #make move  
                #add enw body part in direction moved
                #remove the tail
                #health -= 1

            #if found food
                #reset health to max
                #add another body part to be removed next turn
                #remove food
            


        #newState.board.

        newState.currentPlayer = self.currentPlayer * -1
        return newState

    def isTerminal(self):

        no_actions_left = len(self.getPossibleActions()) == 0
        no_health_left =  self.getHealth() == 0
        if no_actions_left or no_health_left:
          return True

        return False

    def getReward(self):
        if currentPlayer==1:
          return 0

        return 1



    def getHealth(self, targetSnakeID):
        for snake in board.snakes:
          if snake.id = targetSnakeID:
            return snake.health




