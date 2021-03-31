#!/usr/local/bin/python3
from bottle import route, template, request
import prime_factorize

@route('/')
def index():
    return template('index.html')

@route('/factorize', method='POST')
def factorize():
    try:
        number = int(request.POST.getunicode('number'))
        primes = prime_factorize.prime_factorize(number)
        return template('factorize.html', number=number, primes=primes)
    except Exception as e:
        return str(e)
