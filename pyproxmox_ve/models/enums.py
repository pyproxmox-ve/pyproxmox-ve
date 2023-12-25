from enum import Enum


class ConsoleEnum(str, Enum):
    applet = "applet"
    vv = "vv"
    html5 = "html5"
    xtermjs = "xtermhjs"


class AccessACLEnum(str, Enum):
    user = "user"
    group = "group"
    token = "token"
