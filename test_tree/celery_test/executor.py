from test_tree.celery_test.tasks import gen_prime

import time

primes = gen_prime.delay(1000)

while True:
    time.sleep(1)
    print(primes.ready())
    print(primes.get(propagate=True))