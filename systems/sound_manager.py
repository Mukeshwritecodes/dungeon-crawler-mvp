import pygame

class SoundManager:
    def __init__(self):

        self.sounds = {
            "jump": pygame.mixer.Sound("assets/sounds/jump.wav"),
            "attack": pygame.mixer.Sound("assets/sounds/attack.wav"),
            "hit": pygame.mixer.Sound("assets/sounds/hit.wav"),
            "slime": pygame.mixer.Sound("assets/sounds/slime.wav"),
            "bat": pygame.mixer.Sound("assets/sounds/bat.wav"),
            "death": pygame.mixer.Sound("assets/sounds/death.wav"),
            "running": pygame.mixer.Sound("assets/sounds/running.wav"),
        }

        # Set volumes
        self.sounds["jump"].set_volume(0.3)
        self.sounds["slime"].set_volume(0.3)
        self.sounds["bat"].set_volume(0.2)
        self.sounds["death"].set_volume(0.2)
        self.sounds["attack"].set_volume(0.1)

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()