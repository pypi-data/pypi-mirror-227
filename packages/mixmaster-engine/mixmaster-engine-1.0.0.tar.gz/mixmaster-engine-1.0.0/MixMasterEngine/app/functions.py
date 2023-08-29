from datetime import datetime
import hashlib
import re


def mysql_password_hash(password):
    stage1 = hashlib.sha1(password.encode('utf-8')).digest()
    stage2 = hashlib.new('sha1', stage1).digest()
    hashed_password = '*' + stage2.hex().upper()
    return hashed_password


def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(regex, email):
        return True
    else:
        return False


def check_block(block):
    blocks = {'allow', 'game', 'web', 'sum', 'suceder', 'wait'}
    for b in blocks:
        if block.lower() == b:
            return True
    return False


def check_authcheck(authcheck):
    authchecks = {'auth_ok', 'auth_wait', 'auth_check'}
    for b in authchecks:
        if authcheck.lower() == b:
            return True
    return False


def check_username(user):
    excluded_chars = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    for char in user:
        if char in excluded_chars:
            return False
    return True


def check_password(password):
    excluded_chars = " *?'+/()=}][{"
    for char in password:
        if char in excluded_chars:
            return False
    return True


def format_datetime(value):
    if isinstance(value, str):
        try:
            datetime_obj = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            formatted_string = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            return formatted_string
        except ValueError:
            return "Invalid string format"
    elif isinstance(value, datetime):
        formatted_string = value.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_string
    else:
        return "Invalid input type"


def check_column(column):
    columns = {"id_idx", "PlayerID", "Passwd", "Passwd_Q", "Passwd_A", "Name", "JuminNo", "nYear", "nMonth", "nDay", "Sex", "TelePhone1", "TelePhone2", "TelePhone3", "CPhone1", "CPhone2", "CPhone3", "ZipCode", "AddressDo", "AddressSi", "AddressDong", "AddressEtc", "Address", "Email", "JobType", "SchoolName", "Access", "Block", "LoginIP",
               "NewsLetter", "ParentName", "ParentJuminNo", "ParentPhone1", "ParentPhone2", "ParentPhone3", "LastLoginDate", "SecederDate", "PayPlayDate", "PayPlayHours", "RegDate", "OldBlock", "ssoChk", "AuthCheck", "AuthTimeLimit", "LoginState", "personal_auth", "Accesschecktype", "PlayerNickName", "PlayerGameServer", "IsAdmin", "CashPoint"}
    for c in columns:
        if c.lower() == column.lower():
            return True
    return False


def check_string(string):
    if not isinstance(string, bool) and isinstance(string, str):
        return True
    else:
        return False


def check_number(number):
    if not isinstance(number, bool) and isinstance(number, int) or isinstance(number, str):
        try:
            number = int(number)
            return True
        except:
            return False
    else:
        return False
