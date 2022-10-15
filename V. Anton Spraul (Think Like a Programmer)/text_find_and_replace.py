"""
find and replace words problem from from https://youtu.be/4Gsy27337-g?t=69

must work with punction.

cat should not match catalog, concatanation, ect
"""

def split_words(text):
    
    words = []
    current = ""

    for i, char in enumerate(text):
        if char == " ":
            words.append((current, (start, end)))
            current_word = []
            
        

    return words

def find_and_replace(starting_text: str, old: str, new: str):
    pass

    

def main():
    starting_text = input("Enter starting text: ")

    old = input("Enter text you want to replace: ")
    new = input("Enter new text: ")

    print(split_words(starting_text))
    # print(find_and_replace(starting_text, old, new))

if __name__ == "__main__":
    main()