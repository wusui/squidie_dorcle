# Copyright (C) 2024 Warren Usui, MIT License
"""
Sedecordle solver, main interface
"""
import sys
import time
from itertools import chain
from random import randrange
from find_all_possible_words import find_all_possible_words
from setup_selenium import handle_word_input, read_word_set, start_selenium
from get_word_info import get_word_info
from opening import opening, pick_opening
from screen import scroll_move

def get_elem_len(wlists):
    """
    Get the lengths of each of the word lists for the 16 sedecordle words
    """
    return list(map(len, wlists))

def solver():
    """
    Main sedecordle solver
    """
    def s_have_dvr(dvr):
        def fill_in_one_solution(plist):
            def do_actions(ind_wd):
                scroll_move({'driver': dvr, 'word_numb': ind_wd[0] + 1})
                handle_word_input({'driver': dvr,
                                   'guess': ind_wd[1][0].lower()})
                time.sleep(2)
            list(map(do_actions, plist))
        def s_have_wlist(wlist):
            def xtract_green(row):
                if 'G' not in row[-1]:
                    return False
                return list(filter(lambda a: a[-1][-1] == 'G',
                      list(enumerate(list(zip(row[0], row[1]))))))
            def gen_green_word(word_disp):
                return [''.join(list(map(lambda a:
                        dict(list(chain.from_iterable(list(filter(None,
                        list(map(xtract_green, word_disp)))))))[a][0],
                        list(range(0, 5)))))]
            def get_cpat(numb):
                return read_word_set({'driver': dvr, 'set': numb + 1})
            def find_green_exit(indv_wrd):
                if indv_wrd[-1][-1].count('G') == 5:
                    return False
                return gen_green_word(indv_wrd)
            def pick_next_w(nlist):
                def write_word(lword):
                    if lword:
                        handle_word_input({'driver': dvr,
                                           'guess': lword.lower()})
                def pnw_hwi(sh_list):
                    if sh_list:
                        return sh_list[randrange(len(sh_list))]
                    if not nlist[0]:
                        return False
                    return nlist[0][randrange(len(nlist[0]))]
                write_word(pnw_hwi(list(filter(lambda a: a in opening(),
                                list(map(lambda a: a.lower(), nlist[0]))))))
            if sum(get_elem_len(wlist)) == 0:
                fill_in_one_solution(list(filter(lambda a: a[1],
                            list(enumerate(list(map(find_green_exit,
                            list(map(get_cpat, list(range(0, 16)))))))))))
                time.sleep(15)
                dvr.close()
                sys.exit(0)
            if 1 not in get_elem_len(wlist):
                pick_next_w(list(filter(lambda a: len(a) ==
                            max(get_elem_len(wlist)), wlist)))
            else:
                fill_in_one_solution(list(filter(lambda a: len(a[1]) == 1,
                                    enumerate(wlist))))
            return s_have_wlist(find_all_possible_words(get_word_info(dvr)))
        handle_word_input({'driver': dvr, 'guess': pick_opening()})
        return s_have_wlist(find_all_possible_words(get_word_info(dvr)))
    return s_have_dvr(start_selenium('?mode=free'))

if __name__ == "__main__":
    solver()
