
with open("advent_of_code_2023/day1/input.in", "r") as file:
    text = file.readlines()
    
numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]   

total = 0
for line in text:
    num_indexes = {}
    
    for num_index, num_str in enumerate(numbers):
        for i in range(len(line) - len(num_str)):
            if line[i:i+len(num_str)] == num_str:
                num_indexes[i] = str(num_index)

    for i, char in enumerate(line):
        if char.isdigit():
            num_indexes[i] = char
            
    num_keys = num_indexes.keys()
    output = int(num_indexes[min(num_keys)] + num_indexes[max(num_keys)])
    
    total += output
    
print(total)
    
