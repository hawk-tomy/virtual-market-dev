from __future__ import annotations


class Bank:

    #initialize

    def __init__(self, db):
        pass

    @classmethod
    def from_column(cls, db, column):
        pass

    @classmethod
    def from_new(cls, data):
        pass

    #for property

    @property
    def setting(self):
        pass

    #for setting

    def update_setting(self, new):
        pass

    #for periodically

    def get_log_amount(self):
        pass

    #for account

    def move(self, before, after, amount):
        pass
