from abc import ABC, abstractmethod

class Transporte(ABC):
    def __init__(self, capacidade: int):
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser positiva")
        self.capacidade = capacidade

    @abstractmethod
    def mover(self) -> str:
        pass

    def info(self) -> str:
        return f"Capacidade: {self.capacidade}"


class Carro(Transporte):
    def mover(self) -> str:
        return f"O carro está se movendo com até {self.capacidade} passageiros"


class Bicicleta(Transporte):
    def mover(self) -> str:
        return f"A bicicleta está se movendo com até {self.capacidade} pessoas"


if __name__ == "__main__":
    transportes = [Carro(5), Bicicleta(2)]

    for t in transportes:
        print(t.mover())
        print(t.info())
