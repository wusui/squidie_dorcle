# Copyright (C) 2024 Warren Usui, MIT License
"""
Find words to guess/select
"""
from itertools import chain
from get_dict import get_dict

def find_all_possible_words(wt_data):
    """
    Return lists of possible words, given the words played so far
    """
    def fapw_dict(w_dict):
        def fapw_wlists(wt_entry):
            def chain_doubles():
                return list(chain.from_iterable(wt_entry['lit_doubles']))
            def fapw_chk_double(shrtr_list):
                def chk_dub1(aword):
                    def chk_dub2(dub_val):
                        return list(map(lambda a:
                            aword.count(dub_val[a][0]) == dub_val[a][1],
                            list(range(0, len(dub_val))))).count(True) \
                            == len(dub_val)
                    if not wt_entry['lit_doubles']:
                        return True
                    return chk_dub2(chain_doubles())

                return list(filter(chk_dub1, shrtr_list))
            def fapw_chk_yellow(shrtr_list):
                def chk_bad_cols(sub_list):
                    def indv_col(pos_ans):
                        return list(map(lambda a: pos_ans[a] not in
                                 wt_entry['also_have']['bad_columns'][a],
                                 list(range(0, 5)))).count(True) == 5
                    return list(filter(indv_col, sub_list))
                def y_crunch(yword):
                    if len(wt_entry['also_have']['letters']) == 0:
                        return 0
                    return list(map(lambda a: a in yword,
                                wt_entry['also_have']['letters'])).count(True)
                if len(shrtr_list) < 2:
                    return shrtr_list
                return chk_bad_cols(list(filter(lambda a: y_crunch(a) ==
                        len(wt_entry['also_have']['letters']), shrtr_list)))
            def fapw_chk_green(shrtr_list):
                def g_crunch(gword):
                    def cmp_w_green(cmp_tup):
                        if cmp_tup[1] == '':
                            return True
                        if cmp_tup[0] == cmp_tup[1]:
                            return True
                        return False
                    return list(map(cmp_w_green, list(zip(list(gword),
                            wt_entry['must_have'])))).count(True) == 5
                if len(shrtr_list) < 2:
                    return shrtr_list
                return list(filter(g_crunch, shrtr_list))
            def fapw_wchk_black(dword):
                return list(map(lambda a: a in wt_entry['cant_have'],
                                       dword)).count(False) == 5
            if wt_entry['must_have'].count('') == 0:
                return []
            return fapw_chk_double(fapw_chk_yellow(fapw_chk_green(
                    list(filter(fapw_wchk_black, w_dict)))))
        return list(map(fapw_wlists, wt_data))
    return fapw_dict(list(map(lambda a: a.upper(), get_dict())))
