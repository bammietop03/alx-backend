#!/usr/bin/python3
"""
A class BasicCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """A BasicCache that inherits from BaseCaching
        and is a caching system
    """
    def __init__(self):
        """calling the super function"""
        super().__init__()

    def put(self, key, item):
        """ Add key and value to the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ Get key and value to the cache"""
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
