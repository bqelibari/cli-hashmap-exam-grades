"""
Implementation of a hash map using lists for storing multiple values for the
same key.

Copyright 2021, University of Freiburg.
Chair of Algorithms and Data Structures.

Axel Lehmann <lehmann@cs.uni-freiburg.de>
Niklas Schnelle <schnelle@cs.uni-freiburg.de>
Patrick Brosi <brosi@cs.uni-freiburg.de>

"""
from typing import List, Any, Tuple


class HashMap:
    """
    Implements a hash map (associative container) with a fixed number
    of buckets. It supports string keys and values of any type.
    """

    def __init__(self, size: int):
        """
        Creates an empty HashMap with <size> buckets.

        >>> hash_map0 = HashMap(0)
        >>> hash_map1 = HashMap(5)
        """
        self.hash_map = [[None, [None]] for _ in range(size)]

    def insert(self, key: str, value: Any):
        """
        Insert or updates the value to <value> for a given key <key>.

        >>> hash_map = HashMap(5)
        >>> hash_map.insert("test", 5)
        >>> hash_map.lookup("test")
        5
        >>> hash_map.insert("test", "wert")
        >>> hash_map.lookup("test")
        'wert'
        """
        hashed_key = self.key_hash(key)
        index = hashed_key % len(self.hash_map)
        idx_count = index + 1

        if self.hash_map[index][0] is None:
            self.hash_map[index] = [key, [value]]
        elif self.hash_map[index][0] == key:
            self.hash_map[index][1].append(value)
        else:
            while idx_count != index:
                if idx_count == len(self.hash_map):
                    idx_count = 0
                if self.hash_map[idx_count][0] is None:  # field empty->replace
                    self.hash_map[idx_count] = [key, [value]]
                    break
                elif self.hash_map[idx_count][0] == key:  # field not empty
                    self.hash_map[idx_count][1].append(value)
                    break
                else:  # field not empty and keys dont match
                    idx_count += 1

    def lookup(self, key: str) -> Any:

        """
        Return the stored value or None if there is no value
        stored for the key.

        >>> hash_map = HashMap(5)
        >>> not hash_map.lookup("test")
        True
        >>> hash_map.lookup("test") is None  # lookup will not insert!
        True
        >>> hash_map.insert("test", "wert")
        >>> hash_map.lookup("test")
        'wert'
        """
        for idx, element in enumerate(self.hash_map):
            if element[0] == key:
                return element[1][-1]
        return None

    def key_value_pairs(self) -> List[Tuple[str, Any]]:
        """
        Get a list of all (key, value) pairs stored in the
        hash map. This can be used to iterate over the entire map.

        >>> hash_map = HashMap(50)
        >>> hash_map.key_value_pairs()
        []

        >>> hash_map.insert("truth", 42)
        >>> hash_map.insert("NotJustNumbers", "value")
        >>> key_values = hash_map.key_value_pairs()
        >>> # sort so the order is independent of the hash function
        >>> sorted(key_values, key = lambda pair: pair[0])
        [('NotJustNumbers', 'value'), ('truth', 42)]
        """
        result = []
        for field_in_hash_map in self.hash_map:
            for value_idx in range(len(field_in_hash_map[1])):
                if field_in_hash_map != [None, [None]]:
                    result.append((field_in_hash_map[0],
                                   field_in_hash_map[1][value_idx]))
        return sorted(result, key=lambda pair: pair[0])

    @staticmethod
    def key_hash(key: str) -> int:
        """
        Hashes a given string returning an int value.

        >>> type(HashMap.key_hash('ceiling')) == int
        True
        >>> type(HashMap.key_hash('floor')) == int
        True
        >>> HashMap.key_hash('poison') != HashMap.key_hash('food')
        True
        """
        hashed_key = 0
        for idx, char in enumerate(key):
            hashed_key += ord(char) * (113 ** idx)
        return hashed_key
