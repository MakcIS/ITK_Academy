import matplotlib.pyplot as plt

x = ["a", "b", "c"]
y = [1, 2, 3]

plt.bar(x, y, label="sdsd")

plt.title("Example")
plt.xlabel("x")
plt.ylabel("y")
plt.savefig("grafik.png")
