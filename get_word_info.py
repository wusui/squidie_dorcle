# Copyright (C) 2024 Warren Usui, MIT License
"""
Solve sedecordle page
"""
from itertools import chain
from setup_selenium import read_word_set

def get_word_info(dvr):
    """
    Get a list of information for each word to guess
    """
    def find_letter_set(linfo):
        return sorted(list(set(list(map(lambda a: a[0],
                list(filter(lambda a: a[1] == linfo[1],
                list(chain.from_iterable(linfo[0])))))))))
    def set_blackv(owords):
        def fix_dup_letters(full_let_info):
            return list(filter(lambda a: a not in full_let_info[1],
                               full_let_info[0]))
        return fix_dup_letters([find_letter_set([owords, 'B']),
                find_letter_set([owords, 'G']) +
                find_letter_set([owords, 'Y'])])
    def find_letter_col(linfo):
        def sg_pos(indx):
            def sg_words(iword):
                if iword[indx][1] == linfo[1]:
                    return iword[indx][0]
                return ''
            return list(map(sg_words, linfo[0]))
        return list(map(''.join, list(map(sg_pos, list(range(0,5))))))
    def set_greenv(owords):
        def rmdups(letters):
            if len(letters) > 1:
                return letters[0]
            return letters
        return list(map(rmdups, find_letter_col([owords, 'G'])))
    def set_yellowv(owords):
        return {'letters': find_letter_set([owords, 'Y']),
                'bad_columns': find_letter_col([owords, 'Y'])}
    def info_doubles(owords):
        def d_word(aword):
            def cntw(new_wlist):
                def chkl(olist):
                    def ifmt(linfo):
                        return list(filter(lambda a: a[1] > 1, linfo))
                    return ifmt(list(map(lambda a: [a, olist.count(a)],
                                    list(set(olist)))))
                return chkl(list(map(lambda a: a[0], new_wlist)))
            return cntw(list(filter(lambda a: a[1] != 'B', aword)))
        return list(map(d_word, owords))
    def get_org_data(owords):
        return {'cant_have': set_blackv(owords),
                'must_have': set_greenv(owords),
                'also_have': set_yellowv(owords),
                'lit_doubles': info_doubles(owords)}
    def zip_each_word(wordd):
        return list(zip(wordd[0], wordd[1]))
    def gwi_main(wdata):
        return get_org_data(list(map(zip_each_word, wdata)))
    def find_pwords(wnumb):
        return gwi_main(read_word_set({'driver': dvr, 'set': wnumb}))
    return list(map(find_pwords, list(range(1,17))))
