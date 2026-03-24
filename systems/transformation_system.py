from forms.base_form import BaseForm
from forms.bat_form import BatForm
from forms.slime_form import SlimeForm

class TransformationSystem:
    def __init__(self):
        self.forms = [BaseForm(), SlimeForm(), BatForm()]
        self.index = 0


    def transform(self, player):
        if player.level >= 5:
            self.index = (self.index + 1) % len(self.forms)
            player.form = self.forms[self.index]
            player.form.apply(player)
        elif player.level >= 3:
            self.index = (self.index + 1) % (len(self.forms) - 1)
            player.form = self.forms[self.index]
            player.form.apply(player)

        elif player.level >= 2:
            self.index = (self.index + 1) % (len(self.forms) - 2)
            player.form = self.forms[self.index]
            player.form.apply(player)