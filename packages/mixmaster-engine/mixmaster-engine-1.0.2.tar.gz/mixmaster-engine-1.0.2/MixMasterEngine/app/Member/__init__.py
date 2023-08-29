from .models import *
from datetime import datetime
from ..functions import *


class Members():

    def __init__(self, engine):
        # Connect Member
        self.engine = engine

    def get_all_players(self):
        return self.engine.query(Players).all()

    def get_player(self, id_or_name):
        if isinstance(id_or_name, int) or isinstance(id_or_name, str) and not isinstance(id_or_name, bool):
            try:
                id_or_name = int(id_or_name)
                player = self.engine.query(
                    Players).filter_by(id_idx=id_or_name).first()
            except ValueError:
                player = self.engine.query(Players).filter_by(
                    PlayerID=id_or_name).first()
            if player:
                return player
            else:
                raise Warning('User not found')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def get_player_by_email(self, email):
        if check_email(email):
            player = self.engine.query(Players).filter_by(
                Email=email).first()
            if player:
                return player
            else:
                raise Warning('Email not found')
        else:
            raise Warning(
                'Invalid search, value must be string email')

    def set_player(self, id_or_username, column_name, new_value):
        if isinstance(id_or_username, int) or isinstance(id_or_username, str) and not isinstance(id_or_username, bool):
            if check_column(column_name):
                try:
                    id_or_username = int(id_or_username)
                    player = self.engine.query(
                        Players).filter_by(id_idx=id_or_username).first()
                except ValueError:
                    player = self.engine.query(Players).filter_by(
                        PlayerID=id_or_username).first()
                if player:
                    if column_name.lower() == "PlayerID".lower():
                        player.PlayerID = new_value
                    elif column_name.lower() == "Passwd".lower():
                        if len(new_value) < 8:
                            raise Warning(
                                'Weak password, must be 8 or more characters')
                        player.Passwd = mysql_password_hash(new_value)
                    elif column_name.lower() == "Passwd_Q".lower():
                        player.Passwd_Q = new_value
                    elif column_name.lower() == "Passwd_A".lower():
                        player.Passwd_A = new_value
                    elif column_name.lower() == "Name".lower():
                        if isinstance(new_value, str):
                            player.Name = new_value
                        else:
                            raise Warning(
                                'Name must be a string')
                    elif column_name.lower() == "JuminNo".lower():
                        player.JuminNo = new_value
                    elif column_name.lower() == "nYear".lower():
                        player.nYear = new_value
                    elif column_name.lower() == "nMonth".lower():
                        player.nMonth = new_value
                    elif column_name.lower() == "nDay".lower():
                        player.nDay = new_value
                    elif column_name.lower() == "Sex".lower():
                        if new_value == 1 or new_value == 2 or new_value == "1" or new_value == "2":
                            player.Sex = new_value
                        else:
                            raise Warning(
                                'Invalid value, sex needs to be 1 (male) or 2 (female)')
                    elif column_name.lower() == "TelePhone1".lower():
                        player.TelePhone1 = new_value
                    elif column_name.lower() == "TelePhone2".lower():
                        player.TelePhone2 = new_value
                    elif column_name.lower() == "TelePhone3".lower():
                        player.TelePhone3 = new_value
                    elif column_name.lower() == "CPhone1".lower():
                        player.CPhone1 = new_value
                    elif column_name.lower() == "CPhone2".lower():
                        player.CPhone2 = new_value
                    elif column_name.lower() == "CPhone3".lower():
                        player.CPhone3 = new_value
                    elif column_name.lower() == "ZipCode".lower():
                        player.ZipCode = new_value
                    elif column_name.lower() == "AddressDo".lower():
                        player.AddressDo = new_value
                    elif column_name.lower() == "AddressSi".lower():
                        player.AddressSi = new_value
                    elif column_name.lower() == "AddressDong".lower():
                        player.AddressDong = new_value
                    elif column_name.lower() == "AddressEtc".lower():
                        player.AddressEtc = new_value
                    elif column_name.lower() == "Address".lower():
                        player.Address = new_value
                    elif column_name.lower() == "Email".lower():
                        if check_email(new_value):
                            player.Email = new_value
                        else:
                            raise Warning(
                                'Invalid Email')
                    elif column_name.lower() == "JobType".lower():
                        player.JobType = new_value
                    elif column_name.lower() == "SchoolName".lower():
                        player.SchoolName = new_value
                    elif column_name.lower() == "Access".lower():
                        player.Access = new_value
                    elif column_name.lower() == "Block".lower():
                        if check_block(new_value):
                            player.Block = new_value.upper()
                        else:
                            raise Warning(
                                'Invalid Block Value')
                    elif column_name.lower() == "LoginIP".lower():
                        player.LoginIP = new_value
                    elif column_name.lower() == "NewsLetter".lower():
                        if new_value == 1 or new_value == 2 or new_value == "1" or new_value == "2":
                            player.NewsLetter = new_value
                        else:
                            raise Warning(
                                'Invalid value, NewsLetter needs to be 1 (enable) or 2 (disable)')
                    elif column_name.lower() == "ParentName".lower():
                        player.ParentName = new_value
                    elif column_name.lower() == "ParentJuminNo".lower():
                        player.ParentJuminNo = new_value
                    elif column_name.lower() == "ParentPhone1".lower():
                        player.ParentPhone1 = new_value
                    elif column_name.lower() == "ParentPhone2".lower():
                        player.ParentPhone2 = new_value
                    elif column_name.lower() == "ParentPhone3".lower():
                        player.ParentPhone3 = new_value
                    elif column_name.lower() == "LastLoginDate".lower():
                        format_data = format_datetime(new_value)
                        if format_data == "Invalid string format" or format_data == "Invalid input type":
                            raise Warning(
                                format_data)
                        else:
                            player.LastLoginDate = format_data
                    elif column_name.lower() == "SecederDate".lower():
                        format_data = format_datetime(new_value)
                        if format_data == "Invalid string format" or format_data == "Invalid input type":
                            raise Warning(
                                format_data)
                        else:
                            player.SecederDate = format_data
                    elif column_name.lower() == "PayPlayDate".lower():
                        format_data = format_datetime(new_value)
                        if format_data == "Invalid string format" or format_data == "Invalid input type":
                            raise Warning(
                                format_data)
                        else:
                            player.PayPlayDate = format_data
                    elif column_name.lower() == "PayPlayHours".lower():
                        player.PayPlayHours = new_value
                    elif column_name.lower() == "RegDate".lower():
                        format_data = format_datetime(new_value)
                        if format_data == "Invalid string format" or format_data == "Invalid input type":
                            raise Warning(
                                format_data)
                        else:
                            player.RegDate = format_data
                    elif column_name.lower() == "OldBlock".lower():
                        if check_block(new_value):
                            player.OldBlock = new_value.upper()
                        else:
                            raise Warning(
                                'Invalid OldBlock Value')
                    elif column_name.lower() == "ssoChk".lower():
                        player.ssoChk = new_value
                    elif column_name.lower() == "AuthCheck".lower():
                        if check_authcheck(new_value):
                            player.AuthCheck = new_value.upper()
                        else:
                            raise Warning(
                                'Invalid OldBlock Value')
                    elif column_name.lower() == "AuthTimeLimit".lower():
                        player.AuthTimeLimit = new_value
                    elif column_name.lower() == "LoginState".lower():
                        if new_value == 0 or new_value == 1 or new_value == "0" or new_value == "1":
                            player.LoginState = new_value
                        else:
                            raise Warning(
                                'Invalid value, LoginState needs to be 0 (off) or 1 (on)')
                    elif column_name.lower() == "personal_auth".lower():
                        player.personal_auth = new_value
                    elif column_name.lower() == "Accesschecktype".lower():
                        if isinstance(new_value, int):
                            player.Accesschecktype = new_value
                        else:
                            raise Warning(
                                'Invalid value, use only integer value')
                    elif column_name.lower() == "PlayerNickName".lower():
                        player.PlayerNickName = new_value
                    elif column_name.lower() == "PlayerGameServer".lower():
                        player.PlayerGameServer = new_value
                    elif column_name.lower() == "IsAdmin".lower():
                        if isinstance(new_value, int):
                            player.IsAdmin = new_value
                        else:
                            raise Warning(
                                'Invalid value, use only integer value')
                    elif column_name.lower() == "CashPoint".lower():
                        if isinstance(new_value, int):
                            player.CashPoint = new_value
                        else:
                            raise Warning(
                                'Invalid value, use only integer value')

                    self.engine.commit()
                else:
                    raise Warning('User not found')
            else:
                raise Warning(
                    'Invalid column name')
        else:
            raise Warning(
                'Invalid search, value must be number or string ')

    def add_user(self, username, password, name, email, block, authcheck, ipaddress, isadmin, cashpoint):
        if check_username(username):
            if self.engine.query(Players).filter_by(PlayerID=username).first():
                raise Warning('User already exist')
        else:
            raise Warning('Invalid character')

        if check_email(email):
            if self.engine.query(Players).filter_by(Email=email).first():
                raise Warning('Email already exist')
        else:
            raise Warning('Invalid email')

        if len(password) < 8:
            raise Warning(
                'Password must be 8 characters or more')
        elif not check_password(password):
            raise Warning('Password has invalid character')

        if not check_block(block):
            raise Warning(
                'Block is invalid, use a valid value')

        if not check_authcheck(authcheck):
            raise Warning(
                'AuthCheck is invalid, use a valid value')

        if check_number(cashpoint):
            raise Warning(
                'CashPoint must be number integer')

        my_user = Players()
        my_user.PlayerID = username
        my_user.Passwd = mysql_password_hash(password)
        my_user.Name = name
        my_user.Email = email
        my_user.block = block
        my_user.authcheck = authcheck
        my_user.LoginIP = ipaddress
        my_user.RegDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        my_user.IsAdmin = isadmin
        my_user.CashPoint = cashpoint
        self.engine.add(my_user)
        self.engine.commit()
        return True

    def del_user(self, username, password):
        if check_username(username):
            if check_password(password):
                player = self.engine.query(Players).filter(
                    Players.PlayerID == username, Players.Passwd == mysql_password_hash(password)).first()
                if player:
                    self.engine.delete(player)
                    self.engine.commit()
                    return True
                else:
                    raise Warning(
                        'Usuário ou senha inválidos')
            else:
                raise Warning('Password invalid character')
        else:
            raise Warning('Username invalid character')
