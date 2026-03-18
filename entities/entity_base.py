class EntityBase:

    def __init__( self, name, e_type, position, velocity):
        self.name = name
        self.e_type = e_type
        self.position = position
        self.velocity = velocity


    def update(self, dt):
        pass

    def draw(self, surface):
        pass



