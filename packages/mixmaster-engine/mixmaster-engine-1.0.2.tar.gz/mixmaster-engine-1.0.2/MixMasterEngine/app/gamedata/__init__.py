from .models import *
from sqlalchemy import func
from ..functions import *


def check_status_str(status):
    is_valid = {"str", "dex", "aim", "luck"}
    for valid in is_valid:
        if status.lower() == valid:
            return True
    return False


class Game():

    def __init__(self, engine):
        # Connect Member
        self.engine = engine

    def get_my_heros(self, player_id):
        heros = self.engine.query(u_hero).filter_by(
            id_idx=player_id).all()
        if heros:
            return heros
        else:
            raise Warning('Heros not found')

    def get_hero_by_name(self, name):
        if check_string(name):
            hero = self.engine.query(u_hero).filter(
                func.binary(u_hero.name) == name).first()
            if hero:
                return hero
            else:
                raise Warning('Hero not found')
        else:
            raise Warning(
                'Invalid values, value must be string')

    def get_hero_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            if hero_order < 0 or hero_order > 2:
                raise Warning(
                    'Hero order needs to be between 0 to 2')

            hero = self.engine.query(u_hero).filter(
                u_hero.id_idx == hero_id, u_hero.hero_order == hero_order).first()
            if hero:
                return hero
            else:
                raise Warning('Hero not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_hero_login_by_id(self, hero_id, hero_order):
        hero = self.get_hero_by_id(hero_id, hero_order)
        if hero.login == 1:
            return True
        else:
            return False

    def get_hero_login_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 1:
            return True
        else:
            return False

    def get_all_battle_sa(self):
        return self.engine.query(u_CastleWarInfo).all()

    def get_all_guilds(self):
        return self.engine.query(u_guild).all()

    def get_all_members_guild(self):
        return self.engine.query(u_guildmember).all()

    def get_all_owner_castle(self):
        return self.engine.query(u_GuildZone).all()

    def get_all_henchs(self):
        monster = []
        search = self.engine.query(u_hench_0).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_1).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_2).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_3).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_4).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_5).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_6).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_7).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_8).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_hench_9).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        return monster

    def get_all_store_henchs(self):
        monster = []
        search = self.engine.query(u_store_hench_0).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_1).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_2).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_3).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_4).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_5).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_6).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_7).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_8).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        search = self.engine.query(u_store_hench_9).all()
        if search:
            monster.append(search)
        else:
            monster.append([])
        return monster

    def get_all_switchs(self):
        return self.engine.query(u_hero_quest).all()

    def get_all_items(self):
        return self.engine.query(u_item).all()

    def get_all_store_items(self):
        return self.engine.query(u_store_item).all()

    def get_all_skills(self):
        return self.engine.query(u_HeroSkill).all()

    def get_all_friends(self):
        return self.engine.query(u_messenger).all()

    def get_all_mix_log(self):
        return self.engine.query(u_MixLog).all()

    def get_all_mix_skill(self):
        return self.engine.query(u_MixSkill).all()

    def get_all_quest_log(self):
        return self.engine.query(u_MixSkill).all()

    def get_all_store(self):
        return self.engine.query(u_store).all()

# Guild
    def get_map_battle_sa(self, map_id_or_name):
        if not isinstance(map_id_or_name, bool) and isinstance(map_id_or_name, int) or isinstance(map_id_or_name, str):
            map_id = 0
            try:
                map_id = int(map_id_or_name)
            except ValueError:
                if map_id_or_name.lower() == "magirita":
                    map_id = 101
                elif map_id_or_name.lower() == "mekrita":
                    map_id = 102
            sa = self.engine.query(u_CastleWarInfo).filter_by(
                zone_idx=map_id).all()
            if sa:
                return sa
            else:
                raise Warning('Map not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_guild(self, guild_id_or_name):
        if not isinstance(guild_id_or_name, bool) and isinstance(guild_id_or_name, int) or isinstance(guild_id_or_name, str):
            try:
                guild_id_or_name = int(guild_id_or_name)
                guild = self.engine.query(u_guild).filter_by(
                    GuildIdx=guild_id_or_name).first()
            except ValueError:
                guild = self.engine.query(u_guild).filter_by(
                    Name=guild_id_or_name).all()
            if guild:
                return guild
            else:
                raise Warning('Guild not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_guild_members(self, guild_id_or_name):
        if not isinstance(guild_id_or_name, bool) and isinstance(guild_id_or_name, int) or isinstance(guild_id_or_name, str):
            guild = self.get_guild(guild_id_or_name)
            members = self.engine.query(u_guildmember).filter_by(
                GuildIdx=guild.GuildIdx).all()

            if members:
                return members
            else:
                raise Warning('Members not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_owner_castle(self, map_id_or_name):
        if not isinstance(map_id_or_name, bool) and isinstance(map_id_or_name, int) or isinstance(map_id_or_name, str):
            map_id = 0
            try:
                map_id = int(map_id_or_name)
            except ValueError:
                if map_id_or_name.lower() == "magirita":
                    map_id = 101
                elif map_id_or_name.lower() == "mekrita":
                    map_id = 102
            sa = self.engine.query(u_GuildZone).filter_by(
                zone_idx=map_id).first()
            if sa:
                return sa
            else:
                raise Warning('Map not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

# Switch Quest
    def get_switchs_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            switch = self.engine.query(u_hero_quest).filter(
                u_hero_quest.id_idx == hero_id, u_hero_quest.hero_order == hero_order).all()
            if switch:
                return switch
            else:
                raise Warning('Switchs not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_switchs_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        switch = self.engine.query(u_hero_quest).filter(
            u_hero_quest.id_idx == hero.id_idx, u_hero_quest.hero_order == hero.hero_order).all()
        if switch:
            return switch
        else:
            raise Warning('Switchs not found')

    def get_switch_by_id(self, hero_id, hero_order, switch_number):
        if check_number(hero_id) and check_number(hero_order) and check_number(switch_number):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            switch_number = int(switch_number)
            switch = self.engine.query(u_hero_quest).filter(
                u_hero_quest.id_idx == hero_id, u_hero_quest.hero_order == hero_order, u_hero_quest.switch_number == switch_number).first()
            if switch:
                return switch
            else:
                raise Warning('Switch not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_switch_by_name(self, hero_name, switch_number):
        if check_number(switch_number):
            switch_number = int(switch_number)
            hero = self.get_hero_by_name(hero_name)
            switch = self.engine.query(u_hero_quest).filter(
                u_hero_quest.id_idx == hero.id_idx, u_hero_quest.hero_order == hero.hero_order, u_hero_quest.switch_number == switch_number).first()
            if switch:
                return switch
            else:
                raise Warning('Switch not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_switch(self, switch_number):
        if check_number(switch_number):
            switch_number = int(switch_number)
            switch = self.engine.query(u_hero_quest).filter_by(
                switch_number=switch_number).all()
            if switch:
                return switch
            else:
                raise Warning('Switch not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

# Skills
    def get_skills_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            skill = self.engine.query(u_HeroSkill).filter(
                u_HeroSkill.heroIndex == hero_id, u_HeroSkill.heroSocketNum == hero_order).all()
            if skill:
                return skill
            else:
                raise Warning('Skills not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_skills_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        skill = self.engine.query(u_HeroSkill).filter(
            u_HeroSkill.heroIndex == hero.id_idx, u_HeroSkill.heroSocketNum == hero.hero_order).all()
        if skill:
            return skill
        else:
            raise Warning('Skills not found')

    def get_skill_by_id(self, hero_id, hero_order, skill_index):
        if check_number(hero_id) and check_number(hero_order) and check_number(skill_index):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            skill_index = int(skill_index)
            skill = self.engine.query(u_HeroSkill).filter(
                u_HeroSkill.heroIndex == hero_id, u_HeroSkill.heroSocketNum == hero_order, u_HeroSkill.skillIndex == skill_index).first()
            if skill:
                return skill
            else:
                raise Warning('Skill not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_skill_by_name(self, hero_name, skill_index):
        if check_number(skill_index):
            skill_index = int(skill_index)
            hero = self.get_hero_by_name(hero_name)
            skill = self.engine.query(u_HeroSkill).filter(
                u_HeroSkill.heroIndex == hero.id_idx, u_HeroSkill.heroSocketNum == hero.hero_order, u_HeroSkill.skillIndex == skill_index).first()
            if skill:
                return skill
            else:
                raise Warning('Skill not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_skill(self, skill_index):
        if check_number(skill_index):
            skill_index = int(skill_index)
            skill = self.engine.query(u_HeroSkill).filter_by(
                skillIndex=skill_index).all()
            if skill:
                return skill
            else:
                raise Warning('Skill not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

# Friends
    def get_friends_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            friends = self.engine.query(u_messenger).filter(
                u_messenger.HeroIdx == hero_id, u_messenger.HeroOrder == hero_order).all()
            if friends:
                return friends
            else:
                raise Warning('Friends not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_friends_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        friends = self.engine.query(u_messenger).filter(
            u_messenger.HeroIdx == hero.id_idx, u_messenger.HeroOrder == hero.hero_order).all()
        if friends:
            return friends
        else:
            raise Warning('Friends not found')

# MixLog
    def get_mix_log_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            mix = self.engine.query(u_MixLog).filter(
                u_MixLog.HeroIdx == hero_id, u_MixLog.HeroOrder == hero_order).all()
            if mix:
                return mix
            else:
                raise Warning('MixLog not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_mix_log_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        mix = self.engine.query(u_MixLog).filter(
            u_MixLog.HeroIdx == hero.id_idx, u_MixLog.HeroOrder == hero.hero_order).all()
        if mix:
            return mix
        else:
            raise Warning('MixLog not found')

    def get_mix_log_by_hench_id(self, hero_id, hero_order, hench_id):
        if check_number(hero_id) and check_number(hero_order) and check_number(hench_id):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            hench_id = int(hench_id)
            mix = self.engine.query(u_MixLog).filter(
                u_MixLog.HeroIdx == hero_id, u_MixLog.HeroOrder == hero_order, u_MixLog.type == hench_id).first()
            if mix:
                return mix
            else:
                raise Warning('MixLog not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_mix_log_by_hench_name(self, hero_name, hench_id):
        if check_number(hench_id):
            hench_id = int(hench_id)
            hero = self.get_hero_by_name(hero_name)
            mix = self.engine.query(u_MixLog).filter(
                u_MixLog.HeroIdx == hero.id_idx, u_MixLog.HeroOrder == hero.hero_order, u_MixLog.type == hench_id).first()
            if mix:
                return mix
            else:
                raise Warning('MixLog not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_mix_log_hench(self, hench_id):
        if check_number(hench_id):
            hench_id = int(hench_id)
            mix = self.engine.query(u_MixLog).filter_by(
                type=hench_id).all()
            if mix:
                return mix
            else:
                raise Warning('MixLog not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

# MixSkill
    def get_mix_skill_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            mix_skill = self.engine.query(u_MixSkill).filter(
                u_MixSkill.HeroIdx == hero_id, u_MixSkill.HeroOrder == hero_order).first()
            if mix_skill:
                return mix_skill
            else:
                raise Warning('MixSkill not found')
        else:
            raise Warning(
                'Invalid search, value must be number ')

    def get_mix_skill_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        mix_skill = self.engine.query(u_MixSkill).filter(
            u_MixSkill.HeroIdx == hero.id_idx, u_MixSkill.HeroOrder == hero.hero_order).first()
        if mix_skill:
            return mix_skill
        else:
            raise Warning('MixSkill not found')


# QuestLog


    def get_quest_log_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            quest = self.engine.query(u_QuestLog).filter(
                u_QuestLog.id_idx == hero_id, u_QuestLog.hero_order == hero_order).all()
            if quest:
                return quest
            else:
                raise Warning('Quests not found')
        else:
            raise Warning(
                'Invalid search, value must be number ')

    def get_quest_log_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        mix = self.engine.query(u_QuestLog).filter(
            u_QuestLog.id_idx == hero.id_idx, u_QuestLog.hero_order == hero.hero_order).all()
        if mix:
            return mix
        else:
            raise Warning('Quests not found')

    def get_quest_log_by_id(self, hero_id, hero_order, quest_id):
        if check_number(hero_id) and check_number(hero_order) and check_number(quest_id):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            quest_id = int(quest_id)
            quest = self.engine.query(u_QuestLog).filter(
                u_QuestLog.id_idx == hero_id, u_QuestLog.hero_order == hero_order, u_QuestLog.quest_index == quest_id).first()
            if quest:
                return quest
            else:
                raise Warning('Quest not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_quest_log_by_name(self, hero_name, quest_id):
        if check_number(quest_id):
            quest_id = int(quest_id)
            hero = self.get_hero_by_name(hero_name)
            quest = self.engine.query(u_QuestLog).filter(
                u_QuestLog.id_idx == hero.id_idx, u_QuestLog.hero_order == hero.hero_order, u_QuestLog.quest_index == quest_id).first()
            if quest:
                return quest
            else:
                raise Warning('Quest not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_quest_log(self, quest_id):
        if check_number(quest_id):
            quest_id = int(quest_id)
            quest = self.engine.query(u_QuestLog).filter_by(
                quest_index=quest_id).all()
            if quest:
                return quest
            else:
                raise Warning('Quests not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

# Store
    def get_store_by_id(self, hero_id):
        if check_number(hero_id):
            hero_id = int(hero_id)
            store = self.engine.query(u_store).filter(
                u_store.id_idx == hero_id).first()
            if store:
                return store
            else:
                raise Warning('Store not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_store_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        store = self.engine.query(u_store).filter(
            u_store.id_idx == hero.id_idx).first()
        if store:
            return store
        else:
            raise Warning('Store not found')

###

    def get_item_by_id(self, item_id):
        if check_number(item_id):
            item_id = int(item_id)
            item = self.engine.query(
                u_item).filter_by(item_idx=item_id).all()
            if item:
                return item
            else:
                raise Warning('Item not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_store_item_by_id(self, item_id):
        if check_number(item_id):
            item_id = int(item_id)
            item = self.engine.query(
                u_store_item).filter_by(item_idx=item_id).all()
            if item:
                return item
            else:
                raise Warning('Item not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_hench_by_id(self, hench_id):
        if check_number(hench_id):
            hench = []
            hench_id = int(hench_id)
            search = self.get_all_henchs()
            for h1 in search:
                for h2 in h1:
                    if h2.monster_type == hench_id:
                        hench.append(h2)
            if len(hench) > 0:
                return hench
            else:
                raise Warning('Hench not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_store_hench_by_id(self, hench_id):
        if check_number(hench_id):
            hench = []
            hench_id = int(hench_id)
            search = self.get_all_store_henchs()
            for h1 in search:
                for h2 in h1:
                    if h2.monster_type == hench_id:
                        hench.append(h2)
            if len(hench) > 0:
                return hench
            else:
                raise Warning('Hench not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

###
    def get_items_for_hero_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            items = self.engine.query(
                u_item).filter(u_item.id_idx == hero_id, u_item.hero_order == hero_order).all()
            if items:
                return items
            else:
                raise Warning('Items not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_items_for_hero_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        items = self.engine.query(
            u_item).filter(u_item.id_idx == hero.id_idx, u_item.hero_order == hero.hero_order).all()
        if items:
            return items
        else:
            raise Warning('Items not found')

    def get_store_items_for_player(self, player_id):
        if check_number(player_id):
            player_id = int(player_id)
            items = self.engine.query(
                u_store_item).filter_by(id_idx=player_id).all()
            if items:
                return items
            else:
                raise Warning('Items not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_henchs_for_hero_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hench = None
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            final_id = int(hero_id) % 10
            if final_id == 0:
                hench = self.engine.query(
                    u_hench_0).filter(u_hench_0.id_idx == hero_id, u_hench_0.hero_order == hero_order).all()
            elif final_id == 1:
                hench = self.engine.query(
                    u_hench_1).filter(u_hench_1.id_idx == hero_id, u_hench_1.hero_order == hero_order).all()
            elif final_id == 2:
                hench = self.engine.query(
                    u_hench_2).filter(u_hench_2.id_idx == hero_id, u_hench_2.hero_order == hero_order).all()
            elif final_id == 3:
                hench = self.engine.query(
                    u_hench_3).filter(u_hench_3.id_idx == hero_id, u_hench_3.hero_order == hero_order).all()
            elif final_id == 4:
                hench = self.engine.query(
                    u_hench_4).filter(u_hench_4.id_idx == hero_id, u_hench_4.hero_order == hero_order).all()
            elif final_id == 5:
                hench = self.engine.query(
                    u_hench_5).filter(u_hench_5.id_idx == hero_id, u_hench_5.hero_order == hero_order).all()
            elif final_id == 6:
                hench = self.engine.query(
                    u_hench_6).filter(u_hench_6.id_idx == hero_id, u_hench_6.hero_order == hero_order).all()
            elif final_id == 7:
                hench = self.engine.query(
                    u_hench_7).filter(u_hench_7.id_idx == hero_id, u_hench_7.hero_order == hero_order).all()
            elif final_id == 8:
                hench = self.engine.query(
                    u_hench_8).filter(u_hench_8.id_idx == hero_id, u_hench_8.hero_order == hero_order).all()
            elif final_id == 9:
                hench = self.engine.query(
                    u_hench_9).filter(u_hench_9.id_idx == hero_id, u_hench_9.hero_order == hero_order).all()

            if hench:
                return hench
            else:
                raise Warning('Henchs not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_henchs_for_hero_by_name(self, hero_name):
        hench = None
        hero = self.get_hero_by_name(hero_name)
        final_id = int(hero.id_idx) % 10
        if final_id == 0:
            hench = self.engine.query(
                u_hench_0).filter(u_hench_0.id_idx == hero.id_idx, u_hench_0.hero_order == hero.hero_order).all()
        elif final_id == 1:
            hench = self.engine.query(
                u_hench_1).filter(u_hench_1.id_idx == hero.id_idx, u_hench_1.hero_order == hero.hero_order).all()
        elif final_id == 2:
            hench = self.engine.query(
                u_hench_2).filter(u_hench_2.id_idx == hero.id_idx, u_hench_2.hero_order == hero.hero_order).all()
        elif final_id == 3:
            hench = self.engine.query(
                u_hench_3).filter(u_hench_3.id_idx == hero.id_idx, u_hench_3.hero_order == hero.hero_order).all()
        elif final_id == 4:
            hench = self.engine.query(
                u_hench_4).filter(u_hench_4.id_idx == hero.id_idx, u_hench_4.hero_order == hero.hero_order).all()
        elif final_id == 5:
            hench = self.engine.query(
                u_hench_5).filter(u_hench_5.id_idx == hero.id_idx, u_hench_5.hero_order == hero.hero_order).all()
        elif final_id == 6:
            hench = self.engine.query(
                u_hench_6).filter(u_hench_6.id_idx == hero.id_idx, u_hench_6.hero_order == hero.hero_order).all()
        elif final_id == 7:
            hench = self.engine.query(
                u_hench_7).filter(u_hench_7.id_idx == hero.id_idx, u_hench_7.hero_order == hero.hero_order).all()
        elif final_id == 8:
            hench = self.engine.query(
                u_hench_8).filter(u_hench_8.id_idx == hero.id_idx, u_hench_8.hero_order == hero.hero_order).all()
        elif final_id == 9:
            hench = self.engine.query(
                u_hench_9).filter(u_hench_9.id_idx == hero.id_idx, u_hench_9.hero_order == hero.hero_order).all()
        if hench:
            return hench
        else:
            raise Warning('Henchs not found')

    def get_store_henchs_for_player(self, player_id):
        if check_number(player_id):
            hench = None
            player_id = int(player_id)
            final_id = player_id % 10
            if final_id == 0:
                hench = self.engine.query(
                    u_store_hench_0).filter(u_store_hench_0.id_idx == player_id).all()
            elif final_id == 1:
                hench = self.engine.query(
                    u_store_hench_1).filter(u_store_hench_1.id_idx == player_id).all()
            elif final_id == 2:
                hench = self.engine.query(
                    u_store_hench_2).filter(u_store_hench_2.id_idx == player_id).all()
            elif final_id == 3:
                hench = self.engine.query(
                    u_store_hench_3).filter(u_store_hench_3.id_idx == player_id).all()
            elif final_id == 4:
                hench = self.engine.query(
                    u_store_hench_4).filter(u_store_hench_4.id_idx == player_id).all()
            elif final_id == 5:
                hench = self.engine.query(
                    u_store_hench_5).filter(u_store_hench_5.id_idx == player_id).all()
            elif final_id == 6:
                hench = self.engine.query(
                    u_store_hench_6).filter(u_store_hench_6.id_idx == player_id).all()
            elif final_id == 7:
                hench = self.engine.query(
                    u_store_hench_7).filter(u_store_hench_7.id_idx == player_id).all()
            elif final_id == 8:
                hench = self.engine.query(
                    u_store_hench_8).filter(u_store_hench_8.id_idx == player_id).all()
            elif final_id == 9:
                hench = self.engine.query(
                    u_store_hench_9).filter(u_store_hench_9.id_idx == player_id).all()
            if hench:
                return hench
            else:
                raise Warning('Henchs not found in store')
        else:
            raise Warning(
                'Invalid search, value must be number')

###
    def get_item_by_id_for_hero(self, hero_name, item_id):
        if check_number(item_id):
            item_id = int(item_id)
            hero = self.get_hero_by_name(hero_name)
            item = self.engine.query(
                u_item).filter(u_item.id_idx == hero.id_idx, u_item.hero_order == hero.hero_order, u_item.item_idx == item_id).all()
            if item:
                return item
            else:
                raise Warning('Item not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_store_item_by_id_for_player(self, player_id, item_id):
        if check_number(player_id) and check_number(item_id):
            player_id = int(player_id)
            item_id = int(item_id)
            item = self.engine.query(
                u_store_item).filter(u_store_item.id_idx == player_id, u_store_item.item_idx == item_id).all()
            if item:
                return item
            else:
                raise Warning('Item not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_hench_by_id_for_hero(self, hero_name, hench_id):
        if check_number(hench_id):
            hench_id = int(hench_id)
            hero = self.get_hero_by_name(hero_name)
            final_id = int(hero.id_idx) % 10
            if final_id == 0:
                hench = self.engine.query(
                    u_hench_0).filter(u_hench_0.id_idx == hero.id_idx, u_hench_0.hero_order == hero.hero_order, u_hench_0.monster_type == hench_id).all()
            elif final_id == 1:
                hench = self.engine.query(
                    u_hench_1).filter(u_hench_1.id_idx == hero.id_idx, u_hench_1.hero_order == hero.hero_order, u_hench_1.monster_type == hench_id).all()
            elif final_id == 2:
                hench = self.engine.query(
                    u_hench_2).filter(u_hench_2.id_idx == hero.id_idx, u_hench_2.hero_order == hero.hero_order, u_hench_2.monster_type == hench_id).all()
            elif final_id == 3:
                hench = self.engine.query(
                    u_hench_3).filter(u_hench_3.id_idx == hero.id_idx, u_hench_3.hero_order == hero.hero_order, u_hench_3.monster_type == hench_id).all()
            elif final_id == 4:
                hench = self.engine.query(
                    u_hench_4).filter(u_hench_4.id_idx == hero.id_idx, u_hench_4.hero_order == hero.hero_order, u_hench_4.monster_type == hench_id).all()
            elif final_id == 5:
                hench = self.engine.query(
                    u_hench_5).filter(u_hench_5.id_idx == hero.id_idx, u_hench_5.hero_order == hero.hero_order, u_hench_5.monster_type == hench_id).all()
            elif final_id == 6:
                hench = self.engine.query(
                    u_hench_6).filter(u_hench_6.id_idx == hero.id_idx, u_hench_6.hero_order == hero.hero_order, u_hench_6.monster_type == hench_id).all()
            elif final_id == 7:
                hench = self.engine.query(
                    u_hench_7).filter(u_hench_7.id_idx == hero.id_idx, u_hench_7.hero_order == hero.hero_order, u_hench_7.monster_type == hench_id).all()
            elif final_id == 8:
                hench = self.engine.query(
                    u_hench_8).filter(u_hench_8.id_idx == hero.id_idx, u_hench_8.hero_order == hero.hero_order, u_hench_8.monster_type == hench_id).all()
            elif final_id == 9:
                hench = self.engine.query(
                    u_hench_9).filter(u_hench_9.id_idx == hero.id_idx, u_hench_9.hero_order == hero.hero_order, u_hench_9.monster_type == hench_id).all()
            if hench:
                return hench
            else:
                raise Warning('Hench not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def get_store_hench_by_id_for_player(self, player_id, hench_id):
        if check_number(player_id) and check_number(hench_id):
            hench_id = int(hench_id)
            player_id = int(player_id)
            final_id = int(player_id) % 10
            if final_id == 0:
                hench = self.engine.query(
                    u_store_hench_0).filter(u_store_hench_0.id_idx == player_id, u_store_hench_0.monster_type == hench_id).all()
            elif final_id == 1:
                hench = self.engine.query(
                    u_store_hench_1).filter(u_store_hench_1.id_idx == player_id, u_store_hench_1.monster_type == hench_id).all()
            elif final_id == 2:
                hench = self.engine.query(
                    u_store_hench_2).filter(u_store_hench_2.id_idx == player_id, u_store_hench_2.monster_type == hench_id).all()
            elif final_id == 3:
                hench = self.engine.query(
                    u_store_hench_3).filter(u_store_hench_3.id_idx == player_id, u_store_hench_3.monster_type == hench_id).all()
            elif final_id == 4:
                hench = self.engine.query(
                    u_store_hench_4).filter(u_store_hench_4.id_idx == player_id, u_store_hench_4.monster_type == hench_id).all()
            elif final_id == 5:
                hench = self.engine.query(
                    u_store_hench_5).filter(u_store_hench_5.id_idx == player_id, u_store_hench_5.monster_type == hench_id).all()
            elif final_id == 6:
                hench = self.engine.query(
                    u_store_hench_6).filter(u_store_hench_6.id_idx == player_id, u_store_hench_6.monster_type == hench_id).all()
            elif final_id == 7:
                hench = self.engine.query(
                    u_store_hench_7).filter(u_store_hench_7.id_idx == player_id, u_store_hench_7.monster_type == hench_id).all()
            elif final_id == 8:
                hench = self.engine.query(
                    u_store_hench_8).filter(u_store_hench_8.id_idx == player_id, u_store_hench_8.monster_type == hench_id).all()
            elif final_id == 9:
                hench = self.engine.query(
                    u_store_hench_9).filter(u_store_hench_9.id_idx == player_id, u_store_hench_9.monster_type == hench_id).all()
            if hench:
                return hench
            else:
                raise Warning('Hench not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

###
    def get_hench_by_name_for_hero(self, hero_name, hench_name):
        if check_string(hench_name):
            hero = self.get_hero_by_name(hero_name)
            final_id = int(hero.id_idx) % 10
            if final_id == 0:
                hench = self.engine.query(
                    u_hench_0).filter(u_hench_0.id_idx == hero.id_idx, u_hench_0.hero_order == hero.hero_order, u_hench_0.name == hench_name).all()
            elif final_id == 1:
                hench = self.engine.query(
                    u_hench_1).filter(u_hench_1.id_idx == hero.id_idx, u_hench_1.hero_order == hero.hero_order, u_hench_1.name == hench_name).all()
            elif final_id == 2:
                hench = self.engine.query(
                    u_hench_2).filter(u_hench_2.id_idx == hero.id_idx, u_hench_2.hero_order == hero.hero_order, u_hench_2.name == hench_name).all()
            elif final_id == 3:
                hench = self.engine.query(
                    u_hench_3).filter(u_hench_3.id_idx == hero.id_idx, u_hench_3.hero_order == hero.hero_order, u_hench_3.name == hench_name).all()
            elif final_id == 4:
                hench = self.engine.query(
                    u_hench_4).filter(u_hench_4.id_idx == hero.id_idx, u_hench_4.hero_order == hero.hero_order, u_hench_4.name == hench_name).all()
            elif final_id == 5:
                hench = self.engine.query(
                    u_hench_5).filter(u_hench_5.id_idx == hero.id_idx, u_hench_5.hero_order == hero.hero_order, u_hench_5.name == hench_name).all()
            elif final_id == 6:
                hench = self.engine.query(
                    u_hench_6).filter(u_hench_6.id_idx == hero.id_idx, u_hench_6.hero_order == hero.hero_order, u_hench_6.name == hench_name).all()
            elif final_id == 7:
                hench = self.engine.query(
                    u_hench_7).filter(u_hench_7.id_idx == hero.id_idx, u_hench_7.hero_order == hero.hero_order, u_hench_7.name == hench_name).all()
            elif final_id == 8:
                hench = self.engine.query(
                    u_hench_8).filter(u_hench_8.id_idx == hero.id_idx, u_hench_8.hero_order == hero.hero_order, u_hench_8.name == hench_name).all()
            elif final_id == 9:
                hench = self.engine.query(
                    u_hench_9).filter(u_hench_9.id_idx == hero.id_idx, u_hench_9.hero_order == hero.hero_order, u_hench_9.name == hench_name).all()
            if hench:
                return hench
            else:
                raise Warning('Hench not found')
        else:
            raise Warning(
                'Invalid search, value must be string')

    def get_store_hench_by_name_for_player(self, player_id, hench_name):
        if check_number(player_id) and check_string(hench_name):
            player_id = int(player_id)
            final_id = player_id % 10
            if final_id == 0:
                hench = self.engine.query(
                    u_store_hench_0).filter(u_store_hench_0.id_idx == player_id, u_store_hench_0.name == hench_name).all()
            elif final_id == 1:
                hench = self.engine.query(
                    u_store_hench_1).filter(u_store_hench_1.id_idx == player_id, u_store_hench_1.name == hench_name).all()
            elif final_id == 2:
                hench = self.engine.query(
                    u_store_hench_2).filter(u_store_hench_2.id_idx == player_id, u_store_hench_2.name == hench_name).all()
            elif final_id == 3:
                hench = self.engine.query(
                    u_store_hench_3).filter(u_store_hench_3.id_idx == player_id, u_store_hench_3.name == hench_name).all()
            elif final_id == 4:
                hench = self.engine.query(
                    u_store_hench_4).filter(u_store_hench_4.id_idx == player_id, u_store_hench_4.name == hench_name).all()
            elif final_id == 5:
                hench = self.engine.query(
                    u_store_hench_5).filter(u_store_hench_5.id_idx == player_id, u_store_hench_5.name == hench_name).all()
            elif final_id == 6:
                hench = self.engine.query(
                    u_store_hench_6).filter(u_store_hench_6.id_idx == player_id, u_store_hench_6.name == hench_name).all()
            elif final_id == 7:
                hench = self.engine.query(
                    u_store_hench_7).filter(u_store_hench_7.id_idx == player_id, u_store_hench_7.name == hench_name).all()
            elif final_id == 8:
                hench = self.engine.query(
                    u_store_hench_8).filter(u_store_hench_8.id_idx == player_id, u_store_hench_8.name == hench_name).all()
            elif final_id == 9:
                hench = self.engine.query(
                    u_store_hench_9).filter(u_store_hench_9.id_idx == player_id, u_store_hench_9.name == hench_name).all()
            if hench:
                return hench
            else:
                raise Warning('Hench not found')
        else:
            raise Warning(
                'Invalid search, value must be number')

# Ranking
    def get_ranking_hero_level(self, limit):
        heros = self.engine.query(u_hero).filter_by(
            classe=0).order_by(u_hero.baselevel.desc()).limit(limit)  # desc
        return heros

    def get_ranking_hero_exp(self, limit):
        heros = self.engine.query(u_hero).filter_by(
            classe=0).order_by(u_hero.exp.desc()).limit(limit)  # desc
        return heros

    def get_ranking_hero_gp(self, limit):
        heros = self.engine.query(u_hero).filter_by(
            classe=0).order_by(u_hero.gold.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_1(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill1.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_2(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill2.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_3(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill3.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_4(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill4.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_5(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill5.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_6(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill6.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_7(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill7.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_8(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill8.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_9(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill9.desc()).limit(limit)  # desc
        return heros

    def get_ranking_mix_master_10(self, limit):
        heros = self.engine.query(u_MixSkill).order_by(
            u_MixSkill.MixSkill10.desc()).limit(limit)  # desc
        return heros

    def set_hero_class_by_id(self, hero_id, hero_order, new_class_id):
        if check_number(hero_id) and check_number(hero_order) and check_number(new_class_id):
            new_class_id = int(new_class_id)
            if new_class_id < 0 or new_class_id > 3:
                raise Warning(
                    f'Invalid new class, use 0 for Ditt, 1 for Jin, 2 for Penril or 3 for Phoy')
            hero = self.get_hero_by_id(hero_id, hero_order)
            if hero.login == 0:
                if hero.hero_type == new_class_id:
                    raise Warning(
                        f'New class cannot be the same as the current one')
                hero.hero_type = new_class_id
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_hero_class_by_name(self, hero_name, new_class_id):
        if check_number(new_class_id):
            new_class_id = int(new_class_id)
            if new_class_id < 0 or new_class_id > 3:
                raise Warning(
                    f'Invalid new class, use 0 for Ditt, 1 for Jin, 2 for Penril or 3 for Phoy')
            hero = self.get_hero_by_name(hero_name)
            if hero.login == 0:
                if hero.hero_type == new_class_id:
                    raise Warning(
                        f'New class cannot be the same as the current one')
                hero.hero_type = new_class_id
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_hero_name_by_id(self, hero_id, hero_order, new_name):
        hero = None
        try:
            self.get_hero_by_name(new_name)
            check = False
        except Warning:
            check = True
        if check:
            hero = self.get_hero_by_id(hero_id, hero_order)
        else:
            raise Warning(
                f'New Name already exists')
        if hero.login == 0:
            hero.name = new_name
            self.engine.commit()
            return True
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def set_hero_name_by_name(self, hero_name, new_name):
        hero = None
        try:
            self.get_hero_by_name(new_name)
            check = False
        except Warning:
            check = True
        if check:
            print("aqui")
            hero = self.get_hero_by_name(hero_name)
        else:
            raise Warning(
                f'New Name already exists')
        if hero.login == 0:
            hero.name = new_name
            self.engine.commit()
            return True
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def set_hero_gp_by_id(self, hero_id, hero_order, new_gp):
        if check_number(new_gp):
            new_gp = int(new_gp)
            if new_gp > 4200000000:
                raise Warning(
                    'New Value must be less than 4.2kkk')
            hero = self.get_hero_by_id(hero_id, hero_order)
            if hero.login == 0:
                hero.gold = new_gp
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_hero_gp_by_name(self, hero_name, new_gp):
        if check_number(new_gp):
            new_gp = int(new_gp)
            if new_gp > 4200000000:
                raise Warning(
                    'New Value must be less than 4.2kkk')
            hero = self.get_hero_by_name(hero_name)
            if hero.login == 0:
                hero.gold = new_gp
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_hero_status_by_id(self, hero_id, hero_order, str_dex_aim_luck, new_status):
        if check_string(str_dex_aim_luck):
            if not check_status_str(str_dex_aim_luck):
                raise Warning(
                    'status invalid, only valid string: str, dex, aim or luck')
        else:
            raise Warning(
                'Invalid search, value must be string')
        if check_number(new_status):
            new_status = int(new_status)
            if new_status > 65000:
                raise Warning(
                    'New Value must be less than 65k')
            hero = self.get_hero_by_id(hero_id, hero_order)
            if hero.login == 0:
                if str_dex_aim_luck.lower() == "str":
                    hero.str = new_status
                elif str_dex_aim_luck.lower() == "dex":
                    hero.dex = new_status
                elif str_dex_aim_luck.lower() == "aim":
                    hero.aim = new_status
                elif str_dex_aim_luck.lower() == "luck":
                    hero.luck = new_status
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_hero_status_by_name(self, hero_name, str_dex_aim_luck, new_status):
        if check_string(str_dex_aim_luck):
            if not check_status_str(str_dex_aim_luck):
                raise Warning(
                    'status invalid, only valid string: str, dex, aim or luck')
        else:
            raise Warning(
                'Invalid search, value must be string')
        if check_number(new_status):
            new_status = int(new_status)
            if new_status > 65000:
                raise Warning(
                    'New Value must be less than 65k')
            hero = self.get_hero_by_name(hero_name)
            if hero.login == 0:
                if str_dex_aim_luck.lower() == "str":
                    hero.str = new_status
                elif str_dex_aim_luck.lower() == "dex":
                    hero.dex = new_status
                elif str_dex_aim_luck.lower() == "aim":
                    hero.aim = new_status
                elif str_dex_aim_luck.lower() == "luck":
                    hero.luck = new_status
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_hero_free_points_by_id(self, hero_id, hero_order, new_value):
        if check_number(new_value):
            new_value = int(new_value)
            hero = self.get_hero_by_id(hero_id, hero_order)
            if hero.login == 0:
                hero.abil_freepoint = new_value
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_hero_free_points_by_name(self, hero_name, new_value):
        if check_number(new_value):
            new_value = int(new_value)
            hero = self.get_hero_by_name(hero_name)
            if hero.login == 0:
                hero.abil_freepoint = new_value
                self.engine.commit()
                return True
            else:
                raise Warning(
                    f'Change in hero is only possible when not logged in')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_switch_count_by_id(self, hero_id, hero_order, switch_number, new_count):
        if check_number(new_count):
            new_count = int(new_count)
            if new_count > 65535 or new_count < 1:
                raise Warning(
                    f'Count must be between 1 and 65535')
            switch = self.get_switch_by_id(
                hero_id, hero_order, switch_number)
            if switch:
                if not self.get_hero_login_by_id(hero_id, hero_order):
                    switch.success_count = new_count
                    self.engine.commit()
                    return True
                else:
                    raise Warning(
                        f'Change in hero is only possible when not logged in')
            else:
                raise
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_switch_count_by_name(self, hero_name, switch_number, new_count):
        if check_number(new_count):
            switch_number = int(switch_number)
            new_count = int(new_count)
            if new_count > 65535 or new_count < 1:
                raise Warning(
                    f'Count must be between 1 and 65535')
            switch = self.get_switch_by_name(hero_name, switch_number)
            if switch:
                if not self.get_hero_login_by_name(hero_name):
                    switch.success_count = new_count
                    self.engine.commit()
                    return True
                else:
                    raise Warning(
                        f'Change in hero is only possible when not logged in')
            else:
                raise
        else:
            raise Warning(
                'Invalid search, value must be number')

    def set_switch_time_by_id(self, hero_id, hero_order, switch_number, new_time):
        format_data = format_datetime(new_time)
        if format_data == "Invalid string format" or format_data == "Invalid input type":
            raise Warning(
                format_data)
        else:
            new_time = format_data
            switch = self.get_switch_by_id(
                hero_id, hero_order, switch_number)
            if switch:
                if not self.get_hero_login_by_id(hero_id, hero_order):
                    switch.success_time = new_time
                    self.engine.commit()
                    return True
                else:
                    raise Warning(
                        f'Change in hero is only possible when not logged in')
            else:
                raise

    def set_switch_time_by_name(self, hero_name, switch_number, new_time):
        format_data = format_datetime(new_time)
        if format_data == "Invalid string format" or format_data == "Invalid input type":
            raise Warning(
                format_data)
        else:
            new_time = format_data
            switch = self.get_switch_by_name(hero_name, switch_number)
            if switch:
                if not self.get_hero_login_by_name(hero_name):
                    switch.success_time = new_time
                    self.engine.commit()
                    return True
                else:
                    raise Warning(
                        f'Change in hero is only possible when not logged in')
            else:
                raise

    def add_switch_by_id(self, hero_id, hero_order, switch_number, success_count, success_time):
        if check_number(success_count):
            format_data = format_datetime(success_time)
            if format_data == "Invalid string format" or format_data == "Invalid input type":
                raise Warning(
                    format_data)
            else:
                success_count = int(success_count)
                if success_count > 65535 or success_count < 1:
                    raise Warning(
                        f'Count must be between 1 and 65535')
                try:
                    self.get_switch_by_id(
                        hero_id, hero_order, switch_number)
                    check = False
                except Warning:
                    check = True
                if check:
                    if not self.get_hero_login_by_id(hero_id, hero_order):
                        switch = u_hero_quest()
                        switch.id_idx = hero_id
                        switch.hero_order = hero_order
                        switch.switch_number = switch_number
                        switch.success_count = success_count
                        switch.success_time = format_data
                        self.engine.add(switch)
                        self.engine.commit()
                        return True
                    else:
                        raise Warning(
                            f'Change in hero is only possible when not logged in')
                else:
                    raise Warning(
                        f'Switch Already exists')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def add_switch_by_name(self, hero_name, switch_number, success_count, success_time):
        if check_number(success_count):
            format_data = format_datetime(success_time)
            if format_data == "Invalid string format" or format_data == "Invalid input type":
                raise Warning(
                    format_data)
            else:
                success_count = int(success_count)
                if success_count > 65535 or success_count < 1:
                    raise Warning(
                        f'Count must be between 1 and 65535')
                try:
                    self.get_switch_by_name(
                        hero_name, switch_number)
                    check = False
                except Warning:
                    check = True
                if check:
                    hero = self.get_hero_login_by_name(hero_name)
                    if hero.login == 0:
                        switch = u_hero_quest()
                        switch.id_idx = hero.id_idx
                        switch.hero_order = hero.as_integer_ratiohero_order
                        switch.switch_number = switch_number
                        switch.success_count = success_count
                        switch.success_time = format_data
                        self.engine.add(switch)
                        self.engine.commit()
                        return True
                    else:
                        raise Warning(
                            f'Change in hero is only possible when not logged in')
                else:
                    raise Warning(
                        f'Switch Already exists')
        else:
            raise Warning(
                'Invalid search, value must be number')

    def clean_items_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_item).filter(
                u_item.id_idx == hero_id, u_item.hero_order == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_items_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_item).filter(
                u_item.id_idx == hero.id_idx, u_item.hero_order == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_switch_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_hero_quest).filter(
                u_hero_quest.id_idx == hero_id, u_hero_quest.hero_order == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_switch_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_hero_quest).filter(
                u_hero_quest.id_idx == hero.id_idx, u_hero_quest.hero_order == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_guild_member_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_guildmember).filter(
                u_guildmember.HeroIdx == hero_id, u_guildmember.HeroOrder == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_guild_member_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_guildmember).filter(
                u_guildmember.HeroIdx == hero.id_idx, u_guildmember.HeroOrder == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_henchs_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            final_id = hero_id % 10
            if final_id == 0:
                self.engine.query(u_hench_0).filter(
                    u_hench_0.id_idx == hero_id, u_hench_0.hero_order == hero_order).delete()
            elif final_id == 1:
                self.engine.query(u_hench_1).filter(
                    u_hench_1.id_idx == hero_id, u_hench_1.hero_order == hero_order).delete()
            elif final_id == 2:
                self.engine.query(u_hench_2).filter(
                    u_hench_2.id_idx == hero_id, u_hench_2.hero_order == hero_order).delete()
            elif final_id == 3:
                self.engine.query(u_hench_3).filter(
                    u_hench_3.id_idx == hero_id, u_hench_3.hero_order == hero_order).delete()
            elif final_id == 4:
                self.engine.query(u_hench_4).filter(
                    u_hench_4.id_idx == hero_id, u_hench_4.hero_order == hero_order).delete()
            elif final_id == 5:
                self.engine.query(u_hench_5).filter(
                    u_hench_5.id_idx == hero_id, u_hench_5.hero_order == hero_order).delete()
            elif final_id == 6:
                self.engine.query(u_hench_6).filter(
                    u_hench_6.id_idx == hero_id, u_hench_6.hero_order == hero_order).delete()
            elif final_id == 7:
                self.engine.query(u_hench_7).filter(
                    u_hench_7.id_idx == hero_id, u_hench_7.hero_order == hero_order).delete()
            elif final_id == 8:
                self.engine.query(u_hench_8).filter(
                    u_hench_8.id_idx == hero_id, u_hench_8.hero_order == hero_order).delete()
            elif final_id == 9:
                self.engine.query(u_hench_9).filter(
                    u_hench_9.id_idx == hero_id, u_hench_9.hero_order == hero_order).delete()
            else:
                raise Warning(
                    f'Invalid hero id')
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_henchs_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            final_id = hero.id_idx % 10
            if final_id == 0:
                self.engine.query(u_hench_0).filter(
                    u_hench_0.id_idx == hero.id_idx, u_hench_0.hero_order == hero.hero_order).delete()
            elif final_id == 1:
                self.engine.query(u_hench_1).filter(
                    u_hench_1.id_idx == hero.id_idx, u_hench_1.hero_order == hero.hero_order).delete()
            elif final_id == 2:
                self.engine.query(u_hench_2).filter(
                    u_hench_2.id_idx == hero.id_idx, u_hench_2.hero_order == hero.hero_order).delete()
            elif final_id == 3:
                self.engine.query(u_hench_3).filter(
                    u_hench_3.id_idx == hero.id_idx, u_hench_3.hero_order == hero.hero_order).delete()
            elif final_id == 4:
                self.engine.query(u_hench_4).filter(
                    u_hench_4.id_idx == hero.id_idx, u_hench_4.hero_order == hero.hero_order).delete()
            elif final_id == 5:
                self.engine.query(u_hench_5).filter(
                    u_hench_5.id_idx == hero.id_idx, u_hench_5.hero_order == hero.hero_order).delete()
            elif final_id == 6:
                self.engine.query(u_hench_6).filter(
                    u_hench_6.id_idx == hero.id_idx, u_hench_6.hero_order == hero.hero_order).delete()
            elif final_id == 7:
                self.engine.query(u_hench_7).filter(
                    u_hench_7.id_idx == hero.id_idx, u_hench_7.hero_order == hero.hero_order).delete()
            elif final_id == 8:
                self.engine.query(u_hench_8).filter(
                    u_hench_8.id_idx == hero.id_idx, u_hench_8.hero_order == hero.hero_order).delete()
            elif final_id == 9:
                self.engine.query(u_hench_9).filter(
                    u_hench_9.id_idx == hero.id_idx, u_hench_9.hero_order == hero.hero_order).delete()
            else:
                raise Warning(
                    f'Invalid hero id')
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_skills_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_HeroSkill).filter(
                u_HeroSkill.heroIndex == hero_id, u_HeroSkill.heroSocketNum == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_skills_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_HeroSkill).filter(
                u_HeroSkill.heroIndex == hero.id_idx, u_HeroSkill.heroSocketNum == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_friends_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_messenger).filter(
                u_messenger.HeroIdx == hero_id, u_messenger.HeroOrder == hero_order).delete()
            self.engine.query(u_messenger).filter(
                u_messenger.TargetHeroIdx == hero_id, u_messenger.TargetHeroOrder == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_friends_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_messenger).filter(
                u_messenger.HeroIdx == hero.id_idx, u_messenger.HeroOrder == hero.hero_order).delete()
            self.engine.query(u_messenger).filter(
                u_messenger.TargetHeroIdx == hero.id_idx, u_messenger.TargetHeroOrder == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_mix_log_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_MixLog).filter(
                u_MixLog.HeroIdx == hero_id, u_MixLog.HeroOrder == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_mix_log_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_MixLog).filter(
                u_MixLog.HeroIdx == hero.id_idx, u_MixLog.HeroOrder == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_mix_points_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_MixSkill).filter(
                u_MixSkill.HeroIdx == hero_id, u_MixSkill.HeroOrder == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_mix_points_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_MixSkill).filter(
                u_MixSkill.HeroIdx == hero.id_idx, u_MixSkill.HeroOrder == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_quest_log_by_id(self, hero_id, hero_order):
        if not self.get_hero_login_by_id(hero_id, hero_order):
            self.engine.query(u_QuestLog).filter(
                u_QuestLog.id_idx == hero_id, u_QuestLog.hero_order == hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def clean_quest_log_by_name(self, hero_name):
        hero = self.get_hero_by_name(hero_name)
        if hero.login == 0:
            self.engine.query(u_QuestLog).filter(
                u_QuestLog.id_idx == hero.id_idx, u_QuestLog.hero_order == hero.hero_order).delete()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def del_hero_by_id(self, hero_id, hero_order):
        try:
            hero = self.get_hero_by_id(hero_id, hero_order)
        except:
            raise
        if hero.login == 0:
            self.clean_friends_by_id(hero_id, hero_order)
            self.clean_guild_member_by_id(hero_id, hero_order)
            self.clean_henchs_by_id(hero_id, hero_order)
            self.clean_items_by_id(hero_id, hero_order)
            self.clean_mix_log_by_id(hero_id, hero_order)
            self.clean_mix_points_by_id(hero_id, hero_order)
            self.clean_quest_log_by_id(hero_id, hero_order)
            self.clean_skills_by_id(hero_id, hero_order)
            self.clean_switch_by_id(hero_id, hero_order)
            self.engine.delete(hero)
            self.engine.commit()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')

    def del_hero_by_name(self, hero_name):
        try:
            hero = self.get_hero_by_name(hero_name)
        except:
            raise
        if hero.login == 0:
            self.clean_friends_by_name(hero_name)
            self.clean_guild_member_by_name(hero_name)
            self.clean_henchs_by_name(hero_name)
            self.clean_items_by_name(hero_name)
            self.clean_mix_log_by_name(hero_name)
            self.clean_mix_points_by_name(hero_name)
            self.clean_quest_log_by_name(hero_name)
            self.clean_skills_by_name(hero_name)
            self.clean_switch_by_name(hero_name)
            self.engine.delete(hero)
            self.engine.commit()
        else:
            raise Warning(
                f'Change in hero is only possible when not logged in')
