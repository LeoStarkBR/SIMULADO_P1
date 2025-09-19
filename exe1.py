#Exercício 1

# Implemente um sistema de transporte em Python utilizando classes abstratas:

#Crie uma classe abstrata Transporte com um atributo capacidade, um método abstrato mover() e um método concreto info() que exibe a capacidade.
#Crie duas subclasses:
#Carro, que imprime "O carro está se movendo com até X passageiros".
#Bicicleta, que imprime "A bicicleta está se movendo com até X pessoas".
#No programa principal, crie objetos das duas subclasses, adicione-os em uma lista e invoque mover() e info() para cada um.

from abc import ABC, abstractmethod

class transporte(ABC):
  @abstractmethod
  def mover(self):
    pass

  def __init__(self, capacidade = int, passageiros = int):
    self.capacidade = capacidade
    if self.capacidade <= 0:
      raise ValueError('Não pode haver numero negativos ou zero')
    pass
  
  def info(self):
     return f'O carro está se movendo com {self.capacidade} pessoas abordo! '

class carro(transporte):
  def mover(self):
    return f'O carro está se movendo com {self.capacidade} pessoas abordo! '

class bicicleta(transporte):
  def mover(self):
    return f'O Bicicleta está se movendo com {self.capacidade} pessoas abordo! '

#lista para guardar:
lista_transporte = []

#objeto 1
obj1 = carro(5)
obj1.mover()
lista_transporte.append(obj1)

#objeto 2
bike1 = bicicleta(2)
bike1.mover()
lista_transporte.append(bike1)