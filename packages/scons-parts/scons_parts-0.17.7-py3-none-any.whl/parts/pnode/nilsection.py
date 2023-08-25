
import SCons.Executor


class NilSection:
    '''
    Acts as an empty section for cases for optional depends
    '''

    def __init__(self):
        pass

    def __bool__(self):
        return False

    @property
    def Env(self):
        return SCons.Executor.get_NullEnvironment()
