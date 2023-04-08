import encoder


def main():
    operation = input("Encode or decode? (e/D): ")
    if operation.lower() == "e":
        encoder.main()
    elif operation.lower() == "d":
        pass
    else:
        raise TypeError("Non valid operation type")


if __name__ == '__main__':
    main()
