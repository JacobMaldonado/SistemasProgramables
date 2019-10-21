x = int(input('Asigne el numero de factorial a calcular -> '))
factorial = 1
while x > 0:
    factorial *= x
    x -= 1
print(factorial)