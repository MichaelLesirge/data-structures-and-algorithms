def main():
    print("Standard FizzBuzz")
    fizzbuzz()

    print("Custom Fizzbuzz")
    fizzbuzz(mapper = {2: "Even", 5: "Steven"})


def fizzbuzz(n: int = 100, *, mapper: dict[int, str] = None) -> None:
    if mapper is None:
        mapper = {3: "Fizz", 5: "Buzz"}
    
    for num in range(1, n + 1):
        out = ""
        for disable_num, message in mapper.items():
            if num % disable_num == 0:
                out += message
        print(out or num)


if __name__ == "__main__":
    main()
