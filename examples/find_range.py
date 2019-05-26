import console
console.setup()

from simpio import get_integer


# Value representing positive infinity.
POSITIVE_INFINITY = float('inf')

# Value representing negative infinity.
NEGATIVE_INFINITY = float('-inf')

# Input that terminates the program.
SENTINEL = 0


def main():
    print("This program finds the largest and smallest numbers.")
    smallest, largest = POSITIVE_INFINITY, NEGATIVE_INFINITY

    # Loop until the user enters the SENTINEL value.
    while True:
        n = get_integer('?')
        if n == SENTINEL:
            break

        # Possibly update the running lowest or highest values.
        if n < smallest:
            smallest = n
        if n > largest:
            largest = n

    # The smallest and largest values will be set to their defaults values only
    # if the user has entered no non-sentinel values.
    if smallest == POSITIVE_INFINITY or largest == NEGATIVE_INFINITY:
        print('You must enter at least one value before the sentinel!')
    else:
        print('Smallest:', smallest)
        print('Largest:', largest)


if __name__ == '__main__':
    main()
