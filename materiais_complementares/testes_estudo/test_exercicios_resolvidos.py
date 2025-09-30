from decimal import Decimal

import pytest

from materiais_complementares import exercicios_resolvidos as er


def test_produto_promocional_valida_desconto_e_estoque():
    produto = er.Produto.criar_promocional('P01', 'Teclado', 200.0)
    assert produto.preco == pytest.approx(160.0)

    produto.atualizar_estoque(5)
    assert produto.quantidade == 5

    with pytest.raises(ValueError):
        produto.atualizar_estoque(-10)


def test_funcionarios_calculam_salario_de_forma_polimorfica():
    funcionarios = [
        er.FuncionarioCLT('Ana', 3000.0, dependentes=2),
        er.FuncionarioPJ('Bruno', 4500.0, bonus=500.0),
    ]
    folhas = er.demonstrar_folha(funcionarios)

    assert 'Ana' in folhas[0]
    assert 'Bruno' in folhas[1]
    assert folhas[0] != folhas[1]


def test_listar_materiais_polimorfismo():
    materiais = [
        er.LivroFisico('Clean Code', 'Robert Martin', 464),
        er.Ebook('Fluent Python', 'Luciano Ramalho', 6.2),
        er.Revista('Python Monthly', 'Equipe', '2024-09'),
    ]
    descricoes = er.listar_materiais(materiais)

    assert "Livro físico" in descricoes[0]
    assert "E-book" in descricoes[1]
    assert "Revista" in descricoes[2]


def test_cache_resultado_evita_recalculo(monkeypatch):
    contador = {'executou': 0}

    @er.cache_resultado
    def func(x):
        contador['executou'] += 1
        return x * 2

    assert func(10) == 20
    assert func(10) == 20
    assert contador['executou'] == 1


def test_pedido_total_com_itens():
    pedido = er.Pedido(
        'P123',
        er.Cliente('C1', 'Alice'),
        er.EnderecoEntrega('Rua A', '1', 'Cidade', 'SP', '00000-000'),
    )
    pedido.adicionar_item(er.ItemPedido('SKU1', 2, Decimal('50.00')))
    pedido.adicionar_item(er.ItemPedido('SKU2', 1, Decimal('100.00')))

    assert pedido.total() == Decimal('200.00')


def test_repositorio_clientes_erro_para_id_inexistente():
    repo = er.RepositorioClientes()
    with pytest.raises(KeyError):
        repo.buscar_email(999)
