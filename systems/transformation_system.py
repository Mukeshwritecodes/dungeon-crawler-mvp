from forms.base_form import BaseForm
from forms.bat_form import BatForm
from forms.slime_form import SlimeForm

class TransformationSystem:
    def __init__(self):
        self.forms = [BatForm(), SlimeForm(), BaseForm()]
        self.index = 0

    def transform(self, player):
        self.index = (self.index + 1) % len(self.forms)
        player.form = self.forms[self.index]
        player.form.apply(player)