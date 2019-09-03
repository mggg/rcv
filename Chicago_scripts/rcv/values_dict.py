class ValuesDict(dict):
    def __iter__(self):
        return iter(self.values())
