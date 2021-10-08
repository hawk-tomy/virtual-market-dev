from __future__ import annotations


class Account:
    def __init__(self):
        pass

    @classmethod
    def from_schema(cls, db, column):
        pass

    @classmethod
    def from_new(cls, db):
        pass

    def importer(self, new):
        pass

    def exporter(self, new):
        pass
