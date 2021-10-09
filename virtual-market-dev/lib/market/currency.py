from __future__ import annotations


class Currency:

    #initialize

    def __init__(self):
        pass

    @classmethod
    def from_schema(cls, db, column):
        pass

    @classmethod
    def from_new(cls, db):
        pass

    #for save

    def save(self):
        pass

    #for property

    @property
    def setting(self):
        pass

    #for setting

    def update_setting(self, new):
        pass

    def new_rate(self, new):
        pass
