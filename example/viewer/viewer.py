#! /usr/bin/python
# -*- coding: utf8 -*-

import hopper as hp
import time

# Configuration
cfg = hp.config.Config(name="VIEWER")
cfg.dump_config()
ARGS = cfg.opt().args

# Datalink over network
def datalink_recv(socket, packet):
    opt = hp.Opt().loads(packet._data.decode())
    #print(opt)
    # Set learning rate
    if opt.t == 'cmd':
        if opt.a == 'set':
            if opt.key == 'lr':
                #hp.train.set_lr_val(opt.val)
                pass

    hp.util.datalink().send_opt_sock(socket, hp.Opt(ACK='OK'))

if ARGS.port > 1000:
    hp.util.datalink_start(port=ARGS.port)
    hp.util.datalink_register_recv(datalink_recv)


hp.util.datalink_close()

