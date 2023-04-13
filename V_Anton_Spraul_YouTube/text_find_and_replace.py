"""
find and replace words problem from https://youtu.be/4Gsy27337-g?t=69

Must work with punctuation.

cat should not match catalog, concatanation, ect
"""

def split_words(text):
    words = []

    current = ""
    start = 0
    for i, char in enumerate(text+" "):
        if char.isalpha():
            current += char.lower()
        else:
            if current:
                words.append((current, (start, start+len(current))))
            current = ""
            start = i+1

    return words

def find_and_replace(starting_text: str, old: str, new: str):
    lower_old = old.lower()


    split_text = split_words(starting_text)

    list_text = list(starting_text)
    for word, (start, end) in split_text:
        if word == lower_old:
            list_text[start:end] = new

    return "".join(list_text)

def main():
    starting_text = input("Enter starting text: ")

    old = input("Enter text you want to replace: ")
    new = input("Enter new text: ")

    print(find_and_replace(starting_text, old, new))

if __name__ == "__main__":
    main()