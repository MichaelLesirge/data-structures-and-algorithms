"""
Time Complexity: O(N^2)
Auxiliary Space: O(1)

Bubbles value up by swapping them so the higher is on the left side

Pros:
- simple
- no extra memory
- elements with same key maintain relative order

Cons:
- O(N^2) so slow for long lists
"""

def swap(array: list, i: int, j: int) -> None:
    array[i], array[j] = array[j], array[i]

def bubble_sort(array: list) -> None:
    n = len(array)

    for i in range(1, n):
        done = True
        
        for j in range(n-i):
            if array[j] > array[j+1]:
                swap(array, j, j+1)
                done = False
                
        if done: break