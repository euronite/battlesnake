import os
import random
import json

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
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        snake_id = data["you"]["id"]

        possible_moves = {"up", "down", "left", "right"}

        possible_moves = self.get_valid_moves(data, possible_moves)

        move = random.choice(list(possible_moves)) if len(possible_moves) else "up"
        print(f"Chosen move: {move}")
        print(f"Available moves: {possible_moves}")

        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

    def get_valid_moves(self, data, possible_moves):
        """
        This is a valid move calculator.
        """

        # TODO check if there's two snake heads one block apart, if bigger, valid move else abort.
        # TODO invlaid if colliding with other snake

        head = data["you"]["head"]

        adjacent_coords = {
            ("right",(head["x"]+1, head["y"])), 
            ("left", ( head["x"]-1,head["y"])), 
            ("up",( head["x"], head["y"]+1)), 
            ("down", (head["x"], head["y"]-1))
        }


        possible_moves = []
        for dir, coord in adjacent_coords:
            if self.isValidMove(data, coord):
                possible_moves.append(dir)


        if len(possible_moves) == 0:
            for dir, coord in adjacent_coords:
                if not self.going_to_headbutt(data, coord, data["you"]["id"]):
                    possible_moves.append(dir)
                
        return possible_moves


    def isValidMove(self, data, coord):

            height = data["board"]["height"]
            width = data["board"]["width"]

            invalid_coords = set()
            for snake in data["board"]["snakes"]:
                for part in snake["body"]:
                    invalid_coords.add((part["x"],part["y"]))


            in_bounds = coord[0] < width and coord[1] < height and coord[0] >= 0 and coord[1] >= 0
            is_empty_space = coord not in invalid_coords

            our_snake_id = data["you"]["id"]
            wont_headbutt = not self.going_to_headbutt(data, coord, our_snake_id)

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

        if len(adjacent_coords.intersection(other_head_coords)) == 0:
            return False

        return True




    def headbutt_check(self, data, possible_moves, our_head, other_heads):
        # Get other snek heads
        # Check all sneks that are x +- 2 or y +- 2
        # eliminate that direction from the valid moves
        
        head_coords = {(("right"),(our_head["x"]+2, our_head["y"])), (("left"), (our_head["x"]-2, our_head["y"])), (("up"),( our_head["x"], our_head["y"]+2)), (("down"), (our_head["x"], our_head["y"]-2)), (("up", "right"),(our_head["x"]+1, our_head["y"]+1)), (("up","left"),(our_head["x"]-1, our_head["y"]+1)), (("down","left"),(our_head["x"]-1, our_head["y"]-1)), (("down","right"),(our_head["x"]+1, our_head["y"]-1))}

        #print(f"possible_moves before head check {possible_moves}")
        bad_head_coords = []
        for head in other_heads:
            bad_head_coords.append((head["x"], head["y"]))

        for dir_lst, coord in head_coords:
            for dir in dir_lst:
                # if dir_lst > 1:
                    #dir = random.choice(dir_lst)
                #else
                #   dir = dir_lst[0]
                if coord in bad_head_coords and dir in possible_moves:
                    possible_moves.remove(dir)
                    print(f"headbutt direction {dir}")

        #print(f"possible_moves after head check {possible_moves}")
        return possible_moves

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
