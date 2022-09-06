from runner import run, welcome

ROUND_TO = False

def main():
    # TODO problem when there is highest and lowest role

    welcome("dice chance calculator")

    dice_sides = int(input("How many sides does the dice have: ").removeprefix("d").strip())
    num_of_dice = int(input("How many dice do you want: ").strip())

    print()

    if 0 in (dice_sides, num_of_dice):
        print("No roles will be possible")
        return

    calculator = DiceCalculator(sides=dice_sides, count=num_of_dice)
    
    most_common_nums = calculator.most_common_nums()

    print(f"There are {calculator.possible_outcomes} possible roles that are between {calculator.min} and {calculator.max}.")
    if len(most_common_nums) == 2:
        print(f"The most likely roles are either a {most_common_nums[0]} or a {most_common_nums[1]}.")
    else:
        print(f"The most likely role is a {most_common_nums[0]}.")

    def percent_chance(user_number):
        percent_chance = calculator.pertantage_chance_of_num(user_number)
        return f"{percent_chance} chance of the sum of the dice being {user_number} on a roll"

    run(percent_chance, ("Enter your number", (int, "input must be a number")))

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

        most_common_nums = self.most_common_nums()
        if len(most_common_nums) == 1:
            low_num = high_num = most_common_nums[0]
        else:
            low_num, high_num = most_common_nums

        if x < self.mean:
            count = (x+low_num)-low_num-1
        else:
            count = (x+high_num)-high_num-1
        return count
        
    def probability_of_num(self, x: int) -> float:
        """
        probability of roling x
        """
        if not self.is_in_range(x):
            return 0
        return self.count_of_num(x) / self.possible_outcomes
        
    def pertantage_chance_of_num(self, x: int, / , round_to=ROUND_TO) -> str:
        """
        percentage chance of roling x
        """
        chance = self.probability_of_num(x)*100
        if round_to is not False:
            chance = round(chance, round_to)
        return str(chance) + "%"

    def most_common_nums(self) -> tuple[int, ...]:
        """
        returns the most common final sums of numbers
        """
        if self.mean % 1 == 0.5:
            return (self.median, self.median+1)
        return (self.median, )

    def is_in_range(self, x) -> bool:
        return self.min < x < self.max

    @property
    def mean(self) -> float:
        return (self.min + self.max) / 2

    @property
    def median(self) -> int:
        return int(self.mean)

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
    def range(self) -> int:
        """
        number of final answers
        """
        return self.max - self.min

    @property
    def possible_outcomes(self) -> int:
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
