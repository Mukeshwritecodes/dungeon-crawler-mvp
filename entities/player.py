import entity_base

class Player(entity_base.EntityBase):
    def __init__(self, position, velocity):
        super().__init__(position, velocity)
