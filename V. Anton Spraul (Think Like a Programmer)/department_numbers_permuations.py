"""
Department numbers problem from https://youtu.be/2bkfA2fHVwg?t=360:

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

MIN_NUM = 1
MAX_NUM = 7

REQUIRED_SUM = 12

DEPARTMENTS = ["Fire", "Police", "Sanitation"] 

def department_numbers_permuations_simple(department_vals):
    for fire in range(8):
        for police in range(0, 8, 2): # to only get even
            for sanitation in range(8):
                if fire != police and fire != sanitation and sanitation != police:
                    yield department_vals(fire, police, sanitation)

from itertools import permutations
def department_numbers_permuations_genral_purpose(department_vals, min_num, max_num, required_sum = None, *, special_conditions = None):
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
    department_vals = namedtuple("departments", DEPARTMENTS)

    valid_department_numbers_permuations = department_numbers_permuations_genral_purpose(department_vals, MIN_NUM, MAX_NUM, REQUIRED_SUM, special_conditions=[lambda val: val.Police % 2 == 0])
    # valid_department_numbers_permuations = department_numbers_permuations_simple(department_vals)

    for ans in valid_department_numbers_permuations:
        print(", ".join(f"{name}: #{num}" for name, num in zip(department_vals._fields, ans)))

if __name__ == "__main__":
    main()