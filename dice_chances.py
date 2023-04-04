try:
    import numpy as np
except ImportError as exs:
    raise ImportError("Sorry, you have to download this file and install numpy to run this project. Try anouther one.") from exs
    
"""
super inefficient but its more to learn numpy 
"""

def gcd(n, d):
    while d:
        n, d = d, n % d
    return n

def reduce(numerator: int, denominator: int) -> tuple[int, int]:
    greatest = gcd(numerator, denominator)
    return (numerator//greatest, denominator//greatest)

def dice_chances(dice_sides: int, num_of_dice: int, /, flat: bool = False, as_list: bool = False) -> np.ndarray:
    if num_of_dice <= 0 or dice_sides <= 0:
        dice_nums_total = np.array([], dtype=np.int32)
    else:
        def create(*args):
            # return sum((num+1 for num in args))
            total = 0
            for num in args:
                total += num + 1
            return total

        dice_nums_total = np.array(
            [np.fromfunction(create, [dice_sides for _ in range(num_of_dice)], dtype=np.int32)]
        )

        if flat:
            dice_nums_total = dice_nums_total.flatten()
    return dice_nums_total

def make_list_words(l: list, sep = ", ", word = " and ") -> str:
    l = list(map(str, l))
    if len(l) == 1: return l[0]
    return sep.join(l[:-1]) + word + l[-1]
    

def main():
    dice_sides = int(input("How many sides does the dice have: ").removeprefix("d").strip())
    num_of_dice = int(input("How many dice do you want: "))

    dice_nums_total = dice_chances(dice_sides, num_of_dice)

    print(dice_nums_total)

    dice_nums_flat = dice_nums_total.flatten()
    count_nums = np.bincount(dice_nums_flat)
    len_nums = dice_nums_flat.size

    if len_nums == 0:
        print("No roles will be possible")
        return    
    
    sorted_nums_count = count_nums.argsort()
    most_common_nums = []
    max_seen_times = count_nums[sorted_nums_count[-1]]
    
    i = -1
    while count_nums[sorted_nums_count[i]] == max_seen_times:
        most_common_nums.insert(0, sorted_nums_count[i])
        i -= 1
            
    min_num, max_num = dice_nums_flat.min(initial=num_of_dice), dice_nums_flat.max(initial=0)
    
    many_common = len(most_common_nums) != 1

    # print(f"\n{min_num=}, {max_num=}, {avg_num=}, {len_nums=}")
    
    print(
        f"\nTheir are {len_nums} possible permutations and {max_num - min_num + 1} combinations of roles.",
        f"The minimum role you could get is {min_num} and the maximum is a {max_num}.",
        f"The most common role{'s' if many_common else ''} {'are' if many_common else 'is'} {make_list_words(most_common_nums)}, {'each ' if many_common else ''}having a {round(max_seen_times / len_nums * 100, 5)}% chance of being rolled.",
        "",
        sep="\n")

    while True:
        user_request = input("Enter your number: ")
        if user_request.lower() in ["exit", "ex", "leave"]:
            print("Good bye!")
            return
        else:
            user_request = int(user_request)

            amount = count_nums[user_request] if min_num <= user_request <= max_num else 0

            reduced_n, reduced_d = reduce(amount, len_nums)
            reduced = f"({reduced_n} in {reduced_d}) " if (reduced_n, reduced_d) != (amount, len_nums) and amount != 0 else ''

            print(f"{amount} in {len_nums} {reduced}chance of getting a {user_request}.")
            print(f"{round(amount / len_nums * 100, 5)}% chance.\n")


if __name__ == "__main__":
    main()