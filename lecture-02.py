import pandas as pd
ord('我')
filename = '80k_articles.txt'
all_content = open(filename, 'r', encoding='UTF-8').read()
print(len(all_content))
# print(all_content[:200])

import re
import requests
# 抓取网页信息
text = requests.get('http://movie.douban.com/').text
#
def tokenize(string):
    return ''.join(re.findall('[\w|\d]+', string))
tokenize('\u3000\u3000新华社华盛顿４月１３日电（记者林小春）寻找外星生命，目前最理想的地点可能是土星卫星土卫二上的冰封小世界。美国航天局１３日宣布，“卡西尼”探测器在土卫二喷出的羽流中探测到氢气，这意味着土卫二具备生命存在的几乎所有已知要素。\\n\u3000\u3000这项发表在美国《科学》杂志上的研究显示，土卫二羽流中９８％是水，约１％是氢气，其余是二氧化碳、甲烷和氨等组成的混合物。\\n\u3000\u3000“卡西尼”项目科学家琳达·施皮尔克当天在网')


ALL_CHARACTER = tokenize(all_content)
# print(len(ALL_CHARACTER))

from collections import Counter
L = [1,1,2,3,4,4,4]
# print(Counter(L))
all_character_counts = Counter(ALL_CHARACTER)
# print(all_character_counts.most_common())

import  matplotlib.pyplot  as plt


M = all_character_counts.most_common()[0][1]
# print(M)

from matplotlib.pyplot import yscale, xscale, title, plot
yscale('log'); xscale('log'); title('Frequency of n-th most frequent word and 1/n line.')
plot([c for (w, c) in all_character_counts.most_common()])
plot([M/i for i in range(1, len(all_character_counts)+1)])

# plt.show()

#两种函数调用方式计算的资源消耗的不同
def get_probability_from_counts(count):
    all_occurences = sum(count.values())
    def get_prob(item):
        return count[item] / all_occurences
    return get_prob

get_char_prob = get_probability_from_counts(all_character_counts)

def get_char_probability(char):
    all_occurences = sum(all_character_counts.values())
    return all_character_counts[char] / all_occurences

import time

def get_running_time(func, arg, times):
    start_time = time.time()
    for _ in range(times):
        func(arg)
    print('\t\t {} used time is {}'.format(func.__name__, time.time() - start_time))

import  random

random_chars = random.sample(ALL_CHARACTER, 1000)
get_running_time(get_char_probability, '神', 1000)
get_running_time(get_char_prob, '神', 1000)
from functools import reduce
from operator import mul, add

# print(reduce(add, range(1, 101)))

def prob_of_string(string):
    return reduce(mul, [get_char_prob(c) for c in string])

print(prob_of_string('这是一个比较常见测试用例')) # 在这个语料的基础上组成此字符串的可能性
print(prob_of_string('这是一个比较罕见的测试用例'))
print(prob_of_string('广州有一个地方叫做沥窖'))
print(prob_of_string('杭州有一个地方叫做西湖'))

pair = """前天晚上吃晚饭的时候
前天晚上吃早饭的时候""".split('\n')
pair2 = """正是一个好看的小猫
真是一个好看的小猫""".split('\n')
pair3 = """我无言以对，简直
我简直无言以对""".split('\n')
pairs = [pair, pair2, pair3]
def get_probability_prefromance(language_model_func, pairs):
    for (p1, p2) in pairs:
        print('*'*18)
        print('\t\t {} with probability {}'.format(p1, language_model_func(tokenize(p1))))
        print('\t\t {} with probability {}'.format(p2, language_model_func(tokenize(p2))))
# get_probability_prefromance(prob_of_string, pairs)
# 以上是单个字组成句子 的可能性
# 接下来是 2个字 组成句子 的可能性

gram_length = 2
two_gram_counts = Counter(ALL_CHARACTER[i:i+gram_length] for i in range(len(ALL_CHARACTER) - gram_length))
# print(two_gram_counts.most_common()[:20]) # 两两组合的频次
# ***
# 两两组成 频次转为概率的核心
get_pair_prob = get_probability_from_counts(two_gram_counts)


def get_2_gram_prob(word, prev):
    if get_pair_prob(word + prev) > 0:
        return get_pair_prob(word + prev) / get_char_prob(prev)
    else:
        return get_char_prob(word)


def get_2_gram_string_prob(string):
    probablities = []
    for i, c in enumerate(string):
        prev = '<s>' if i == 0 else string[i - 1]
        probablities.append(get_2_gram_prob(c, prev))
    return reduce(mul, probablities)
# ***
# 对比1-gram 和2-gram的可能性

get_probability_prefromance(prob_of_string, pairs)

get_probability_prefromance(get_2_gram_string_prob, pairs)

string_pair = ['发表了重要的讲话', '发表了重要的僵化']
print(get_2_gram_string_prob(string_pair[0]))
print(get_2_gram_string_prob(string_pair[1]))
##Some More
# 教学演示版本， 如果你想获得更好的结果，需要查阅更多资料，然后有很多小的点（stop words, smooth, OOV(out of vacabulary)）；
# 我们需要更多数据；
# 数据也要保证高质量；

