from math import floor
from utils import constants


class XPSystem:
    def calculate_xp(self, player, enemy_type, xp_gain):
        player.kill_log[enemy_type][0] += 1
        player.kill_log[enemy_type][1] += xp_gain
        print("#-------------------------#")
        print("Kill log:", player.kill_log)

        player.xp += xp_gain

        while player.xp >= player.level_xp:
            player.level += 1
            player.xp = player.xp - player.level_xp
            player.level_xp *= constants.REQ_XP_FACTOR
            player.level_xp = floor(player.level_xp)

            print("Player level:", player.level)
            print("Player Max xp needed:", player.level_xp)
            print("Player xp:", player.xp)
            print("#-------------------------#")
            self.handle_level_buffs(player)

    def handle_level_buffs(self, player):
        pass


