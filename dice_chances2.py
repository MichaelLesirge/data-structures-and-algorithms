ROUND_TO = 3  # leave 1 decimal
# ROUND_TO = False  # No rounding


def main():
    print("Welcome to dice chance calculator!")

    dice_sides = int(input("How many sides does the dice have: ").removeprefix("d").strip())
    num_of_dice = int(input("How many dice do you want: ").strip())

    print()

    if 0 in (dice_sides, num_of_dice):
        print("No roles will be possible")
        return

    calculator = DiceCalculator(sides=dice_sides, count=num_of_dice)
    
    most_common_nums = calculator.most_common_nums()

    print(f"There are {calculator.possible_permutations} possible roles that are between {calculator.min} and {calculator.max}.")
    if len(most_common_nums) == 2:
        print(f"The most likely roles are either a {most_common_nums[0]} or a {most_common_nums[1]}.")
    else:
        print(f"The most likely role is a {most_common_nums[0]}.")

    while True:
        number = int(input("Enter your number: "))
        print(f"Chance of the sum of the dice being {number} on a roll:")
        print(f"{calculator.pertantage_chance_of_num(number, decimal_digits=5)}, {calculator.count_of_num(number)} in {calculator.possible_permutations}")
        print()

class DiceCalculator:
    """
    I got a bit carried away with this class. So many abstractions....
    """
    def __init__(self, sides: int, count: int) -> None:
        self.sides = sides
        self.count = count
    
    def count_of_num(self, x: int) -> int:
        if not self.is_in_range(x):
            return 0
        
        # https://www.desmos.com/calculator/mz5n5venip
        most_common_nums = self.most_common_nums()
        
        nearest_mean = most_common_nums[len(most_common_nums) and most_common_nums[0] > ] 
        
        return nearest_mean - abs(x - nearest_mean) * (self.count - 1)
        
    def probability_of_num(self, x: int) -> float:
        """
        probability of roling x
        """
        if not self.is_in_range(x):
            return 0
        return self.count_of_num(x) / self.possible_permutations
        
    def pertantage_chance_of_num(self, x: int, *, decimal_digits = 3) -> str:
        """
        percentage chance of roling x
        """
        chance = self.probability_of_num(x)*100
        return str(round(chance, decimal_digits)) + "%"

    def most_common_nums(self) -> tuple[int, ...]:
        """
        returns the most common final sums of numbers
        """
        if self.mean % 1 == 0.5:
            return (int(self.mean - 0.5), int(self.mean + 0.5))
        return (int(self.mean),)

    def is_in_range(self, x) -> bool:
        return self.min <= x <= self.max

    @property
    def mean(self) -> float:
        return (self.min + self.max) / 2

    @property
    def median(self) -> float:
        return self.sides + 1 / self.count
        
    @property
    def min(self) -> int:
        """
        smallest possible number
        """
        return self.count
    
    @property
    def max(self) -> int:
        """
        largest possible number
        """
        return self.count * self.sides

    @property
    def range_size(self) -> int:
        """
        number of final answers
        """
        return self.max - self.min

    @property
    def possible_permutations(self) -> int:
        """
        how many possible conbantions
        """
        return self.sides ** self.count

    def __str__(self) -> str:
        return f"{self.count} differnt {self.sides} sided di{'' if self.count < 2 else 'c'}e."
    
    def __repr__(self) -> str:
        return f"sides={self.sides}, count={self.count}"


if __name__ == "__main__":
    main()
