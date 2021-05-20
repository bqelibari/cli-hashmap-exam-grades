"""
Implementation of a hash map using lists for storing multiple values for the
same key.

Copyright 2021, University of Freiburg.
Chair of Algorithms and Data Structures.

Axel Lehmann <lehmann@cs.uni-freiburg.de>
Niklas Schnelle <schnelle@cs.uni-freiburg.de>
Patrick Brosi <brosi@cs.uni-freiburg.de>

"""
from typing import List, Any, Tuple, Optional


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
        loop_index = index + 1

        key_at_index = self.hash_map[index][0]
        key_at_loop_index = self.hash_map[loop_index][0]

        if key_at_index is None:
            self.insert_key_value_pair_if_key_not_found(index, key, value)
        elif key_at_index == key:
            self.append_value_if_key_exists(index, value)
        else:
            while loop_index != index:
                if loop_index == len(self.hash_map):
                    loop_index = 0
                if key_at_loop_index is None:
                    self.insert_key_value_pair_if_key_not_found(loop_index, key, value)
                    break
                elif key_at_loop_index == key:
                    self.append_value_if_key_exists(loop_index, value)
                    break
                loop_index += 1

    def insert_key_value_pair_if_key_not_found(self, idx: int, key: str, value: Any):
        self.hash_map[idx] = [key, [value]]

    def append_value_if_key_exists(self, index: int, value: Any):
        self.hash_map[index][1].append(value)

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

    def key_value_pairs(self) -> list[tuple[Optional[list[None]], None]]:
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
        return sorted(result, key=lambda pair: pair[0], reverse=True)

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
