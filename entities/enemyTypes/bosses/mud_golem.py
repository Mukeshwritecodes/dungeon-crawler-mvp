from entities.enemy import Enemy

class MudGolem(Enemy):
    def __init__(self, position, tile_rects, player):
        super().__init__(position, tile_rects, player)
