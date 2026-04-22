import mesa

class MovingAgent(mesa.Agent):
    def __init__(self, model, position, colour):
        self.colour = colour
        self.position = position
        self.counter = 0
        super().__init__(model)

    def step(self):
        print("counter increased")
        self.counter +=1


