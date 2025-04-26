s = "AAABBCCDDD"

a = [s[0], 1]
result = ""

for i in s[1:]:
    if i == a[0]:
        a[1] += 1
    else:
        result += a[0] + str(a[1])
        a = [i, 1]

print(result)
