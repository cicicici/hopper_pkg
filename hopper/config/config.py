from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time
import sys
import argparse
import configparser
import json

import hopper as hp


class Config(object):

    def __init__(self, name="demo", app='viewer', argv=None, command=None):
        self._name = name
        self._app = app
        if argv is None:
            self._argv = sys.argv[1:]
            self._command = sys.argv[0]
        else:
            self._argv = argv
            self._command = command

        self.init_args()
        self.parse_args()
        self.default_config()
        self.init_config()
        self.save_config()
        self.post_config()

    def init_args(self):
        self.args_parser = argparse.ArgumentParser(
            description="Hopper {}".format(self._name),
            epilog="Usage: {} -c config.ini [options]".format(self._command)
        )

        # required argument
        self.args_parser.add_argument('-c', type=str, action="store",
                                      help='Config file',
                                      default="config.ini", required=True)
        # optional arguments
        self.args_parser.add_argument('--name', type=str, help='Name')
        self.args_parser.add_argument('--tag', type=str, help='Tag')
        self.args_parser.add_argument('--host', type=str, help='Datalink host')
        self.args_parser.add_argument('--port', type=int, help='Datalink port')
        self.args_parser.add_argument('--out_dir', type=str, help='Output dir')
        self.args_parser.add_argument('--run_dir', type=str, help='Model dir')
        self.args_parser.add_argument('--add', type=str, help='Addtitional options')

        if self._app == 'viewer':
            self.args_parser.add_argument('--data_dir', type=str, help='Data dir')
            self.args_parser.add_argument('--data_filter', type=str, help='Data dir filter')

    def parse_args(self):
        self._args = self.args_parser.parse_args(self._argv)
        #print(self._args)

    def default_config(self):
        self._default_config = {}

        section = 'args'
        self._default_config[section] = {}
        # common configurations
        self._default_config[section]['name'] = "Hopper"
        self._default_config[section]['tag'] = ""
        self._default_config[section]['host'] = "127.0.0.1"
        self._default_config[section]['port'] = 7001
        self._default_config[section]['out_dir'] = "_tmp/hopper"
        self._default_config[section]['run_dir'] = ""
        self._default_config[section]['add'] = {}

        if self._app == 'viewer':
            self._default_config[section]['data_dir'] = "_tmp/viewer"
            self._default_config[section]['data_filter'] = ".+"

        # debug configurations
        section = 'debug'
        self._default_config[section] = {}
        self._default_config[section]['channel'] = 255
        self._default_config[section]['level'] = 5

    def init_config(self):
        self._config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self._config.read(self._args.c)

        self._opt = hp.Opt()

        # load config to opt
        for section in self._config.sections():
            opt = hp.Opt()
            for key in self._config[section]:
                val_str =  self._config[section][key]
                val = json.loads(val_str)
                opt[key] = val
            self._opt[section] = opt

        # override with command line args
        for arg in vars(self._args):
            val = getattr(self._args, arg)
            if val is None:
                continue
            val_str = str(val)

            if arg in self._opt.args or arg in self._default_config['args']:
                if arg in self._opt.args:
                    opt_val = self._opt.args[arg]
                else:
                    opt_val = self._default_config['args'][arg]

                if isinstance(opt_val, str):
                    val_str = '"' + val_str + '"'

                if type(opt_val) is not type(val):
                    print("[Convert Arg] {}: {}, {} => {}".format(arg, val, type(val), type(opt_val)))
                    self._opt.args[arg] = json.loads(val_str)
                else:
                    self._opt.args[arg] = val
                self._config['args'][arg] = val_str

        # add default settings
        for section in self._default_config:
            opt = hp.Opt()
            for key in self._default_config[section]:
                if key not in self._opt[section]:
                    opt[key] = self._default_config[section][key]
                    self._config[section][key] = json.dumps(opt[key])
            self._opt[section] += opt

        # additional post process
        if self._opt.args.add is not None and type(self._opt.args.add) is dict:
            self._opt.args.add = hp.util.dict_to_opt(self._opt.args.add)

    def save_config(self):
        run_dir = self._opt.args.run_dir
        if not (run_dir is not None and run_dir.startswith('/')):
            if run_dir is None or len(run_dir) == 0:
                run_dir=time.strftime('%Y%m%d_%H%M%S', time.localtime())
            if len(self._opt.args.tag) > 0:
                run_dir = run_dir + "_" + self._opt.args.tag
            run_dir="{}/{}".format(self._opt.args.out_dir, run_dir)

        try:
            if not os.path.isdir(run_dir):
                os.makedirs(run_dir)
        except:
            pass
        self._opt.args.run_dir = run_dir
        self._config['args']['_run_dir'] = '"' + run_dir + '"'
        # config file
        with open('{}/config.ini'.format(run_dir), 'w') as configfile:
            self._config.write(configfile)
        # log file
        hp.set_log_file('{}/log.txt'.format(run_dir))

        self._run_dir = run_dir

    def post_config(self):
        # Set debug settings
        hp.dbg_cfg(level=self._opt.debug.level,
                   channel=self._opt.debug.channel)

        # dump important information
        hp.info(hp.DC.STD, "{} - {}".format(self._opt.args.name, self._opt.args.tag))

    def dump_config(self):
        if self._app == 'viewer':
            hp.info(hp.DC.NET, "Hopper: $ viewer --logdir {} --port {}".format(self._run_dir, 6006))

    def opt(self):
        return self._opt;

