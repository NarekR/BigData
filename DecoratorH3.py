import time

def is_prime(number):
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} выполнилась за {execution_time:.4f} секунд")
        return result
    return wrapper

# Пример использования декоратора:

@timing_decorator
def Is_PrimeTime(n):
   for i in range(1, n):
        if is_prime(i):
            print(i)

n = int(input("Введите до сколки надо шитать: "))
Is_PrimeTime(n)

