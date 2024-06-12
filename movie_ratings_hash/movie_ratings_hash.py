# Implementation of a hash table in Python which will be used to implement a memory cache
# Collision handling will be done using linear probing
import numpy as np 

# Each element in our array needs to hold a key-value pair
# We create a node class to hold the pair 
# We also implement a mechanism to keep track of whether the node was accessed recently
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class HashTable:
    # Initialise the Hash table
    # Use numpy empty array for the associative array
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.buckets = np.empty(capacity, dtype=Node)
    
    # We will be using the built in hash function
    # Since this returns integers of arbitrary sizes, we 
    # use the mod function to ensure they fit in the array
    def hash(self, key):
        return hash(key) % self.capacity
    

    # Set a key-value pair in the hash table
    def set(self, key, value):
        # Hash the key of the pair
        index = self.hash(key)

        # Check if there is a collision
        if (self.buckets[index] == None):
            self.buckets[index] = Node(key, value)
            self.size += 1
        else:
            # If there is a collision find the next empty spot to insert
            index += 1
            if (index == self.capacity):
                index = 0

            while (self.buckets[index] != None):
                index += 1
                if (index == self.capacity):
                    index = 0

            self.buckets[index] = Node(key, value)
            self.size += 1

    # Get the node associated with a given key
    def get(self, key):
        # Find dictionary matching value in list
        for sub in self.buckets:
            if key.lower() in sub.key.lower():
                return sub


    # Get the node with the lowest value
    def get_lowest_value_item(self):
        return min(self.buckets, key=lambda x: (x.value, x.key))
    

    # Get the node with the highest value
    def get_highest_value_item(self):
        return max(self.buckets, key=lambda x: (x.value, x.key))
