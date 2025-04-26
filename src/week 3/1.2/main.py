nums = [1, 1, 2, 2, 3, 4, 4, 5]
indx = 0

while True:
    try:
        if nums[indx] == nums[indx + 1]:
            nums.pop(indx + 1)
        else:
            indx += 1
    except IndexError:
        break


print(len(nums), nums)
