from .models import *
from ..functions import *


class LoginLogs():

    def __init__(self, engine):
        # Connect Member
        self.engine = engine

    def get_all_login_log(self):
        return self.engine.query(LoginLog).all()

    def get_log_login_by_ip(self, ipaddress):
        if check_string(ipaddress):
            logs = self.engine.query(LoginLog).filter_by(
                IP=ipaddress).all()
            if logs:
                return logs
            else:
                raise Warning('IP address not found')
        else:
            raise Warning(
                'Invalid search, value must be string')

    def get_log_login_by_name(self, hero_name):
        if check_string(hero_name):
            logs = self.engine.query(LoginLog).filter_by(
                HeroName=hero_name).all()
            if logs:
                return logs
            else:
                raise Warning('Hero not found in Log')
        else:
            raise Warning(
                'Invalid search, value must be string')

    def get_log_login_by_id(self, hero_id, hero_order):
        if check_number(hero_id) and check_number(hero_order):
            hero_id = int(hero_id)
            hero_order = int(hero_order)
            logs = self.engine.query(LoginLog).filter(
                LoginLog.HeroIdx == hero_id, LoginLog.HeroOrder == hero_order).all()
            if logs:
                return logs
            else:
                raise Warning('Hero not found in Log')
        else:
            raise Warning(
                'Invalid search, value must be number ')
