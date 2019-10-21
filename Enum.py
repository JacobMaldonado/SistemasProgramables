lista = ["a","b",2222,"hola"]
def confor():
    for num,i in enumerate([1,2,3]):
        print(str(num) + " -> " + str(i) )
def conwhile(lis):
    i = 0
    while len(lis) > i:
        print(str(i) + " " + str(lis[i]))
        i += 1

while True:
    try:
        x = input("Dame un numero ")
        y = int(x)
        break
    except:
        print('otra vez')

confor()
conwhile(lista)