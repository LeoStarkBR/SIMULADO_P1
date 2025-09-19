from exe1 import *
import pytest

def test_entrada_quantidade():
  ob1 = carro(5)
  assert ob1.capacidade == 5

def test_entrada_negativa():
    with pytest.raises(ValueError):
       obj2 = carro(-1)

def test_string_bike():
   ob2 = bicicleta(2)
   assert ob2.mover() == f'O Bicicleta está se movendo com {2} pessoas abordo! '

def test_string_carro():
   ob3 = carro(5)
   assert ob3.mover() == f'O carro está se movendo com {5} pessoas abordo! '