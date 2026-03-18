import entity_base

class Player(entity_base.EntityBase):
    def __init__(self, name, entity_type, position, velocity):
        super().__init__(name, entity_type, position, velocity)

    def update(self, dt, action):
        self.move(dt, action)
        pass

    def draw(self, surface):
        pass

    def move(self, dt, action):
        match action:
            case "LEFT":
                self.position.x -= self.velocity.x * dt
            case "RIGHT":
                self.position.x += self.velocity.x * dt
            case "JUMP":
                self.position.y -= self.velocity.y * dt
            case "CROUCH":
                self.position.y -= self.velocity.y * dt