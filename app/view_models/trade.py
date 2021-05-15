from app.view_models.book import BookViewModel


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


class MyTrades:

    def __init__(self, trades_of_mine, wish_count_list):
        self.trades = []
        self.__trades_of_mine = trades_of_mine
        self.__wish_count_list = wish_count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trades in self.__trades_of_mine:
            my_trades = self.__maching(trades)
            temp_trades.append(my_trades)
        return temp_trades

    def __maching(self, trades):
        count = 0
        for wish_count in self.__wish_count_list:
            if trades.isbn == wish_count["isbn"]:
                count = wish_count["count"]
        r = {
            "count": count,
            "book": BookViewModel(trades.book),
            "id": trades.id
        }
        return r
