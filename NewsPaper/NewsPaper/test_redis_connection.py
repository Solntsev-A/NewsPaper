import os
import redis
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL")

print("Connecting to:", redis_url)

try:
    r = redis.from_url(redis_url)
    print("Pinging Redis...")
    print("Response:", r.ping())c
    print("✅ Connection successful!")
except Exception as e:
    print("❌ Connection failed:", e)
