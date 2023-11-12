
def swap(array: list, i: int, j: int) -> None:
    array[i], array[j] = array[j], array[i]

def selection_sort(array: list) -> None:
    n = len(array)
    
    for i in range(n-1):
        min_index = i
        
        for j in range(i+1, n):
            if array[j] < array[min_index]:
                min_index = j
                
        swap(array, i, min_index)