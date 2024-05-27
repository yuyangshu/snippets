from math import ceil, log

if __name__ == "__main__":
    initial = ceil(log(16, 2))

    for n in (224, 256, 257, 512, 16, 17, 32):
        terminal = ceil(log(n, 2))

        print(n, f"terminal: {terminal}")
        for i in map(lambda x : 2 ** x, range(initial, terminal)):
            print(i, end=' ')
        print()
