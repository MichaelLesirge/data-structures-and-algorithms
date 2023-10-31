special_unit_words = [
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
]

tens_words = [
    "zero", "ten", "twenty", "thirty", "forty", 
    "fifty", "sixty", "seventy", "eighty", "ninety",
]

large_unit_words = [
    "hundred", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion", "decillion", "undecillion", "duodecillion", "tredecillion", "quatttuor-decillion", "quindecillion", "sexdecillion", "septen-decillion", "octodecillion", "novemdecillion", "vigintillion"
]

def num_to_word(n: int) -> str:
    if n == 0: return "zero"
    word_components = num_to_word_components(abs(n))
    if n < 0: word_components.insert(0, "negitive")
    return " ".join(word_components)
    
        

def num_to_word_components(n: int) -> list[str]:
    if n == 0:
        return []
    
    if n < 20:
        return [special_unit_words[n]]

    if n < 100:
        tens_count, extra = divmod(n, 10)
        return ["-".join([tens_words[tens_count]] + num_to_word_components(extra))]

    last = 100
    current = 1
    for unit_word in large_unit_words:
        current *= 1000
        if n < current:
            unit_count, extra = divmod(n, last)
            return num_to_word_components(unit_count) + [unit_word] + num_to_word_components(extra)
        last = current
    
    raise Exception(f"Can not convert number higher than {current-1}")
    
while True:
    print(num_to_word(int(input("Enter number: "))).title())
 