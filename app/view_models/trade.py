class TradeInfo:

    def __init__(self, info):
        self.total = 0
        self.trades = []
        self.__parse(info)

    def __parse(self, info):
        self.total = len(info)
        self.trades = [self.__map_to_trade(gift_or_wish) for gift_or_wish in info]

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
