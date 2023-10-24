from collections import Counter
from typing import List


def find_anagrams(first_word: str, second_word: str) -> List[int]:
    len_first_word = len(first_word)
    len_second_word = len(second_word)

    if len_second_word > len_first_word:
        return []

    if len_second_word == 0 or len_second_word == 0:
        return []

    second_word_map = Counter(second_word)
    first_word_map = Counter(first_word[:len_second_word])
    res = []

    for i in range(len_second_word, len_first_word):
        if second_word_map == first_word_map:
            res.append(i - len_second_word)
        first_word_map[first_word[i]] += 1
        first_word_map[first_word[i - len_second_word]] -= 1

    if second_word_map == first_word_map:
        res.append(len_first_word - len_second_word)

    return res


print(find_anagrams('acdbacdacb', 'abc'))
