from functools import lru_cache

def main():

    print("Welcome to the fibonacci sequence calculator!")
    choice = input("Do you want the first n numbers (1) or to get indival number from the fibonacci sequence (2): ")
    print()
    if choice == "1":
        n = int(input("How many numbers do you want: "))
        for i in range(1, n):
            print(FIB_FUNC(i), ",", end=" ", sep="")
        print(FIB_FUNC(i+1))
    elif choice == "2":
        while True:
            number = int(input("Enter your number: "))
            print(FIB_FUNC(number))
            print()
    else:
        print(f"Invalid input, {choice} must be '1' or '2'")


@lru_cache(3)
def fib1(n):
    if n < 2:
        return n
    return fib1(n-1) + fib1(n-2)


# no imports
def fib2(n, memo={0: 0, 1: 1}):
    if n not in memo:
        memo[n] = fib2(n-1) + fib2(n-2)
    return memo[n]


FIB_FUNC = fib1
if __name__ == "__main__":
    main()