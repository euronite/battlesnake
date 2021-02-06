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
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#888888",  # TODO: Personalize
            "head": "default",  # TODO: Personalize
            "tail": "default",  # TODO: Personalize
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

        possible_moves = self.valid_move(data, possible_moves)

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

    def valid_move(self, data, possible_moves):
        """
        This is a valid move calculator.
        """

        # TODO check if there's two snake heads one block apart, if bigger, valid move else abort.
        # TODO invlaid if colliding with other snake
        height = data["board"]["height"]
        width = data["board"]["width"]

        head = data["you"]["head"]
        invalid_coords = set()

        for part in data["you"]["body"]:
            invalid_coords.add((part["x"],part["y"]))

        adjacent_coords = {("right",(head["x"]+1, head["y"])), ("left", ( head["x"]-1,head["y"])), ("up",( head["x"], head["y"]+1)), ("down", (head["x"], head["y"]-1))}

        print(f"head coords {head['x']}, {head['y']}")
        print(f"adjacent_coords: {adjacent_coords}")
        possible_moves = []
        for dir, coord in adjacent_coords:

            in_bounds = coord[0] < width and coord[1] < height and coord[0] >= 0 and coord[1] >= 0
            is_empty_space = coord not in invalid_coords

            if in_bounds and is_empty_space:

                possible_moves.append(dir)

        return possible_moves

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
