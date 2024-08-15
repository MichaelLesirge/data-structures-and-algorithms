from typing import Callable

"""Fizzbuzz from simple to complex"""

def main():
    print("Standard FizzBuzz:")
    print(fizzbuzz())

    print("\nCustom Fizzbuzz with fizzbuzz_map={2: \"Even\", 5: \"Steven\"}:")
    print(fizzbuzz(fizzbuzz_map={2: "Even", 5: "Steven"}))
    

# Fourth and final version
# Changes: use passed in function to compare, also better names
def fizzbuzz(upper_bound: int = 100, *, fizzbuzz_map: dict[int, str] = {3: "Fizz", 5: "Buzz"}, compare_func: Callable[[int, int], bool] = lambda num, compare: num % compare == 0) -> str:
    return "\n".join(
        "".join(word for compare_value, word in fizzbuzz_map.items() if compare_func(num, compare_value)) or str(num)
        for num in range(1, upper_bound + 1))


# Third version
# Changes: use list comp (may or may not be better depending on who you ask)
def fizzbuzz_v3(n: int = 100, *, mapper: dict[int, str] = {3: "Fizz", 5: "Buzz"}) -> str:
    return "\n".join(
        "".join(word for divisor, word in mapper.items() if num % divisor == 0) or str(num)
        for num in range(1, n + 1))


# Second version
# Changes: returns list instead of printing out immediately
def fizzbuzz_v2(n: int = 100, *, mapper: dict[int, str] = None) -> None:
    if mapper is None:
        mapper = {3: "Fizz", 5: "Buzz"}

    nums = []
    for num in range(1, n + 1):
        out = ""
        for divisor, word in mapper.items():
            if num % divisor == 0:
                out += word
        nums.append(out or str(num))
    return "\n".join(nums)


# First version
# Fizzbuzz with mapper
def fizzbuzz_v1(n: int = 100, *, mapper: dict[int, str] = None) -> None:
    if mapper is None:
        mapper = {3: "Fizz", 5: "Buzz"}

    for num in range(1, n + 1):
        out = ""
        for divisor, word in mapper.items():
            if num % divisor == 0:
                out += word
        print(out or num)


# My Code Golf FizzBuzz Function. 
def f():[print('Fizz'[i%3*4:]+'Buzz'[i%5*4:]or i) for i in range(1,101)]

# Fizzbuzz in just 62 charters. Only 3 more charters than the shortest one possible fizzbuzz in python3 (at least from what I found).
# I did not look at other cold golfed fizzbuzz solutions before making this
# for i in range(1,101):print('Fizz'[i%3*4:]+'Buzz'[i%5*4:]or i)

if __name__ == "__main__":
    main()
