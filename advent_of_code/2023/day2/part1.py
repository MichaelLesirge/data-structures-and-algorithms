
with open("advent_of_code_2023/day2/input.in", "r") as file:
    text = file.readlines()

valid = {"red": 12, "green": 13, "blue": 14}

total = 0

for line in text:
    
    id_part, data = line.split(": ")
    data = data.strip()
    
    id_num = int(id_part.lstrip("Game"))
    
    values = []
    for value in data.split(", "):
        values.extend(value.split("; "))
    
    
    highest = {}
    for value in values:
        num, color = value.split(" ")
        num = int(num)
        highest[color] = max(highest.get(color, num), num)

    
    correct = all(highest[key] <= valid[key] for key in highest)
    if correct:
        total += id_num
            
        
print(total)