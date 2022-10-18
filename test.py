cont = ""
with open("bussindataset.txt", "r") as f:
    for line in f.read().splitlines():
        cont += line.split(" ")[1] + "\n"

print(cont)

with open('betterdataset.txt', 'w') as f:
    f.write(cont)
