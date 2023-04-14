from typing import Callable


def main():
    print("Standard FizzBuzz:")
    print(fizzbuzz())

    print("\nCustom Fizzbuzz with fizzbuzz_map={2: \"Even\", 5: \"Steven\"}:")
    print(fizzbuzz(fizzbuzz_map={2: "Even", 5: "Steven"}))
    
    print("\nCustom Fizzbuzz with compare_func=lambda num, compare: num % compare == 0 and num % 7 != 0)")
    print(fizzbuzz(compare_func=lambda num, compare: num % compare == 0 and num % 7 != 0))


# Final version, use passed in funtion to compare. Also don't set mutable object as default argument
def fizzbuzz(upper_bound: int = 100, *, fizzbuzz_map: dict[int, str] = {3: "Fizz", 5: "Buzz"}, compare_func: Callable[[int, int], bool] = lambda num, compare: num % compare == 0) -> str:
    return "\n".join(
        "".join(word for compare_value, word in fizzbuzz_map.items() if compare_func(num, compare_value)) or str(num)
        for num in range(1, upper_bound + 1))


# Thrid version, use list comp (may or may not be better depending on who you ask)
def fizzbuzz_thrid(n: int = 100, *, mapper: dict[int, str] = {3: "Fizz", 5: "Buzz"}) -> str:
    return "\n".join(
        "".join(word for divisor, word in mapper.items() if num % divisor == 0) or str(num)
        for num in range(1, n + 1))


# Second version, returns list instead of printing out immediately
def fizzbuzz_second(n: int = 100, *, mapper: dict[int, str] = None) -> None:
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
def fizzbuzz_first(n: int = 100, *, mapper: dict[int, str] = None) -> None:
    if mapper is None:
        mapper = {3: "Fizz", 5: "Buzz"}

    for num in range(1, n + 1):
        out = ""
        for divisor, word in mapper.items():
            if num % divisor == 0:
                out += word
        print(out or num)


if __name__ == "__main__":
    main()
