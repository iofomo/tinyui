# -*- encoding:utf-8 -*-
# @brief:  ......
# @Author: ...
# @Date:   2023.05.15 00:00:19

from framework.CommandBase import CommandBase


# --------------------------------------------------------------------------------------------------------------------
def createCommand(typ, path, args):
    if typ != 'tree': return None
    return SampleTreeCommand(path, args)


class SampleTreeCommand(CommandBase):
    def __init__(self, path, args):
        CommandBase.__init__(self, path, args)

    def run(self):
        if not CommandBase.run(self): return
        # TODO set module value from arguments ...
        self.mModule.doAction()
