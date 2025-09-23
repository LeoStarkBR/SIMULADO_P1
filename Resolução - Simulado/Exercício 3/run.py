import math

def valida_positivo(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg < 0:
                raise ValueError("Todos os argumentos devem ser positivos")
        for arg in kwargs.values():
            if arg < 0:
                raise ValueError("Todos os argumentos devem ser positivos")
        return func(*args, **kwargs)
    return wrapper


@valida_positivo
def raiz_quadrada(x):
    return math.sqrt(x)


@valida_positivo
def divisao(a, b):
    return a / b


if __name__ == "__main__":
    print(raiz_quadrada(36))  
    print(divisao(12, 3))  

    try:
        print(raiz_quadrada(-25))
    except ValueError as e:
        print(f"Erro: {e}")

    try:
        print(divisao(8, -2))
    except ValueError as e:
        print(f"Erro: {e}")
