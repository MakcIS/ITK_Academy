nums = [2, 7, 11, 15]
target = int(input("Введите число: "))

result = []
for i in range(len(nums)):
    for j in range(i, len(nums)):
        if nums[i] + nums[j] == target:
            result.append([i, j])

if result:
    print(*result, sep="\n")
else:
    print(f"Нет элемнтов чья сумма равна {target}")
