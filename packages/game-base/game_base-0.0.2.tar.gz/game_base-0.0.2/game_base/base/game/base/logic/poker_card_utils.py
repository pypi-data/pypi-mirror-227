def get_card_value(card):
    r"""
     获取牌的值
    :param card:牌
    :return:
    """
    return card % 100


def get_card_color(card):
    r"""
     获取牌的花色
    :param card:牌
    :return:
    """
    return card / 100


def is_same_value(cards, count):
    r"""
    :是否有相同值的牌
    :param cards: 所有牌
    :param count: 要找的个数 > 0
    :return bool
    """
    _values = []
    for _card in cards:
        _values.append(get_card_value(_card))
    _values = sorted(_values)
    for i in range(len(cards) - count):
        if _values[i] == _values[i + count]:
            return True


def has_value(cards, value):
    r"""
    :是否有相同值的牌
    :param cards: 所有牌
    :param value: 值
    :return bool
    """
    _values = []
    for _card in cards:
        if get_card_value(_card) == value:
            return True
    return False


def has_color(cards, color):
    r"""
    :是否有相同值的牌
    :param cards: 所有牌
    :param color: 值
    :return bool
    """
    _values = []
    for _card in cards:
        if get_card_color(_card) == color:
            return True
    return False


def is_same_color(cards):
    r"""
    :是否有相同花色的牌
    :param cards: 所有牌
    :return bool
    """
    _values = []
    for _card in cards:
        _values.append(get_card_color(_card))
    _values = sorted(_values)
    return _values[0] == _values[len(_values) - 1]


def is_straight(cards):
    r"""
    :是否顺子
    :param cards: 所有牌
    :return bool
    """
    _values = []
    for _card in cards:
        _values.append(get_card_value(_card))
    _values = sorted(_values)
    for i in range(len(_values)):
        if _values[i] == _values[i + 1] - 1:
            return True


def find_same_value(cards, count):
    r"""
    :是否有相同值的牌
    :param cards: 所有牌
    :param count: 要找的个数 > 1
    :return bool
    """
    _values = []
    for _card in cards:
        _values.append(get_card_value(_card))
    _values = sorted(_values)
    for i in range(len(cards) - count):
        if _values[i] == _values[i + count]:
            return _values[i:i + count]
    return None
