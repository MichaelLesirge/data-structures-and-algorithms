FULL_CHAR = "#"
BLACK_CHAR = " "

def create_diamond(edge_height, full_char="#", blank_char=" ") -> str:
    final = []

    for i in range(edge_height):
        final.append((blank_char * ((edge_height - i) - 1)) + (full_char * ((i * 2) + 1)))
    final.extend(reversed(final[:-1]))

    return "\n".join(final)


def main():
    from runner import run
    run(create_diamond, [("Enter edge height of diamond", (int, "input most be a number"))], output_label=None)

if __name__ == "__main__":
    main()
