"""
Problem from https://www.youtube.com/watch?v=2bkfA2fHVwg&t=360s

Department numbers:

- Fire
- Police
- Sanitation

Each assigned a number from 1 to 7
All department # must be different
Sum of all # must be 12
Police cannot be odd

Display all valid department numbers permuations
"""
from collections import namedtuple
from itertools import permutations

department_vals = namedtuple("departments", ("Fire", "Police", "Sanitation"))

def department_numbers_permuations(min_num, max_num, required_sum = None, *, special_conditions = None):
    # get all permutaions of vals
    all_deparment_vals = permutations(range(min_num, max_num+1), len(department_vals._fields))

    # convert to our named tuple
    all_deparment_vals = map(lambda val: department_vals(*val), all_deparment_vals)

    if required_sum is not None:
        # just get conbantions where sum = the required sum
        all_deparment_vals = filter(lambda val: sum(val) == required_sum, all_deparment_vals)

    if special_conditions:
        for special_condition in special_conditions:
            all_deparment_vals = filter(special_condition, all_deparment_vals)

    return all_deparment_vals

def main() -> None:
    MIN_NUM = 1
    MAX_NUM = 7

    REQUIRED_SUM = 12 

    valid_department_numbers_permuations = department_numbers_permuations(MIN_NUM, MAX_NUM, REQUIRED_SUM, special_conditions=[lambda val: val.Police % 2 == 0])
    for ans in valid_department_numbers_permuations:
        print(ans)

if __name__ == "__main__":
    main()