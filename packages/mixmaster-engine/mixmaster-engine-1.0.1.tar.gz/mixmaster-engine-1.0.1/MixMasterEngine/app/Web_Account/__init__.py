
from .models import *
from termcolor import colored
from datetime import datetime


class GameTailMall():

    def __init__(self, engine):
        # Connect Member
        self.engine = engine

    def get_all_game_tail(self):
        return self.engine.query(GameTail).all()

    def get_all_game_tail_event(self):
        return self.engine.query(GameTail_Event).all()

    def get_gametail_by_player(self, player_id_or_name):
        if isinstance(player_id_or_name, int) or isinstance(player_id_or_name, str) and not isinstance(player_id_or_name, bool):
            try:
                player_id_or_name = int(player_id_or_name)
                game = self.engine.query(
                    GameTail).filter_by(GiftIdIdx=player_id_or_name).all()
            except ValueError:
                game = self.engine.query(GameTail).filter_by(
                    GiftPlayerID=player_id_or_name).all()
            if game:
                return game
            else:
                raise Warning(colored('User not found', 'yellow'))
        else:
            raise Warning(
                colored('Invalid search, value must be number or string ', 'yellow'))

    def get_gametail_event_by_player(self, player_id_or_name):
        if isinstance(player_id_or_name, int) or isinstance(player_id_or_name, str) and not isinstance(player_id_or_name, bool):
            try:
                player_id_or_name = int(player_id_or_name)
                game = self.engine.query(
                    GameTail_Event).filter_by(IdIdx=player_id_or_name).all()
            except ValueError:
                game = self.engine.query(GameTail_Event).filter_by(
                    PlayerID=player_id_or_name).all()
            if game:
                return game
            else:
                raise Warning(colored('User not found', 'yellow'))
        else:
            raise Warning(
                colored('Invalid search, value must be number or string ', 'yellow'))

    def get_gametail_by_item(self, item_id):
        if isinstance(item_id, int) or isinstance(item_id, str) and not isinstance(item_id, bool):
            try:
                item_id = int(item_id)
                game = self.engine.query(
                    GameTail).filter_by(ItemIdx=item_id).all()
            except ValueError:
                raise Warning(
                    colored('Invalid search, value must be number ', 'yellow'))
            if game:
                return game
            else:
                raise Warning(colored('User not found', 'yellow'))
        else:
            raise Warning(
                colored('Invalid search, value must be number or string ', 'yellow'))

    def get_gametail_event_by_item(self, item_id):
        if isinstance(item_id, int) or isinstance(item_id, str) and not isinstance(item_id, bool):
            try:
                item_id = int(item_id)
                game = self.engine.query(
                    GameTail_Event).filter_by(ObjectIdx=item_id).all()
            except ValueError:
                raise Warning(
                    colored('Invalid search, value must be number ', 'yellow'))
            if game:
                return game
            else:
                raise Warning(colored('User not found', 'yellow'))
        else:
            raise Warning(
                colored('Invalid search, value must be number or string ', 'yellow'))

    def add_gametail(self, player_name, player_id, item_id, item_quantity, opt, opt_level):
        if not isinstance(player_name, str):
            raise Warning(
                colored('Invalid player name, value must be string ', 'yellow'))
        elif isinstance(player_id, bool) and not isinstance(player_id, str) and not isinstance(player_id, int):
            raise Warning(
                colored('Invalid player id, value must be number ', 'yellow'))
        elif isinstance(item_id, bool) and not isinstance(item_id, str) and not isinstance(item_id, int):
            raise Warning(
                colored('Invalid item id, value must be number ', 'yellow'))
        elif isinstance(item_quantity, bool) and not isinstance(item_quantity, str) and not isinstance(item_quantity, int):
            raise Warning(
                colored('Invalid item quantity, value must be number ', 'yellow'))
        elif isinstance(opt, bool) and not isinstance(opt, str) and not isinstance(opt, int):
            raise Warning(
                colored('Invalid opt, value must be number ', 'yellow'))
        elif isinstance(opt_level, bool) and not isinstance(opt_level, str) and not isinstance(opt_level, int):
            raise Warning(
                colored('Invalid opt level, value must be number ', 'yellow'))
        try:
            player_id = int(player_id)
            item_id = int(item_id)
            item_quantity = int(item_quantity)
            opt = int(opt)
            opt_level = int(opt_level)
        except ValueError:
            raise Warning(
                colored('Invalid values, value must be number', 'yellow'))
        game = GameTail()
        game.GiftPlayerID = player_name
        game.GiftIdIdx = player_id
        game.IdIdx = player_id
        game.ItemIdx = item_id
        game.Qty = item_quantity
        game.Opt = opt
        game.OptLevel = opt_level
        game.RegDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.engine.add(game)
        self.engine.commit()

    def add_gametail_event(self, player_name, player_id, item_id, item_quantity, info):
        if not isinstance(player_name, str):
            raise Warning(
                colored('Invalid player name, value must be string ', 'yellow'))
        elif isinstance(player_id, bool) and not isinstance(player_id, str) and not isinstance(player_id, int):
            raise Warning(
                colored('Invalid player id, value must be number ', 'yellow'))
        elif isinstance(item_id, bool) and not isinstance(item_id, str) and not isinstance(item_id, int):
            raise Warning(
                colored('Invalid item id, value must be number ', 'yellow'))
        elif isinstance(item_quantity, bool) and not isinstance(item_quantity, str) and not isinstance(item_quantity, int):
            raise Warning(
                colored('Invalid item quantity, value must be number ', 'yellow'))
        elif isinstance(info, bool) and not isinstance(info, str) and not isinstance(info, int):
            raise Warning(
                colored('Invalid info, value must be number or string', 'yellow'))
        try:
            player_id = int(player_id)
            item_id = int(item_id)
            item_quantity = int(item_quantity)
        except ValueError:
            raise Warning(
                colored('Invalid values, value must be number', 'yellow'))
        game = GameTail_Event()
        game.PlayerID = player_name
        game.IdIdx = player_id
        game.ObjectIdx = item_id
        game.Qty = item_quantity
        game.Info = info
        game.RegDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.engine.add(game)
        self.engine.commit()
