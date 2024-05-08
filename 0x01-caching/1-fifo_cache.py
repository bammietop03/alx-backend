#!/usr/bin/python3
"""
A class FIFOCache that inherits from BaseCaching and is a caching system
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ A class FIFOCache that inherits from
        BaseCaching and is a caching system
    """
    def __init__(self):
        """ Calling the super function"""
        super().__init__()

    def put(self, key, item):
        """ Add key and value to the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = next(iter(self.cache_data))
            del self.cache_data[first_key]
            print("DISCARD:", first_key)

        self.cache_data[key] = item

    def get(self, key):
        """ Get key and value to the cache"""
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data[key]
