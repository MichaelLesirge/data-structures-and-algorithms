special_units = [
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]

tens = [
    "zero", "ten", "twenty", "thirty", "forty", 
    "fifty", "sixty", "seventy", "eighty", "ninety",
]

large_units = [
    "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion", "decillion", "undecillion", "duodecillion", "tredecillion", "quattuordecillion", "quindecillion", "sexdecillion", "septendecillion", "octodecillion", "novemdecillion", "vigintillion"
]

def num_to_word(n):
    if n < 20:
        return special_units[n]

    if n < 100:
        unit, extra = divmod(n, 10)
        return tens[unit] + ("-" + num_to_word(extra) if extra != 0 else "")
    
    last = 1000
    for i, unit_name in enumerate(large_units):
        current = last * 1000
        print(current, last)
        if n < current:
            unit, extra = divmod(n, last)
            return f"{num_to_word(unit)} {unit_name}{' ' + num_to_word(extra) if extra != 0 else ''}"
        last = current
    
    raise Exception(f"Can not handle numbers larger than {current-1}")

print("Warning: Not funtional yet. Still a work in progress")
while True:
    print(num_to_word(int(input("Enter number:"))).title())