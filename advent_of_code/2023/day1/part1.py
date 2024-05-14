with open("2023_advent_of_code/day1/input.in", "r") as file:
    text = file.readlines()
    
total = 0
for line in text:
    digits = [char for char in line if char.isdigit()]
    output = int(digits[0] + digits[-1])
    total += output
 
print(total)
    
