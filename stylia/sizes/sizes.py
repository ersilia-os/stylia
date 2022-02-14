class Sizes(object):

    def __init__(self, support="slide"):
        if support == "slide":
            self.linewidth = 1
            self.fontsize = 16
            self.s = 30
        elif support == "paper":
            self.linewidth = 1
            self.fontsize = 10
            self.s = 50
        else:
            pass
        self._set_rc_params()

    def _set_rc_params(self):
        pass


class SymbolSize(Sizes):
    
    def __init__(self, support):
        Sizes.__init__(self, support=support)

    def fit(self, data):
        pass

    def transform(self, data):
        pass

