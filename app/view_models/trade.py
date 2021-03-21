class TradeInfo:

    def __init__(self, db_obj):
        self.total = 0
        self.trades = []
        self.__parse(db_obj)

    def __parse(self, db_obj):
        self.total = len(db_obj)
        self.trades = [self.__map_to_trade(gift_or_wish) for gift_or_wish in db_obj]

    @staticmethod
    def __map_to_trade(gift_or_wish):
        if gift_or_wish.create_datetime:
            time = gift_or_wish.create_datetime.strftime("%Y-%m-%d")
        else:
            time = '未知'
        return dict(
            user_name=gift_or_wish.user.nickname,
            time=time,
            id=gift_or_wish.id
        )
