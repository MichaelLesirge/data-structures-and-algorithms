from functools import lru_cache

from runner import welcome, run, print_input_error, get_valid_input


int_settings = (int, "input most be a number")

def main():

    welcome("fibonacci sequence calculator")
    choice = input("Do you want the first n numbers (1) or to get indival number from the fibonacci sequence (2): ")
    if choice == "1":
        n = get_valid_input("How many numbers do you want", int_settings)
        for i in range(1, n):
            print(fib1(i), ",", end=" ", sep="")
        print(fib1(i+1))
    elif choice == "2":
        run(FIB_FUNC, ("Enter your number", int_settings))
    else:
        print_input_error(f"{choice} must be '1' or '2'")




@lru_cache(2)
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