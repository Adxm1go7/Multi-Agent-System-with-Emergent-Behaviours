import mesa

class MyAgent(mesa.Agent):
    def __init__(self, model, age, position):
        super().__init__(model)
        self.age = age
        self.position = position
    
    def step(self):
        self.age += 1

