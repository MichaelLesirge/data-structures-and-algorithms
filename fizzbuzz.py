def main():
    print("Standard FizzBuzz:")
    print(fizzbuzz())

    print("Custom Fizzbuzz:")
    print(fizzbuzz(mapper = {2: "Even", 5: "Steven"}))



def fizzbuzz(n: int = 100, *, mapper: dict[int, str] = {3: "Fizz", 5: "Buzz"}) -> str:
    return "\n".join(
        "".join(word for divisor, word in mapper.items() if num % divisor == 0) or str(num)
        for num in range(1, n + 1))
    
# First one I made
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
