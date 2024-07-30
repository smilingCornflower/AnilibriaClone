import redis


R = redis.Redis(host='localhost', port=6379, decode_responses=True)

EXPIRE_10MIN = 600
EXPIRE_1HOUR = 3600
EXPIRE_3HOUR = 3600 * 3
