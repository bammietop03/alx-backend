#!/usr/bin/python3
""" BaseCaching module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ A class LRUCache that inherits from BaseCaching
    and is a caching system"""
    def __init__(self):
        """ initializing """
        super().__init__()
        self.access_tracker = []

    def put(self, key, item):
        if key is None or item is None:
            return

        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # If cache is full, discard the least recently used item (LRU)
            lru_key = self.access_tracker.pop(0)
            del self.cache_data[lru_key]
            print("DISCARD:", lru_key)

        self.cache_data[key] = item
        self.access_tracker.append(key)

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        # Update access_tracker to reflect recent access
        self.access_tracker.remove(key)
        self.access_tracker.append(key)

        return self.cache_data[key]
