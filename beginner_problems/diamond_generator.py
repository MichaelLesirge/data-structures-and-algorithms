FULL_CHAR = "#"
BLACK_CHAR = " "

def create_diamond(edge_height, full_char="#", blank_char=" ") -> str:
    final = []

    for i in range(edge_height):
        final.append((blank_char * ((edge_height - i) - 1)) + (full_char * ((i * 2) + 1)))
    final.extend(reversed(final[:-1]))

    return "\n".join(final)


def main():
    print("Welcome to the the diamond pattern generator!")

    while True:
        print()

        edge_size = int(input("Enter edge height of diamond: "))

        print()
        print(create_diamond(edge_size))

if __name__ == "__main__":
    main()
