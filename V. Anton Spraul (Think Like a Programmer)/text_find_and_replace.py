"""
find and replace words problem from from https://youtu.be/4Gsy27337-g?t=69
"""

def find_and_replace(starting_text: str, old: str, new: str):
    # no built in funtions/methods allowd
    starting_text, old, new = list(starting_text), list(old), list(new)
    
    for start in range(len(starting_text)):
        end = start + len(old)
        if starting_text[start:end] == old:
            starting_text[start:end] = new

    return "".join(starting_text)

def main():
    starting_text = input("Enter starting text: ")

    old = input("Enter text you want to replace: ")
    new = input("Enter new text: ")

    print(find_and_replace(starting_text, old, new))

if __name__ == "__main__":
    main()