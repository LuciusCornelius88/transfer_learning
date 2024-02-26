royal_flash = ["KH", "AH", "QH", "JH", "10H"]
streight_flash = ["QC", "JC", "10C", "9C", "8C"]
four_of_kind = ["5C", "5S", "5H", "5D", "QH"]
full_house = ["2H", "2D", "2S", "10H", "10C"]
flush = ["2D", "KD", "7D", "6D", "5D"]
streight = ["JC", "10H", "9C", "8C", "7D"]
three_of_kind = ["10H", "10C", "10D", "2D", "5S"]
two_pair = ["KD", "KH", "5C", "5S", "6D"]
pair = ["2D", "2S", "9C", "KD", "10C"]
high_card = ["KD", "5H", "2D", "10C", "JH"]

higher_ranks = {
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}


def define_royal_flash(ranks, suites):
    # 10 - A, same suite
    royal_ranks = [10, 11, 12, 13, 14]
    ranks = sorted(ranks)
    return len(set(suites)) == 1 and ranks == royal_ranks


def define_streight_flash(ranks, suites):
    # 5 in range, same suite
    ranks = sorted(ranks)
    return len(set(suites)) == 1 and ranks == list(range(ranks[0], ranks[0] + 5))


def define_four_of_kind(ranks, suites):
    # 4 equal ranks
    # for r in ranks:
    #     if ranks.count(r) == 4:
    #         return True
    # return False
    ranks_as_set = list(set(ranks))
    return len(ranks_as_set) == 2 and ranks.count(ranks_as_set[0]) in [1, 4]


def define_full_house(ranks, suites):
    # 3 equal rank + 2 equal (another) rank
    # ranks = sorted(ranks)
    # return ((ranks.count(ranks[0]) == 2 and ranks.count(ranks[-1]) == 3) or
    #         (ranks.count(ranks[0]) == 3 and ranks.count(ranks[-1]) == 2))
    ranks_as_set = list(set(ranks))
    return len(ranks_as_set) == 2 and ranks.count(ranks_as_set[0]) in [2, 3]


def define_flush(ranks, suites):
    # 5 same suite
    # return suites.count(suites[0]) == 5
    return len(set(suites)) == 1


def define_streight(ranks, suites):
    # 5 in range
    ranks = sorted(ranks)
    return ranks == list(range(ranks[0], ranks[0] + 5))


def define_three_of_kind(ranks, suites):
    # 3 equal rank
    # for r in ranks:
    #     if ranks.count(r) == 3:
    #         return True
    # return False
    ranks_as_set = list(set(ranks))
    return len(ranks_as_set) == 3 and ranks.count(ranks_as_set[0]) in [1, 3]


def define_two_pair(ranks, suites):
    # 2 equal rank + 2 equal (another) rank
    ranks_as_set = list(set(ranks))
    return len(ranks_as_set) == 3 and ranks.count(ranks_as_set[0]) in [1, 2]


def define_pair(ranks, suites):
    # 2 equal rank
    # for r in ranks:
    #     if ranks.count(r) == 2:
    #         return True
    # return False
    ranks_as_set = list(set(ranks))
    return len(ranks_as_set) == 4 and ranks.count(ranks_as_set[0]) in [1, 2]


def define_high_card(ranks):
    # highest rank
    rank = sorted(ranks, reverse=True)[0]
    if rank > 10:
        idx = list(higher_ranks.values()).index(rank)
        return list(higher_ranks.keys())[idx]
    else:
        return rank


def split_rank_suite(lst):
    ranks = []
    suites = []

    for item in lst:
        if len(item) == 2:
            rank = item[0]
            suite = item[1]
        else:
            rank = item[0:2]
            suite = item[2]

        if rank in list(higher_ranks.keys()):
            rank = higher_ranks[rank]

        ranks.append(int(rank))
        suites.append(suite)

    return ranks, suites


def define_poker_hand(poker_hands, hand):
    # ranks, suites = split_rank_suite(royal_flash)
    # ranks, suites = split_rank_suite(streight_flash)
    # ranks, suites = split_rank_suite(four_of_kind)
    # ranks, suites = split_rank_suite(full_house)
    # ranks, suites = split_rank_suite(flush)
    # ranks, suites = split_rank_suite(streight)
    # ranks, suites = split_rank_suite(three_of_kind)
    # ranks, suites = split_rank_suite(two_pair)
    # ranks, suites = split_rank_suite(pair)
    ranks, suites = split_rank_suite(hand)

    for key, func in poker_hands.items():
        if func(ranks, suites):
            return key

    return f'High rank: {define_high_card(ranks)}'


def find_poker_hand(hand):
    poker_hands = {
        'royal_flash': define_royal_flash,
        'streight_flash': define_streight_flash,
        'four_of_kind': define_four_of_kind,
        'full_house': define_full_house,
        'flush': define_flush,
        'streight': define_streight,
        'three_of_kind': define_three_of_kind,
        'two_pair': define_two_pair,
        'pair': define_pair,
    }

    return define_poker_hand(poker_hands, hand)


if __name__ == '__main__':
    find_poker_hand()
