from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hopper as hp

import pprint
pp = pprint.PrettyPrinter(indent=4)


def print_data_info(data, name="Tensor"):
    hp.debug(hp.DC.NET, "{}: shape {}".format(name, tensor.get_info()), frameskip=1)

def print_pp(obj, name="Obj"):
    global pp
    pp.pprint(obj)

