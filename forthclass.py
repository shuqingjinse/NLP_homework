# _*_ coding:utf-8 _*_
import time
from collections import defaultdict
from functools import lru_cache
from functools import wraps #还原func help
# help(lru_cache)
prices = defaultdict(lambda: -float('inf'))
for i, v in enumerate([1, 5, 8, 9, 10, 17, 17, 20, 24, 30]):
    prices[i+1] = v

## 策略2：用自带的lru_cache
# @lru_cache(maxsize=2*10)
# def revenue(r):
#     return max([prices[r]] + [(revenue(i) + revenue(r-i)) for i in range(1, r)])

## 策略3：写一个memo
def memo(func):
    cache = {}
    @wraps(func)
    def _wrap(*args, **kwargs):
        # print('\tHi, I am function:{}'.format(func.__name__))
        str_key = str(args) + str(kwargs)
        if str_key not in cache:
            result = func(*args, **kwargs)
            cache[str_key] = result
        return cache[str_key]
    return _wrap
@memo
def new_function(some_lst):
    return sum(some_lst)
# new_function([1,2,3])

## 优化0:获取最大值
# @memo
# def revenue(r):
#     return max([prices[r]] + [(revenue(i) + revenue(r-i)) for i in range(1, r)])
## 优化1：获取最大值的策略
solution = {}
@memo
def revenue(r):
    split, r_star = max([(0, prices[r])] + [(i, revenue(i) + revenue(r - i)) for i in range(1, r)], key=lambda x: x[1])
    solution[r] = (split, r-split)
    return r_star
revenue(100)
# print(revenue(57))
# print(solution)

def parse_solution(r, revenue_solution):
    assert r in revenue_solution
    left, right = revenue_solution[r]
    if left == 0 : return [right]
    else:
        return [left] + parse_solution(right,revenue_solution)

def pretty_solution(splits):
    return ' => '.join(map(str,splits))
print(pretty_solution(parse_solution(57, solution)))


## 策略1：存在cache中
# cache = {}
# def revenue(r):
#     if r in cache: return cache[r]
#     r_optimal = max([prices[r]] + [(revenue(i) + revenue(r-i)) for i in range(1, r)])
#     cache[r] = r_optimal
#     return r_optimal


# time1 = time.time()
# print(revenue(15))
# print(help(revenue))
# time2 = time.time()
# print(time2 - time1)

## 装饰器
# def print_hi(func):
#     def _wrap(*args, **kwargs):
#         print('\tHi, I am function:{}'.format(func.__name__))
#         return func(*args, **kwargs)
#     return _wrap
# @print_hi
# def add(a, b) : return a + b
# #print_hi_add = print_hi(add) ==> @print_hi
# add(1, 10)
# help(add)





