from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dynaconf import Dynaconf
# Import Database classes
from .app.Profile import Profiles
from .app.Member import Members
from .app.LogDB import LoginLogs
from .app.S_Data import Data
from .app.gamedata import Game
from .app.Web_Account import GameTailMall
# Exemplo de uso

settings = Dynaconf(
    envvar_prefix="DYNACONF",  # export envvars with `export DYNACONF_FOO=bar`.
    settings_files=['settings.toml'],  # Load files in the given order.
)


class DatabaseConnector:

    def __init__(self):

        self.host = str(settings.default.host)
        self.user = str(settings.default.user)
        self.password = str(settings.default.password)
        self.port = int(settings.default.porta)
        self.players = str(settings.default.players)
        self.game = str(settings.default.game)
        self.data = str(settings.default.data)
        self.log = str(settings.default.log)
        self.gametail = str(settings.default.gametail)
        # DataBase Member
        engine = create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.players}"
        )
        self.Players = sessionmaker(bind=engine)

        # DataBase gamedata
        engine = create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.game}"
        )
        self.Game = sessionmaker(bind=engine)

        # DataBase S_Data
        engine = create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.data}"
        )
        self.Data = sessionmaker(bind=engine)

        # DataBase LogDB
        engine = create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.log}"
        )
        self.Log = sessionmaker(bind=engine)

        # DataBase Web_Account
        engine = create_engine(
            f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.gametail}"
        )
        self.Gametail = sessionmaker(bind=engine)


def database_connect():
    try:
        engine = DatabaseConnector()
        return engine
    except SQLAlchemyError as err:
        print(f"Erro de conexão com o banco de dados: {err}")


def profile(userName):
    engine = database_connect()
    engine = Profiles(engine.Players(), userName)
    return engine


def data():
    engine = database_connect()
    engine = Data(engine.Data())
    return engine


def players():
    engine = database_connect()
    engine = Members(engine.Players())
    return engine


def loginLog():
    engine = database_connect()
    engine = LoginLogs(engine.Log())
    return engine


def game():
    engine = database_connect()
    engine = Game(engine.Game())
    return engine


def gametail():
    engine = database_connect()
    engine = GameTailMall(engine.Gametail())
    return engine
