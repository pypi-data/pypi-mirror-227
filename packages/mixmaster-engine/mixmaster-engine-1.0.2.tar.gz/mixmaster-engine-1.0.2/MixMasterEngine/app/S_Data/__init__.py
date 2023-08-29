from .models import *
from sqlalchemy import func


class Data():

    def __init__(self, engine):
        # Connect Member
        self.engine = engine

    def get_all_items(self):
        return self.engine.query(s_item).all()

    def get_all_monsters(self):
        return self.engine.query(s_monster).all()

    def get_all_castles(self):
        return self.engine.query(s_CastleWarInfo).all()

    def get_all_items_box(self):
        return self.engine.query(s_ItemBox).all()

    def get_all_level_exp(self):
        return self.engine.query(s_LvUserInfo).all()

    def get_all_mixes(self):
        return self.engine.query(s_mix).all()

    def get_all_maps(self):
        return self.engine.query(s_zone).all()

    def get_all_mobs_spawn(self):
        return self.engine.query(s_mob).all()

    def get_all_items_drop(self):
        return self.engine.query(s_mobitem).all()

    def get_all_npc(self):
        return self.engine.query(s_npc).all()

    def get_all_npc_sales(self):
        return self.engine.query(s_npc_sale).all()

    def get_all_crafts(self):
        return self.engine.query(s_Production).all()

    def get_item(self, item_id_or_name):
        if not isinstance(item_id_or_name, bool) and isinstance(item_id_or_name, int) or isinstance(item_id_or_name, str):
            try:
                item_id_or_name = int(item_id_or_name)
                item = self.engine.query(
                    s_item).filter_by(idx=item_id_or_name).first()
            except ValueError:
                item = self.engine.query(s_item).filter(func.lower(s_item.name) ==
                                                        item_id_or_name.lower()).first()
            if item:
                return item
            else:
                raise Warning('Item not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_monster(self, monster_id_or_name):
        if not isinstance(monster_id_or_name, bool) and isinstance(monster_id_or_name, int) or isinstance(monster_id_or_name, str):
            try:
                monster_id_or_name = int(monster_id_or_name)
                monster = self.engine.query(
                    s_monster).filter_by(type=monster_id_or_name).first()
            except ValueError:
                monster = self.engine.query(s_monster).filter(func.lower(s_monster.name) ==
                                                              monster_id_or_name.lower()).first()
            if monster:
                return monster
            else:
                raise Warning('Monster not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_castle_by_map(self, map_id_or_name):
        castle = None
        if isinstance(map_id_or_name, int) and not isinstance(map_id_or_name, bool):
            if map_id_or_name == 101 or map_id_or_name == 102:
                castle = self.engine.query(s_CastleWarInfo).filter_by(
                    zone_idx=map_id_or_name).first()
            else:
                raise Warning('Invalid Castle ID')
        elif isinstance(map_id_or_name, str):
            try:
                map_id_or_name = int(map_id_or_name)
                if map_id_or_name == 101 or map_id_or_name == 102:
                    castle = self.engine.query(s_CastleWarInfo).filter_by(
                        zone_idx=map_id_or_name).first()
                else:
                    raise Warning('Invalid Castle ID')
            except ValueError:
                try:
                    if map_id_or_name.lower() == "magirita":
                        castle = self.engine.query(
                            s_CastleWarInfo).filter_by(zone_idx=101).first()
                    elif map_id_or_name.lower() == "mekrita":
                        castle = self.engine.query(
                            s_CastleWarInfo).filter_by(zone_idx=102).first()
                    else:
                        raise Warning('Invalid Castle Name')
                except Exception as e:
                    raise Warning(f'Error: {e}')
        else:
            raise Warning('Invalid Castle')

        if castle:
            return castle
        else:
            raise Warning('Castle not found')

    def get_boxes_by_item(self, item_id_or_name):
        if not isinstance(item_id_or_name, bool) and isinstance(item_id_or_name, int) or isinstance(item_id_or_name, str):
            try:
                item_id_or_name = int(item_id_or_name)
            except ValueError:
                search = self.get_item(item_id_or_name)
                item_id_or_name = search.idx

            itembox = self.engine.query(
                s_ItemBox).filter_by(add_idx=item_id_or_name).all()
            if itembox:
                return itembox
            else:
                raise Warning('Item not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_items_box(self, box_id_or_name):
        if not isinstance(box_id_or_name, bool) and isinstance(box_id_or_name, int) or isinstance(box_id_or_name, str):
            try:
                box_id_or_name = int(box_id_or_name)

            except ValueError:
                search = self.get_item(box_id_or_name)
                box_id_or_name = search.idx

            itembox = self.engine.query(
                s_ItemBox).filter_by(idx=box_id_or_name).all()
            if itembox:
                return itembox
            else:
                raise Warning('Box not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_exp(self, baselevel):
        if not isinstance(baselevel, bool):
            try:
                baselevel = int(baselevel)
            except ValueError:
                raise Warning(
                    'Baselevel must be number (int)')
            if baselevel < 1 or baselevel > 500:
                raise Warning(
                    'Invalid Baselevel, only valid: 1-500')

            exp = self.engine.query(s_LvUserInfo).filter_by(
                Lv=baselevel).first()
            if exp:
                return exp
            else:
                raise Warning('Baselevel not found')
        else:
            raise Warning(
                'Invalid baselevel class, use only number (int)')

    def get_percent_exp(self, baselevel, exp):
        if isinstance(baselevel, int) and isinstance(exp, int) and not isinstance(baselevel, bool) and not isinstance(exp, bool):
            my_level = baselevel - 1
            search_oldLv = self.get_exp(my_level)
            oldLv = search_oldLv.LvUpExp
            search_BaseLv = self.get_exp(baselevel)
            BaseLv = search_BaseLv.LvUpExp
            aLv = BaseLv - oldLv
            percent = round(float(((exp - oldLv) * 100) / aLv), 2)
            return percent
        else:
            print('Invalid baselevel / exp class, use only number (int)')
            return None

    def get_mix(self, monster_id_or_name):
        if not isinstance(monster_id_or_name, bool) and isinstance(monster_id_or_name, int) or isinstance(monster_id_or_name, str):
            try:
                monster_id_or_name = int(monster_id_or_name)
            except ValueError:
                search = self.get_monster(monster_id_or_name)
                monster_id_or_name = search.type
            mix = self.engine.query(
                s_mix).filter_by(result=monster_id_or_name).all()
            if mix:
                return mix
            else:
                raise Warning('Mix not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_mix_evolutions(self, monster_id_or_name):
        if isinstance(monster_id_or_name, int) or isinstance(monster_id_or_name, str) and not isinstance(monster_id_or_name, bool):
            try:
                monster_id_or_name = int(monster_id_or_name)
            except ValueError:
                search = self.get_monster(monster_id_or_name)
                monster_id_or_name = search.type
            evo = []
            mixes = self.engine.query(
                s_mix).filter_by(mainnum=monster_id_or_name).all()
            for mix in mixes:
                evo.append(mix.result)
            mixes = self.engine.query(
                s_mix).filter_by(subnum=monster_id_or_name).all()
            for mix in mixes:
                evo.append(mix.result)
            if len(evo) > 0:
                return evo
            else:
                raise Warning('No evolutions found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_map(self, map_id_or_name):
        if isinstance(map_id_or_name, int) or isinstance(map_id_or_name, str) and not isinstance(map_id_or_name, bool):
            try:
                map_id_or_name = int(map_id_or_name)
                zone = self.engine.query(
                    s_zone).filter_by(idx=map_id_or_name).first()
            except ValueError:
                zone = self.engine.query(
                    s_zone).filter(func.lower(s_zone.name) == func.lower(map_id_or_name)).first()
            if zone:
                return zone
            else:
                raise Warning('Zone not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_map_spawn(self, map_id_or_name):
        if not isinstance(map_id_or_name, bool) and isinstance(map_id_or_name, int) or isinstance(map_id_or_name, str):
            try:
                map_id_or_name = int(map_id_or_name)
            except ValueError:
                search = self.get_map(map_id_or_name)
                map_id_or_name = search.idx

            mobs = []
            spawn = self.engine.query(s_mob).filter_by(
                zone_idx0=map_id_or_name).all()
            if spawn:
                for sp in spawn:
                    mobs.append(sp.monster_type)
            spawn = self.engine.query(s_mob).filter_by(
                zone_idx1=map_id_or_name).all()
            if spawn:
                for sp in spawn:
                    mobs.append(sp.monster_type)
            spawn = self.engine.query(s_mob).filter_by(
                zone_idx2=map_id_or_name).all()
            if spawn:
                for sp in spawn:
                    mobs.append(sp.monster_type)
            spawn = self.engine.query(s_mob).filter_by(
                zone_idx3=map_id_or_name).all()
            if spawn:
                for sp in spawn:
                    mobs.append(sp.monster_type)
            spawn = self.engine.query(s_mob).filter_by(
                zone_idx4=map_id_or_name).all()
            if spawn:
                for sp in spawn:
                    mobs.append(sp.monster_type)
            spawn = self.engine.query(s_mob).filter_by(
                zone_idx5=map_id_or_name).all()
            if spawn:
                for sp in spawn:
                    mobs.append(sp.monster_type)
            if len(mobs) > 0:
                return set(mobs)
            else:
                raise Warning(
                    'No mob found in Map')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_mob_spawn(self, monster_id_or_name):
        if not isinstance(monster_id_or_name, bool) and isinstance(monster_id_or_name, int) or isinstance(monster_id_or_name, str):
            mobs = []
            try:
                monster_id_or_name = int(monster_id_or_name)
            except:
                search = self.get_monster(monster_id_or_name)
                monster_id_or_name = search.type

            spawn = self.engine.query(s_mob).filter_by(
                monster_type=monster_id_or_name).all()
            if spawn:
                for sp in spawn:
                    if sp.zone_idx0 > 0:
                        mobs.append(sp.zone_idx0)
                    if sp.zone_idx1 > 0:
                        mobs.append(sp.zone_idx1)
                    if sp.zone_idx2 > 0:
                        mobs.append(sp.zone_idx2)
                    if sp.zone_idx3 > 0:
                        mobs.append(sp.zone_idx3)
                    if sp.zone_idx4 > 0:
                        mobs.append(sp.zone_idx4)
                    if sp.zone_idx5 > 0:
                        mobs.append(sp.zone_idx5)
            if len(mobs) > 0:
                return set(mobs)
            else:
                raise Warning(
                    'Mob not spawned')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_items_drop(self, item_id_or_name):
        if not isinstance(item_id_or_name, bool) and isinstance(item_id_or_name, int) or isinstance(item_id_or_name, str):
            try:
                item_id_or_name = int(item_id_or_name)
            except ValueError:
                search = self.get_item(item_id_or_name)
                item_id_or_name = search.idx

            items = []
            all_itens = self.get_all_items_drop()
            for item in all_itens:
                if int(item.item_idx0) == item_id_or_name or int(item.item_idx1) == item_id_or_name or int(item.item_idx2) == item_id_or_name or int(item.item_idx3) == item_id_or_name or int(item.item_idx4) == item_id_or_name or int(item.item_idx5) == item_id_or_name or int(item.item_idx6) == item_id_or_name or int(item.item_idx7) == item_id_or_name or int(item.item_idx8) == item_id_or_name or int(item.item_idx9) == item_id_or_name:
                    items.append(item)

            print(len(items))
            if len(items) > 0:
                return items
            else:
                raise Warning('No drop item found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_npc(self, npc_id_or_name):
        if not isinstance(npc_id_or_name, bool) and isinstance(npc_id_or_name, int) or isinstance(npc_id_or_name, str):
            try:
                npc_id_or_name = int(npc_id_or_name)
                npc = self.engine.query(s_npc).filter_by(
                    idx=npc_id_or_name).first()
            except ValueError:
                npc = self.engine.query(
                    s_npc).filter(func.lower(s_npc.name) == func.lower(npc_id_or_name)).first()
            if npc:
                return npc
            else:
                raise Warning('NPC not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_npc_in_maps(self, map_id_or_name):
        if not isinstance(map_id_or_name, bool) and isinstance(map_id_or_name, int) or isinstance(map_id_or_name, str):
            try:
                map_id_or_name = int(map_id_or_name)
            except ValueError:
                search = self.get_map(map_id_or_name)
                map_id_or_name = search.idx

            zone = self.engine.query(s_npc).filter_by(
                birth_zone_idx=map_id_or_name).all()
            if zone:
                return zone
            else:
                raise Warning('NPC in maps not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_items_npc_sale(self, npc_id_or_name):
        if not isinstance(npc_id_or_name, bool) and isinstance(npc_id_or_name, int) or isinstance(npc_id_or_name, str):
            try:
                npc_id_or_name = int(npc_id_or_name)
            except ValueError:
                npc = self.get_npc(npc_id_or_name)
                npc_id_or_name = npc.idx
            sale = self.engine.query(s_npc_sale).filter_by(
                npc_idx=npc_id_or_name).all()
            if sale:
                return sale
            else:
                raise Warning('Sale not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_book_craft(self, book_id_or_name):
        if not isinstance(book_id_or_name, bool) and isinstance(book_id_or_name, int) or isinstance(book_id_or_name, str):
            try:
                book_id_or_name = int(book_id_or_name)
                craft = self.engine.query(s_Production).filter_by(
                    doc_idx=book_id_or_name).first()
            except ValueError:
                craft = self.engine.query(s_Production).filter_by(
                    doc_name=book_id_or_name).first()
            if craft:
                return craft
            else:
                raise Warning('Craft not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_result_craft(self, item_id_or_name):
        if not isinstance(item_id_or_name, bool) and isinstance(item_id_or_name, int) or isinstance(item_id_or_name, str):
            try:
                item_id_or_name = int(item_id_or_name)
            except ValueError:
                search = self.get_item(item_id_or_name)
                item_id_or_name = search.idx

            craft = self.engine.query(s_Production).filter_by(
                result_idx=item_id_or_name).first()
            if craft:
                return craft
            else:
                raise Warning('Craft result not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')
