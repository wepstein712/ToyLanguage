# internal representation of a ["fun*" [arguments] [body]] with the env when it was declared
import copy
class funcVal:

    def __init__(self):
        self.args = None
        self.body = None
        self.workingEnv = None

    def __init__(self, args, body, env):
        self.args = args
        self.body = body
        self.workingEnv = copy.deepcopy(env)

    def __repr__(self):
        # return "[\"funcVal\", \"" + str(self.args) + str(self.body) +  "]"
        return "\"closure\""

    def __str__(self):
        # return "[\"funcVal\", \"" + str(self.args) + str(self.body) +  "]"
        return "\"closure\""


