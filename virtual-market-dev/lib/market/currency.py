from __future__ import annotations


class Currency:
    def __init__(self):
        pass

    @classmethod
    def from_schema(cls, db, column):
        pass

    @classmethod
    def from_new(cls, db):
        pass

    def new_rate(self, new):
        pass

    def update_setting(self):
        pass

    def save(self):
        pass
