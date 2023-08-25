﻿class HistoryUpdateDataItemModelJSON(object):
    """description of class"""
    def __init__(self, path, updateType, values, typePath = None):
        self._path = path
        self._typePath = typePath
        self._updateType = updateType
        self._values = values

    def toDict(self):
        jsonValues = []
        for value in self._values:
            jsonValues.append(value.toDict());

        typePath = None
        if self._typePath != None:
          typePath = self._typePath.toDict()

        return {'path': self._path.toDict(), 'typePath' : typePath, 'updateType': self._updateType, 
               'values' : jsonValues }

