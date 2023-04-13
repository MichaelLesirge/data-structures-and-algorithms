def main():
    print("Standard FizzBuzz:")
    print(fizzbuzz())

    print("\nCustom Fizzbuzz:")
    print(fizzbuzz(mapper = {2: "Even", 5: "Steven"}))
    

# Final version, use list comp (may or may not be better depending on who you ask)
def fizzbuzz(n: int = 100, *, mapper: dict[int, str] = {3: "Fizz", 5: "Buzz"}) -> str:
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
