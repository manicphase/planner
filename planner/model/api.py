from collections import OrderedDict


class EntityTranslationError(Exception):
    pass


class Api(object):
    __apifields__ = None

    def to_dict(self):
        d = OrderedDict()
        d['entity'] = self.__tablename__
        for field in self.__apifields__:
            d[field] = self.__getattribute__(field)

        return d

    @staticmethod
    def from_dict(cls, data):
        if data['entity'] != cls.__tablename__:
            raise EntityTranslationError

        try:
            r = cls()
            for field in cls.__apifields__:
                r.__setattr__(field, data[field])
        except KeyError:
            raise EntityTranslationError

        return r

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
