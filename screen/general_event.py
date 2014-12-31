
class GeneralEvent(object):
    #: :type: tuple
    scenario = None

    #: :type: int
    index = 0

    def __init__(self, scenario):
        self.scenario = scenario

    def __iter__(self):
        return self

    def next(self):
        if self.index == len(self.scenario):
            raise StopIteration
        data = self.scenario[self.index]
        self.index += 1
        return data
