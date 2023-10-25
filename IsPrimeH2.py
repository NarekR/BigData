def is_prime(number):
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False

    #i = 6k-1
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True

def generate_primes(n):
    for i in range(1, n):
        if is_prime(i):
            yield i

n = int(input("Введите до сколки надо генерировать: "))

for prime in generate_primes(n):
    print(prime)

