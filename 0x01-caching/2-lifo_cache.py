#!/usr/bin/python3
"""Create a class LIFOCache that inherits from
BaseCaching and is a caching system:
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """_summary_
    """
    def __init__(self):
        """_summary_
        """
        super().__init__()

    def put(self, key, item):
        """ Add key and value to the cache"""
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key, last_value = self.cache_data.popitem()
            print("DISCARD: {}". format(last_key))

        self.cache_data[key] = item

    def get(self, key):
        """return the value in self.cache_data linked to key
        """
        if key is None or key not in self.cache_data.keys():
            return None
        return self.cache_data.get(key)
