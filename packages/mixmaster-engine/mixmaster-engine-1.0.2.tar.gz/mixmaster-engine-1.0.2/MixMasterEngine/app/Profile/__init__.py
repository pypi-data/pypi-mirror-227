from .models import *
import MixMasterEngine as MixMaster


class Profiles():

    def __init__(self, engine, userName):
        # Connect Member
        self.engine = engine
        player = engine.query(Players).filter_by(
            PlayerID=userName).first()
        if player:
            self.profile = player
        else:
            raise Exception('User not found')
        try:
            gamedata = MixMaster.game()
            self.heros = gamedata.get_my_heros(player.id_idx)
        except:
            self.heros = False

    def refresh(self):
        player = self.engine.query(Players).filter_by(
            PlayerID=self.profile.PlayerID).first()
        if player:
            self.profile = player
        else:
            raise Exception('User not found')
        try:
            gamedata = MixMaster.game()
            self.heros = gamedata.get_my_heros(player.id_idx)
        except:
            self.heros = False
