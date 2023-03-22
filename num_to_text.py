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
    "hundred", "thousand", "million", "billion", "trillion",
]

def num_to_word(n):
    if n < 20:
        return special_units[n]

    if n < 100:
        value, extra = divmod(n, 10)
        return tens[value] + ("-" + num_to_word(extra) if extra != 0 else "")

    last = 100
    current = 1
    for word in large_units:
        current *= 1000
        if n < current:
            value, extra = divmod(n, last)
            return num_to_word(value) + " " + word + (" " + num_to_word(extra) if extra else "")
        last = current
    
while True:
    print(num_to_word(int(input("Enter number: "))).title())