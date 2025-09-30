"""Coleção de exemplos resolvidos para reforçar conceitos de OO, decorators e testes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from functools import wraps
from typing import Callable, Iterable, List, Tuple


class Produto:
    """Modelo simples de produto com encapsulamento e validação."""

    DESCONTO_PROMOCIONAL = 0.20

    def __init__(self, codigo: str, descricao: str, preco: float, quantidade: int = 0) -> None:
        self._codigo = codigo
        self.descricao = descricao
        self.preco = preco
        self._quantidade = quantidade

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        texto = valor.strip()
        if not texto:
            raise ValueError('A descrição não pode ser vazia')
        self._descricao = texto

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError('O preço deve ser positivo')
        self._preco = float(valor)

    @property
    def quantidade(self) -> int:
        return self._quantidade

    def atualizar_estoque(self, quantidade: int) -> None:
        novo_total = self._quantidade + quantidade
        if novo_total < 0:
            raise ValueError('Estoque insuficiente para a operação solicitada')
        self._quantidade = novo_total

    @classmethod
    def criar_promocional(cls, codigo: str, descricao: str, preco: float) -> 'Produto':
        preco_com_desconto = preco * (1 - cls.DESCONTO_PROMOCIONAL)
        return cls(codigo, descricao, preco_com_desconto, quantidade=0)

    def __repr__(self) -> str:  # útil para debugging durante os estudos
        return f"Produto(codigo={self._codigo!r}, descricao={self.descricao!r}, preco={self.preco:.2f}, quantidade={self.quantidade})"


def resumo_produto(produto: Produto) -> str:
    return (
        f"Produto {produto.descricao} (código {produto._codigo}) — "
        f"Preço: R$ {produto.preco:.2f}, Estoque: {produto.quantidade} unidade(s)"
    )


class Funcionario(ABC):
    """Classe base abstrata para demonstrar polimorfismo em folha de pagamento."""

    def __init__(self, nome: str, base_salario: float) -> None:
        if base_salario <= 0:
            raise ValueError('O salário base deve ser positivo')
        self.nome = nome
        self.base_salario = base_salario

    @abstractmethod
    def calcular_salario(self) -> float:
        ...

    def folha_pagamento(self) -> str:
        salario = self.calcular_salario()
        return f"Funcionário: {self.nome}\nSalário líquido: R$ {salario:.2f}"


class FuncionarioCLT(Funcionario):
    BENEFICIO = 0.15
    ADICIONAL_DEPENDENTE = 300

    def __init__(self, nome: str, base_salario: float, dependentes: int = 0) -> None:
        super().__init__(nome, base_salario)
        self.dependentes = dependentes

    def calcular_salario(self) -> float:
        return (
            self.base_salario * (1 + self.BENEFICIO)
            + self.ADICIONAL_DEPENDENTE * self.dependentes
        )


class FuncionarioPJ(Funcionario):
    def __init__(self, nome: str, base_salario: float, bonus: float = 0.0) -> None:
        super().__init__(nome, base_salario)
        self.bonus = bonus

    def calcular_salario(self) -> float:
        return self.base_salario + self.bonus


def demonstrar_folha(funcionarios: Iterable[Funcionario]) -> List[str]:
    return [funcionario.folha_pagamento() for funcionario in funcionarios]


class MaterialBiblioteca(ABC):
    def __init__(self, titulo: str, autor: str) -> None:
        self.titulo = titulo
        self.autor = autor

    @abstractmethod
    def descricao(self) -> str:
        ...


class LivroFisico(MaterialBiblioteca):
    def __init__(self, titulo: str, autor: str, paginas: int) -> None:
        super().__init__(titulo, autor)
        self.paginas = paginas

    def descricao(self) -> str:
        return f"Livro físico: '{self.titulo}' por {self.autor} ({self.paginas} páginas)"


class Ebook(MaterialBiblioteca):
    def __init__(self, titulo: str, autor: str, tamanho_mb: float) -> None:
        super().__init__(titulo, autor)
        self.tamanho_mb = tamanho_mb

    def descricao(self) -> str:
        return f"E-book: '{self.titulo}' por {self.autor} ({self.tamanho_mb:.1f} MB)"


class Revista(MaterialBiblioteca):
    def __init__(self, titulo: str, autor: str, edicao: str) -> None:
        super().__init__(titulo, autor)
        self.edicao = edicao

    def descricao(self) -> str:
        return f"Revista: '{self.titulo}' edição {self.edicao}"

    def resumo_edicao(self) -> str:
        return f"Resumo da edição {self.edicao} da revista '{self.titulo}'"


def listar_materiais(materiais: Iterable[MaterialBiblioteca]) -> List[str]:
    return [material.descricao() for material in materiais]


def auditar(acao: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[AUDITORIA] Ação={acao}; Função={func.__name__}; Args={args}; Kwargs={kwargs}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@auditar('CRIACAO')
def criar_usuario(nome: str, email: str) -> dict:
    return {'nome': nome, 'email': email}


@auditar('EXCLUSAO')
def excluir_usuario(usuario_id: int) -> bool:
    return True


def cache_resultado(func: Callable) -> Callable:
    cache: dict[Tuple, object] = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        chave = args + tuple(sorted(kwargs.items()))
        if chave not in cache:
            cache[chave] = func(*args, **kwargs)
        return cache[chave]

    return wrapper


@cache_resultado
def calcular_distancia(ponto_a: tuple[int, int], ponto_b: tuple[int, int]) -> float:
    print('Executando cálculo pesado...')
    return ((ponto_a[0] - ponto_b[0]) ** 2 + (ponto_a[1] - ponto_b[1]) ** 2) ** 0.5


class Calculadora:
    def somar(self, a, b):
        return a + b

    def dividir(self, a, b):
        if b == 0:
            raise ZeroDivisionError('Divisão por zero não é permitida')
        return a / b


class RepositorioClientes:
    def __init__(self) -> None:
        self._clientes: dict[int, str] = {}

    def adicionar(self, cliente_id: int, email: str) -> None:
        self._clientes[cliente_id] = email

    def buscar_email(self, cliente_id: int) -> str:
        if cliente_id not in self._clientes:
            raise KeyError('Cliente não encontrado')
        return self._clientes[cliente_id]


@dataclass(frozen=True)
class Cliente:
    cliente_id: str
    nome: str


@dataclass(frozen=True)
class EnderecoEntrega:
    rua: str
    numero: str
    cidade: str
    estado: str
    cep: str

    def __post_init__(self) -> None:
        if not all([self.rua.strip(), self.numero.strip(), self.cidade.strip(), self.estado.strip(), self.cep.strip()]):
            raise ValueError('Todos os campos do endereço são obrigatórios')


@dataclass(frozen=True)
class ItemPedido:
    produto_id: str
    quantidade: int
    preco_unitario: Decimal

    def __post_init__(self) -> None:
        if self.quantidade <= 0:
            raise ValueError('Quantidade deve ser positiva')
        if self.preco_unitario <= 0:
            raise ValueError('Preço unitário deve ser positivo')

    def subtotal(self) -> Decimal:
        return self.preco_unitario * self.quantidade


class Pedido:
    def __init__(self, pedido_id: str, cliente: Cliente, endereco: EnderecoEntrega) -> None:
        self.pedido_id = pedido_id
        self.cliente = cliente
        self._endereco = endereco
        self._itens: List[ItemPedido] = []

    @property
    def endereco(self) -> EnderecoEntrega:
        return self._endereco

    def alterar_endereco(self, novo_endereco: EnderecoEntrega) -> None:
        self._endereco = novo_endereco

    def adicionar_item(self, item: ItemPedido) -> None:
        self._itens.append(item)

    def total(self) -> Decimal:
        total = sum((item.subtotal() for item in self._itens), Decimal('0'))
        if total < 0:
            raise ValueError('Total inválido')
        return total

    def __repr__(self) -> str:
        return f"Pedido(id={self.pedido_id!r}, cliente={self.cliente.nome!r}, itens={len(self._itens)})"


def montar_pedido_exemplo() -> Pedido:
    cliente = Cliente(cliente_id='C001', nome='Alice')
    endereco = EnderecoEntrega('Rua das Flores', '10', 'Bauru', 'SP', '17000-000')
    pedido = Pedido('P0001', cliente, endereco)
    pedido.adicionar_item(ItemPedido('PENT', 2, Decimal('150.00')))
    pedido.adicionar_item(ItemPedido('CCHA', 1, Decimal('20.00')))
    return pedido


if __name__ == '__main__':
    # Demonstração rápida quando o arquivo é executado diretamente
    produto = Produto('001', 'Mouse', 120.0, 5)
    produto.atualizar_estoque(+3)
    print(resumo_produto(produto))

    funcionarios = [
        FuncionarioCLT('Bianca', 3000.0, dependentes=1),
        FuncionarioPJ('Carlos', 5500.0, bonus=700.0),
    ]
    for linha in demonstrar_folha(funcionarios):
        print(linha)
        print('-' * 20)

    materiais = [
        LivroFisico('Clean Code', 'Robert C. Martin', 464),
        Ebook('The Pragmatic Programmer', 'Andy Hunt', 5.5),
        Revista('Python Monthly', 'Equipe', '2024-10'),
    ]
    for descricao in listar_materiais(materiais):
        print(descricao)

    criar_usuario('João', 'joao@example.com')
    calcular_distancia((0, 0), (3, 4))
    calcular_distancia((0, 0), (3, 4))  # segunda chamada usa cache

    pedido = montar_pedido_exemplo()
    print(pedido)
    print(f'Total do pedido: R$ {pedido.total():.2f}')
