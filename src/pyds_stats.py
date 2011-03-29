'''
Created on Mar 29, 2011

@author: reineking
'''

import inspect
import sys
import time
import random
from pyds import MassFunction
import numpy


iterations = 10


def stats(results):
    array = numpy.empty((iterations, 1))
    for i, t in enumerate(results):
        array[i] = t
    return array.mean(), array.std()

def measure_time(f, *args):
    def f_measured(i):
        t = time.clock()
        f(*args)
        return time.clock() - t
    return stats(map(f_measured, range(iterations)))

def measure_error(actual, f, *args):
    def f_measured(i):
        t = time.clock()
        f(*args)
        return time.clock() - t
    return stats(map(f_measured, range(iterations)))

def random_likelihoods(singleton_count):
    return [(i, random.random()) for i in range(singleton_count)]


def time_bel():
    return measure_time(MassFunction.gbt(random_likelihoods(12)).bel, frozenset(range(10)))

def time_plausibility():
    return measure_time(MassFunction.gbt(random_likelihoods(12)).pl, frozenset(range(10)))

def time_commonality():
    return measure_time(MassFunction.gbt(random_likelihoods(12)).q, frozenset(range(10)))

def time_gbt():
    return measure_time(MassFunction.gbt, random_likelihoods(12))

def time_gbt_100():
    return measure_time(MassFunction.gbt, random_likelihoods(12), True, 100)

def time_gbt_1000():
    return measure_time(MassFunction.gbt, random_likelihoods(12), True, 1000)

def time_combine_conjunctive():
    m1 = MassFunction.gbt(random_likelihoods(6))
    m2 = MassFunction.gbt(random_likelihoods(6))
    return measure_time(m1.combine_conjunctive, m2)

def time_combine_conjunctive_direct():
    m1 = MassFunction.gbt(random_likelihoods(6))
    m2 = MassFunction.gbt(random_likelihoods(6))
    return measure_time(m1.combine_conjunctive, m2, 1000, 'direct')

def time_combine_conjunctive_importance():
    m1 = MassFunction.gbt(random_likelihoods(6))
    m2 = MassFunction.gbt(random_likelihoods(6))
    return measure_time(m1.combine_conjunctive, m2, 1000, 'importance')

def time_combine_disjunctive():
    m1 = MassFunction.gbt(random_likelihoods(6))
    m2 = MassFunction.gbt(random_likelihoods(6))
    return measure_time(m1.combine_disjunctive, m2)

def time_combine_gbt():
    return measure_time(MassFunction.gbt(random_likelihoods(6)).combine_gbt, random_likelihoods(6))

def time_combine_gbt_direct():
    return measure_time(MassFunction.gbt(random_likelihoods(6)).combine_gbt, random_likelihoods(6), 1000, False)

def time_combine_gbt_importance():
    return measure_time(MassFunction.gbt(random_likelihoods(6)).combine_gbt, random_likelihoods(6), 1000, True)

def time_pignistic():
    return measure_time(MassFunction.gbt(random_likelihoods(12)).pignistic)

def time_markov_update():
    m = MassFunction.gbt(random_likelihoods(4))
    return measure_time(MassFunction.gbt(random_likelihoods(4)).markov_update, lambda s: m)

def time_markov_update_sampling():
    samples = MassFunction.gbt(random_likelihoods(4)).sample(1000)
    return measure_time(MassFunction.gbt(random_likelihoods(4)).markov_update, lambda s, n: samples[:n], 1000)


def error_gbt_100():
    return measure_error(MassFunction.gbt(random_likelihoods(10)), MassFunction.gbt, random_likelihoods(12), True, 100)

def error_gbt_1000():
    return measure_error(MassFunction.gbt(random_likelihoods(10)), MassFunction.gbt, random_likelihoods(12), True, 1000)

def error_combine_conjunctive_direct_100():
    return measure_error(MassFunction.gbt(random_likelihoods(10)), MassFunction.gbt, random_likelihoods(12), True, 100)

def error_combine_conjunctive_direct_1000():
    return measure_error(MassFunction.gbt(random_likelihoods(10)), MassFunction.gbt, random_likelihoods(12), True, 1000)


def run_measures(prefix):
    mod = sys.modules[__name__]
    filt = lambda x: inspect.isfunction(x) and inspect.getmodule(x) == mod and x.__name__.startswith(prefix + '_')
    print('%-32s%-7s (%4s)' % ('function', 'mean', 'stddev'))
    print('-' * 50)
    for f in sorted(filter(filt, globals().copy().values()), key=str):
        random.seed(0)
        print('%-32s%.4fs (+-%.4f)' % ((f.__name__[len(prefix) + 1:],) + f()))


if __name__ == '__main__':
    print('time performance:')
    run_measures('time')
    print('\n')
    print('approximation error:')
    run_measures('error')
