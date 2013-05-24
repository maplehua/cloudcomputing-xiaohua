#!/usr/bin/python  
import time
import redis
import random

def random_number():
	pool=redis.ConnectionPool(host='10.77.20.51',port=6379)
	r=redis.Redis(connection_pool=pool)

	while True:
		nn=random.randint(0,120)
		r.set('number',nn)
		time.sleep(1)

if __name__ == '__main__':
    random_number()
