def search(number: int, lst: list) -> bool:
    first_index = 0
    last_index = len(lst) - 1

    while first_index <= last_index:
        middle_index = (first_index + last_index) // 2

        if lst[middle_index] == number:
            return True

        if number < lst[middle_index]:
            last_index = middle_index - 1
        else:
            first_index = middle_index + 1

    return False
