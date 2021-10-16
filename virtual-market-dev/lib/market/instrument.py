class instrument:
    @classmethod
    def from_column(cls, db, column):
        pass

    @classmethod
    def from_new(
        cls, 
        db, 
        from_ac, # partial account instance
        to_ac, # partial acount instance
        amount, 
        currency, 
        *, 
        exchange=False,
    ):
        pass
