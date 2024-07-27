import redis


R = redis.Redis(host='localhost', port=6379, decode_responses=True)

EXPIRE_10MIN = 600
EXPIRE_1HOUR = 3600
EXPIRE_1DAY = 86_400
EXPIRE_3DAY = 86_400 * 3
EXPIRE_1WEEK = 86_400 * 7
