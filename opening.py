# Copyright (C) 2024 Warren Usui, MIT License
"""
Get a list of opening words
"""
from random import randrange
from itertools import product
from get_dict import get_dict

def opening():
    """
    Opening words are all possible words that do not repeat letters and
    use one of the most common five letters for each letter position.
    """
    def o_main(wdict):
        def histogram(letters):
            return list(map(lambda a: [a, letters.count(a)],
                            'abcdefghijklmnopqrstuvwxyz'))
        def sort_hist(histv):
            return sorted(histv, key=lambda a: a[1])[::-1]
        def get_letters(histv):
            return list(map(lambda a: a[0], histv[0:5]))
        def cleanup(llist):
            return list(filter(lambda a: a in wdict,
                    list(map(lambda a: ''.join(list(a)),
                    list(filter(lambda a: len(set(a)) == len(a), llist))))))
        return cleanup(list(product(*list(map(get_letters, list(map(sort_hist,
                list(map(histogram, list(map(list, zip(*wdict))))))))))))
    return o_main(get_dict())

def pick_opening():
    """
    Pick a random first word
    """
    def po_inner(in_data):
        return in_data[randrange(len(in_data))]
    return po_inner(opening())
