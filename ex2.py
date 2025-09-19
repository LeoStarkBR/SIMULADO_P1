def valida_positivo(func):
    # wrapper é a função que vai "envolver" a função original
    def wrapper(*args, **kwargs):  # *args pega todos os argumentos posicionais, **kwargs pega os argumentos nomeados
        # Verifica todos os argumentos posicionais
        for arg in args:
              if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Todos os números devem ser positivos")
        
        # Verifica todos os argumentos nomeados (se existirem)
        for arg in kwargs.values():
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError("Todos os números devem ser positivos")
        
        return func(*args, **kwargs)  # Executa a função original se tudo estiver certo
    return wrapper

@valida_positivo
def raiz_quadrada(x):
    return x ** 0.5

@valida_positivo
def divisao(a, b):
    return a / b


print(raiz_quadrada(9))  
print(divisao(10, 2))  

