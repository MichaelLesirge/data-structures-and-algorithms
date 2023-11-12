    
def insertion_sort(array: list) -> None:
    n = len(array)
        
    for i in range(1, n):
        
        key = array[i]
                
        j = i - 1
        
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
            
        array[j + 1] = key
    