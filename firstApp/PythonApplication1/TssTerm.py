class TssTerm:
    """Класс терма"""

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
            self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
            self.__name = name

    @property
    def normalForm(self):
        return self.__normalForm

    @normalForm.setter
    def normalForm(self, normalForm):
            self.__normalForm = normalForm


    def __init__(self):
        """Constructor"""
        self.id = -1
        self.name = ''


