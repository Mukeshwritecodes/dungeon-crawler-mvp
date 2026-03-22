class CombatSystem:
    def __init__(self):
        pass

    # If the rectangle collides, the target is in the range
    # Will improve the range later
    def in_range(self, attacker_rect, target_rect):
        if attacker_rect.colliderect(target_rect):
            return True
        return False


    def handle_death(self, target):
        if target.health <= 0:
            target.health = 0
            target.is_alive = False

    def attack(self, attacker, target):
        if self.in_range(attacker.rect, target.rect):
            self.calculate_damage(attacker, target)
        else:
            return

    def calculate_damage(self, attacker, target):
            if target.is_alive:
                target.health -= attacker.attack
                self.handle_death(target)








