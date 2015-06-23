# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'


class YML:
    def __init__(self):
        self.offers = []
        self.categories = []
        self.shop = {
            'name': None,
            'company': None,
            'url': '',
            'platform': None,
            'version': None,
            'agency': None,
            'email': None,
        }
        self.currencies = []
        self.cpa = None

    def category_append(self, category, parent=None):
        # get parent
        if not parent is None and not isinstance(parent, int):
            for cat in self.categories:
                if cat['category'] == parent:
                    parent = self.categories.index(cat)
                    break
        category = {'category': category, 'parentId': parent}
        if not category in self.categories:
            self.categories.append(category)

    def currency_append(self, currency_id, rate=None, plus=None):
        """

        :param currency_id:
        :param rate:
        :param plus: %
        :return:
        <currency id="USD" rate="CBRF" plus="1"/> - Курс доллара по ЦБРФ + 1%
        """
        for c in self.currencies:
            if c['id'] == currency_id:
                return

        if rate is None:
            rate = 'CBRF'

        currency = {'id': currency_id, 'rate': rate, 'plus': plus}
        self.currencies.append(currency)

    def offers_append(self, offer, validate=True):
        if validate and offer.validate():
            self.offers.append(offer)
        else:
            self.offers.append(offer)
