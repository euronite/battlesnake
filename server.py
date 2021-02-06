import os
import random
import json
import collections
import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see
https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Chad Snake",
            "color": "#FFFF00",
            "head": "gamer",
            "tail": "coffee",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):


        data = cherrypy.request.json
        snake_id = data["you"]["id"]

        possible_moves = self.get_valid_moves(data)
        print(possible_moves)

        move = "up" #Default choice

        if len(possible_moves) != 0:
            food_coord = self.getNearestFood(data)

            if food_coord:
                move = min(possible_moves, key=lambda p: abs(p[1][0]-food_coord[0])**2 + abs(p[1][1] - food_coord[1])**2)[0]
            else:
                move = random.choice(possible_moves)[0]


        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

    def get_valid_moves(self, data):
        """
        This is a valid move calculator.


        Output:

        possible_moves: a tuple of the move direction and corresponding coordinate -> (dir, coord)
        """


        head = data["you"]["head"]

        adjacent_coords = {
            ("right",(head["x"]+1, head["y"])), 
            ("left", ( head["x"]-1,head["y"])), 
            ("up",( head["x"], head["y"]+1)), 
            ("down", (head["x"], head["y"]-1))
        }


        possible_moves = []
        for dir, coord in adjacent_coords:
            # call distance checker to check for valid coords that aren't immediate ded ends.
            if not self.distance_checker(data, coord):
                continue
            if self.isValidMove(data, coord, False):
                if self.canKill(data, coord):
                    print("killing")
                    return [(dir, coord)]
                if self.isValidMove(data, coord, True):
                    possible_moves.append((dir, coord))


        if len(possible_moves) == 0:
            for dir, coord in adjacent_coords:
                if self.going_to_headbutt(data, coord, data["you"]["id"]):
                    possible_moves.append((dir, coord))
                
        return possible_moves


    def isValidMove(self, data, coord, count_headbutt):
        """
        data: json file from server
        coord: tuple (x,y) that is being checked.
        count_headbutt: Boolean -> if True then move is invalid if it leads to a headbutt
        return: in_bounds, is_empty_space, wont_headbutt. Boolean.
        """
        height = data["board"]["height"]
        width = data["board"]["width"]

        invalid_coords = set()
        for snake in data["board"]["snakes"]:
            snake_body_parts = snake["body"] 
            for part in snake_body_parts:
                invalid_coords.add((part["x"],part["y"]))
                

        in_bounds = coord[0] < width and coord[1] < height and coord[0] >= 0 and coord[1] >= 0
        is_empty_space = coord not in invalid_coords

        our_snake_id = data["you"]["id"]
        wont_headbutt = not self.going_to_headbutt(data, coord, our_snake_id) if count_headbutt else True

        #if not count_headbutt:
        #    print(f"invalid coord list: {invalid_coords}")
        #    print(f"curr coord: {coord}")


        return in_bounds and is_empty_space and wont_headbutt 


    def going_to_headbutt(self, data, coord, our_snake_id):

        adjacent_coords = {
            (coord[0]+1, coord[1]), 
            (coord[0]-1, coord[1]), 
            (coord[0], coord[1]+1), 
            (coord[0], coord[1]-1)
        }


        other_snake_lst = list(filter(lambda x: x["id"] != our_snake_id, data["board"]["snakes"]))
        other_head_coords = set(map(lambda snake: (snake["head"]["x"], snake["head"]["y"]), other_snake_lst))

        #print(f"these are the adjacent coords: {adjacent_coords}")
        #print(f"These are the otehr head coords: {other_head_coords}")
        #print(f"This is their intersection: {adjacent_coords.intersection(other_head_coords)} \n")
        if len(adjacent_coords.intersection(other_head_coords)) == 0:
            return False

        return True

    def getNearestFood(self, data):
        '''
        Returns None if no food on board, otherwise returns the coords of the nearest food 

        Input:
        data: dict of json data
        
        Output:
        coord: tuple of coords, (x,y)
        '''


        head = data["you"]["head"]
        head_coord = (head["x"], head["y"])
        food_coord_set = set(map(lambda coord_dict : (coord_dict["x"], coord_dict["y"]), data["board"]["food"]))


        result = self.BFS(head_coord, food_coord_set, data)

        return result




    def BFS(self, curr_coord, food_coord_set, data):

        node_queue = collections.deque([curr_coord])
        seen_set = {curr_coord}

        while node_queue:

            next_coord = node_queue.pop()

            if next_coord in food_coord_set:
                return next_coord

            x, y  = next_coord

            adj_coords = {
            (x+1, y), 
            (x-1,y), 
            (x, y+1), 
            (x, y-1)
            }

            for coord in adj_coords:
                if self.isValidMove(data, coord, True) and coord not in seen_set:
                    seen_set.add(coord)
                    node_queue.appendleft(coord)

        return None

    def canKill(self, data, coord):
        
        #We know we can kill when there is a collision point to move into
        #i.e. a valid point
        #AND a snake within one space of the coord we want to move tools
        #This function will check if there is a head in an adjacent space

        our_snake_id = data["you"]["id"]
        
        adjacent_coords = {
            (coord[0]+1, coord[1]), 
            (coord[0]-1, coord[1]), 
            (coord[0], coord[1]+1), 
            (coord[0], coord[1]-1)
        }
        
        other_snake_lst = list(filter(lambda x: x["id"] != our_snake_id, data["board"]["snakes"]))
        other_head_coords = set(map(lambda snake: (snake["head"]["x"], snake["head"]["y"], snake["length"]), other_snake_lst))



        for x, y, enemy_length in other_head_coords:
            if (x,y) in adjacent_coords:
                #print(f"valid move result is: {self.isValidMove(data, (x,y), False)}")
                print(f"our length vs enemy length: {data['you']['length']} v. {enemy_length}")
            if (x,y) in adjacent_coords  and enemy_length < data["you"]["length"]:
                return True
        
        return False
            

    def distance_checker(self, data, dest_coords):
        adjacent_coords = {
            ("right", (dest_coords[0]+1, dest_coords[1])), 
            ("left", ( dest_coords[0]-1, dest_coords[1])), 
            ("up",( dest_coords[0], dest_coords[1]+1)), 
            ("down", (dest_coords[0], dest_coords[1]-1))
        }

        counter = 0
        for dir, coord in adjacent_coords:
            if self.isValidMove(data, coord, False):
                counter += 1


        if counter > 0:
            return True
        else:
            return False

            



if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
