import pytest
from run import Carro, Bicicleta  

def test_carro_capacidade():
    carro = Carro(5)
    assert carro.capacidade == 5

def test_carro_mover():
    carro = Carro(5)
    assert carro.mover() == "O carro está se movendo com até 5 passageiros"

def test_bicicleta_mover():
    bike = Bicicleta(2)
    assert bike.mover() == "A bicicleta está se movendo com até 2 pessoas"

def test_carro_capacidade_negativa():
    with pytest.raises(ValueError):
        Carro(-3)
