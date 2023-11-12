import unittest

import random

import bubble, insertion, selection, merge, quick


def make_random(length: int, num_range: tuple[int, int] = None) -> list[int]:
    array = [(random.randint(*num_range) + 1 if num_range else i) for i in range(length)]
    if num_range is None: random.shuffle(array)
    return array

algorithms = [bubble.bubble_sort, insertion.insertion_sort, selection.selection_sort, merge.merge_sort, quick.quick_sort]

class TestLinkedList(unittest.TestCase):
    def assert_all_sorted(self, array: list):
        sorted_array = sorted(array)
        for algorithm in algorithms:
            array_copy = array.copy()
            algorithm(array_copy)
            self.assertEqual(array_copy, sorted_array, f"Failed algorithm: {algorithm.__name__}")
    
    def test_empty(self):
        self.assert_all_sorted([])

    def test_one(self):
        self.assert_all_sorted([1])

    def test_two_sorted(self):
        self.assert_all_sorted([1, 2])
        
    def test_two_unsorted(self):
        self.assert_all_sorted([2, 1])
    
    def test_two_same(self):
        self.assert_all_sorted([1, 1])
            
    def test_long(self):
        self.assert_all_sorted(make_random(100))
            
    def test_bumpy_long(self):
        self.assert_all_sorted(make_random(100, num_range=(0, 1000)))
            
    def test_negative_long(self):
        self.assert_all_sorted(make_random(20, num_range=(-100, 100)))

if __name__ == '__main__':
    unittest.main()