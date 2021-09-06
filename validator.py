def val(message):

    # if the question requires a Y/N answer
    if message[-5:] == "(Y/N)":
        while True:
            _b = input(message).upper()  # it's ok for users to enter lowercase letters
            if _b not in ("Y", "N"):
                print("Please enter Y or N.")
                continue
            else:
                return _b

    # if the question asks for a natural number
    else:
        while True:
            try:
                _n = int(input(message))
                if _n < 1:
                    print("Please enter a natural number.")
                    continue
                else:
                    return _n
            except ValueError:
                print("Please enter a natural number.")
                continue

if __name__ == "__main__":
    val()