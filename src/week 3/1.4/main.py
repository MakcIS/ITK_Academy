nums = [10, 9, 2, 5, 3, 7, 101, 18]

seqs = [[]]

for i in range(len(nums)):
    seqs[-1].append(nums[i])
    try:
        if nums[i] > nums[i + 1]:
            seqs.append([])
    except IndexError:
        pass

res = max(seqs, key=len)

print(len(res), res)
