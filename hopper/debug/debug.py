from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hopper as hp

from enum import IntEnum
from enum import IntFlag


class DbgChn(IntFlag):
    NONE    = 0
    STD     = 1
    DATA    = 2
    NET     = 4
    VIEW    = 8
    VALID   = 16


class DbgLvl(IntEnum):
    NONE    = 0
    NOTSET  = 0
    MAX     = 5
    DEBUG   = 10
    MED     = 15
    INFO    = 20
    WARNING = 30
    MIN     = 35
    ERROR   = 40
    CRITICAL= 50


_dbg_cfg = hp.Opt()
_dbg_cfg += hp.Opt(level=DbgLvl.MAX, channel=DbgChn.STD |
                                             DbgChn.DATA |
                                             DbgChn.NET |
                                             DbgChn.VIEW |
                                             DbgChn.VALID)

def dbg_cfg_val():
    global _dbg_cfg
    return _dbg_cfg

def dbg_cfg(**kwargs):
    global _dbg_cfg
    _dbg_cfg *= hp.Opt(kwargs)
    if dbg_vld(DbgChn.STD, DbgLvl.DEBUG):
        hp.print_pp(_dbg_cfg)

def dbg_chn(channel):
    global _dbg_cfg
    return bool(_dbg_cfg.channel & channel)

def dbg_lvl(level):
    global _dbg_cfg
    return _dbg_cfg.level <= level

def dbg_vld(channel, level):
    return dbg_chn(channel) and dbg_lvl(level)

