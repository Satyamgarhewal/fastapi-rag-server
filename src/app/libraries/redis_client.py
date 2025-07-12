"""Basic connection example.
"""

import redis

redis_client = redis.Redis(
    host='redis-19685.c246.us-east-1-4.ec2.redns.redis-cloud.com',
    port=19685,
    decode_responses=True,
    username="default",
    password="fBvjPFFsgGQybJETLtZGZAOGh5NwMxKC",
)

success = redis_client.set('foo', 'bar')
# True

result = redis_client.get('foo')
print(result)
# >>> bar

