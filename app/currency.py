"""
currencyClass.py

"""

class Currency:
    """ Models a Currency 

        Args:
            code: the three character code used to represent the currency
            name: the currency's name
            buys: value in € that one unit of the currency buys
            sells: value of this currency that €1 buys
    """

    def __init__(self, code, name, buys, sells):
        self.code = code
        self.name = name
        self.buys = float(buys)
        self.sells = float(sells)