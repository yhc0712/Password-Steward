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


def pw_len_check(length: int, combination: list):
    _ct = 0
    for i in combination:
        if i == "Y":
            _ct +=1
    if _ct > length:
        print('Impossible combination. Please amend your answer.')
        return 'again'
    else:
        return None


def determinator(dictionary: dict, length_needed_to_assign: int):
    from random import randint
    # _it_times to maintain the times the iteration has run
    _it_times = 0
    for key in dictionary:
        # run if == True if it is the ultimate time this iteration runs
        # the logic is different from the previous runs to make sure that the numbers assigned equal to the initial length_needed_to_assign
        if _it_times == len(dictionary) - 1:
            dictionary[key] += length_needed_to_assign
        else:
            _temp_num = randint(0, length_needed_to_assign)
            dictionary[key] += _temp_num
            length_needed_to_assign -= _temp_num
            _it_times += 1
    return dictionary


def generator(dictionary: dict):
    from random import choices, sample
    import string

    _string_dict = {
        'num' : string.digits,
        'upl' : string.ascii_uppercase,
        'lwl' : string.ascii_lowercase,
        'sym' : string.punctuation
    }

    _selection = []

    for key in dictionary:
        _temp_select = choices(_string_dict[key], k = dictionary[key])
        for i in _temp_select:
            _selection.append(i)
    
    pw = ''.join(sample(_selection, k = len(_selection)))

    return pw


def _test():
    import doctest
    return doctest.testmod()

if __name__ == "__main__":
    _test()
