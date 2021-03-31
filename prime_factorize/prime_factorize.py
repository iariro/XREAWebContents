import sys
import unittest

def prime_factorize(num):
    primes = []
    for i in range(2, num + 1):
        while True:
            if num % i == 0:
                primes.append(i)
                num //= i
            else:
                break
    return primes

######################################################################
# test code
######################################################################

class prime_factorize_test(unittest.TestCase):
    def test_1(self):
        self.assertEqual([2, 2, 5, 5], prime_factorize(100))

# python3 -m unittest prime_factorize.prime_factorize_test.test_1
