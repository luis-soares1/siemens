# import os
# import aioredis
# import json



# async def create_redis_pool():
#     global redis_pool
#     redis_pool = await aioredis.create_redis_pool(os.environ.get('REDIS_ENDPOINT_URL'))

# async def put(key, value, ttl):
#     result = await redis_pool.set(key, json.dumps(value), ex=ttl)
#     return bool(result)

# async def get(key):
#     results = await redis_pool.get(key, encoding='utf-8')  
#     if results:
#         return json.loads(results)
#     return None  

# async def incr(key):
#     result = await redis_pool.incr(key)
#     return bool(result)

# # Using aioredis' `iscan` instead of the blocking `scan`
# async def scan():
#     keys = []
#     async for key in redis_pool.iscan():
#         keys.append(key)
#     return keys

# # Make sure to close the connection pool when you're done
# async def close_redis_pool():
#     redis_pool.close()
#     await redis_pool.wait_closed()


# # async def check_cache_before_db(lat: float, lon: float, fn, kwargs):
# #     key = f"{lat}_{lon}"
# #     cached_data = await get(key)
# #     if cached_data:
# #         return cached_data
# #     # If not in cache, query from database
# #     obj = fn(**kwargs)
# #     # Cache the result before returning
# #     if obj:
# #         await put(key, obj, ttl=300)  # cache for 5 minutes or any ttl you prefer
# #     return obj