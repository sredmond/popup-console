import console
console.setup()

# Number which starts the countdown.
COUNTDOWN_START = 10

# Text to print at lift off.
LIFTOFF_MESSAGE = "Lift off!"

if __name__ == '__main__':
    for time_remaining in range(COUNTDOWN_START, 0, -1):
        print(time_remaining)
    print(LIFTOFF_MESSAGE)
