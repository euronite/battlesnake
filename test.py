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



    def getNearestFood(self, data):
        '''
        Returns None if no food on board, otherwise returns the coords of the nearest food 

        Input:
        data: dict of json data
        
        Output:
        coord: tuple of coords, (x,y)
        '''


        head = data["you"]["head"]
        head_coords = (head["x"], head["y"])

        food_coord_set = set(map(lambda coord_dict : (coord_dict["x"], coord_dict["y"]), data["board"]["food"]))

        seen_set = {head_coords}
        return self.BFS(head_coords, food_coord_set, seen_set)




    def BFS(self, curr_coord, food_coord_set, seen_set)   
        if curr_coord in food_coord_set: 
            #might not always go for same food everytime?
            return curr_coord   
        adj_coords = {("right",(head["x"]+1, head["y"])), ("left", ( head["x"]-1,head["y"])), ("up",( head["x"], head["y"]+1)), ("down", (head["x"], head["y"]-1))}

        for coord in adj_coords:
            if isValidCoord(coord) and coord not in seen_set:
                seen_set.add(coord)
                result =  BFS(coord, food_coord_set, seen_set)
                if result:
                    return result   
        return None 

            


    def isValidCoord(self):
        pass