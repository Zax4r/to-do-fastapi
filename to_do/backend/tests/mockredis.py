class MockRedis:

    def __init__(self):
        self.data = {}

    async def set(self, key, value, ex=300):
        self.data[key] = value

    async def get(self, key):
        return self.data.get(key, None)
