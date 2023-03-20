units = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
    11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
    15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
    19: "nineteen",
}

tens = {
    2: "twenty", 3: "thirty", 4: "forty", 5: "fifty",
    6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety",
}

large_unites = {
    10: ("", "-"),
    100: (" hundred ", + " and "),
    1000: (" thousand ", " ")
}


def num_to_word(n):
    if n == 0:
        return "zero"

    if n < 20:
        return units[n]
    
    # TODO replace this with large_unit dict and for loop. Also use divmod 
    elif n < 100:
        return tens[n // 10] + ("-" + num_to_word(n % 10) if n % 10 != 0 else "")
    elif n < 1_000:
        return num_to_word(n // 100) + " hundred" + (" and " + num_to_word(n % 100) if n % 100 != 0 else "")
    elif n < 1_000_000:
        return num_to_word(n // 1000) + " thousand" + (" " + num_to_word(n % 1000) if n % 1000 != 0 else "")
    else:
        raise Exception("Can not handle numbers larger than 999,999")

i = 1
while True:
    print(i, num_to_word(i))
    i += 1
    i *= 2