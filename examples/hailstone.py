import console
console.setup()

from simpio import get_positive_int


def hailstone(n):
    steps = 0
    # Until n is equal to one:
    while n != 1:
        # If n is even, divide it by two.
        if n % 2 == 0:
            m = n // 2
            print('{} is even so I take half: {}'.format(n, m))
        # If n is odd, multiply it by three and add one.
        else:
            m = 3 * n + 1
            print('{} is odd, so I make 3n + 1: {}'.format(n, m))

        # Move to the next step in the hailstone sequence.
        n = m
        steps += 1
    return steps


if __name__ == '__main__':
    # Get a positive integer from the user.
    n = get_positive_int('Enter a number: ')

    # Compute the hailstone sequence starting at that number.
    steps = hailstone(n)
    print('The process took {} step(s) to reach 1'.format(steps))
