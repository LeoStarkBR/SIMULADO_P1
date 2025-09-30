# Questões Clássicas Resolvidas

Cada seção traz um enunciado inspirado em provas e entrevistas técnicas, seguido por uma resolução completa. Os exemplos usam apenas recursos abordados nos seus materiais de estudo: classes e objetos, herança, classes abstratas, decorators e testes unitários com `pytest`.

---

## OO01 — Cadastro de Produtos com Encapsulamento

**Enunciado.** Modele um sistema simples de estoque composto por uma classe `Produto` com os atributos privados `_codigo`, `_descricao`, `_preco` e `_quantidade`. A classe deve expor:

- Propriedades `descricao` e `preco` com validação (descrição não pode ser vazia; preço precisa ser positivo).
- Método `atualizar_estoque(quantidade)` que aceita valores positivos ou negativos, impedindo que o estoque final fique negativo.
- Método de classe `criar_promocional(cls, codigo, descricao, preco)` que cria um produto com desconto de 20% e quantidade inicial zero.

Implemente uma função `resumo_produto(produto)` que retorne uma string formatada com os dados do produto.

**Resolução.**

```python
class Produto:
    DESCONTO_PROMOCIONAL = 0.20

    def __init__(self, codigo: str, descricao: str, preco: float, quantidade: int = 0):
        self._codigo = codigo
        self.descricao = descricao
        self.preco = preco
        self._quantidade = quantidade

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        valor = valor.strip()
        if not valor:
            raise ValueError('A descrição não pode ser vazia')
        self._descricao = valor

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
            raise ValueError('Estoque insuficiente para a operação')
        self._quantidade = novo_total

    @classmethod
    def criar_promocional(cls, codigo: str, descricao: str, preco: float) -> 'Produto':
        preco_com_desconto = preco * (1 - cls.DESCONTO_PROMOCIONAL)
        return cls(codigo, descricao, preco_com_desconto, quantidade=0)


def resumo_produto(produto: Produto) -> str:
    return (
        f"Produto {produto.descricao} (código {produto._codigo}) — "
        f"Preço: R$ {produto.preco:.2f}, Estoque: {produto.quantidade} unidade(s)"
    )
```

**Por que funciona.** O encapsulamento com `@property` garante validação centralizada. O uso de `@classmethod` mantém a lógica promocional dentro da própria classe.

---

## OO02 — Folha de Pagamento com Classe Abstrata

**Enunciado.** Construa uma hierarquia de funcionários onde `Funcionario` é uma classe abstrata com atributos `nome` e `base_salario`. Ela expõe o método concreto `folha_pagamento()` que retorna o salário líquido calculado por `self.calcular_salario()`. Crie duas subclasses:

- `FuncionarioCLT` com benefícios de 15% e adicional de 300 reais por dependente.
- `FuncionarioPJ` com bônus variável definido via parâmetro no construtor.

Apresente o uso das classes percorrendo uma lista heterogênea e imprimindo a folha de pagamento de cada funcionário.

**Resolução.**

```python
from abc import ABC, abstractmethod
from typing import List

class Funcionario(ABC):
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
            self.base_salario
            * (1 + self.BENEFICIO)
            + self.ADICIONAL_DEPENDENTE * self.dependentes
        )


class FuncionarioPJ(Funcionario):
    def __init__(self, nome: str, base_salario: float, bonus: float = 0.0) -> None:
        super().__init__(nome, base_salario)
        self.bonus = bonus

    def calcular_salario(self) -> float:
        return self.base_salario + self.bonus


def demonstrar_folha(funcionarios: List[Funcionario]) -> None:
    for funcionario in funcionarios:
        print(funcionario.folha_pagamento())
        print('-' * 40)
```

**Por que funciona.** O método `folha_pagamento` vive na classe base e delega o cálculo às subclasses via polimorfismo, evitando condicionais espalhadas no código principal.

---

## OO03 — Sistema de Biblioteca com Polimorfismo

**Enunciado.** Modele um sistema que registre diferentes tipos de materiais: livros físicos, e-books e revistas. Todos herdam de `MaterialBiblioteca`, que define os atributos `titulo` e `autor` e um método abstrato `descricao()`. Requisitos extras:

- `LivroFisico` possui atributo `paginas` e devolve descrição com número de páginas.
- `Ebook` possui atributo `tamanho_mb`.
- `Revista` possui atributo `edicao` e método adicional `resumo_edicao()`.
- Crie uma função `listar_materiais(materiais)` que percorre qualquer lista de materiais e chama `descricao()`.

**Resolução.**

```python
from abc import ABC, abstractmethod


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


def listar_materiais(materiais: list[MaterialBiblioteca]) -> None:
    for material in materiais:
        print(material.descricao())
```

**Por que funciona.** A função `listar_materiais` depende apenas do contrato da classe base (`descricao`), ilustrando polimorfismo em listas heterogêneas sem condicionais.

---

## DEC01 — Decorator de Auditoria com Parâmetros

**Enunciado.** Implemente um decorator parametrizado `auditar(acao)` que registre logs no formato `[AUDITORIA] Ação=<acao>; Função=<nome>; Args=<args>; Kwargs=<kwargs>`. O decorator deve envolver a função original sem alterar a assinatura e retornar o resultado normalmente. Demonstre em funções `criar_usuario` e `excluir_usuario`.

**Resolução.**

```python
from functools import wraps
from typing import Callable

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
```

**Por que funciona.** O uso de `@wraps` preserva metadados da função original. O decorator aceita parâmetros ao encapsular mais um nível de função (`decorator`).

---

## DEC02 — Decorator de Cache Simples

**Enunciado.** Crie um decorator `cache_resultado` que memorize o retorno das chamadas de uma função cara (`calcular_distancia`) baseada em todos os argumentos posicionais e nomeados. Se a combinação já tiver sido computada, retorne o valor em cache sem recalcular.

**Resolução.**

```python
from functools import wraps

def cache_resultado(func):
    cache = {}

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
```

**Por que funciona.** O cache usa uma chave imutável com os argumentos ordenados, garantindo reutilização de resultados independentemente da ordem dos argumentos nomeados.

---

## TEST01 — Testes Unitários para Calculadora

**Enunciado.** Dada a classe `Calculadora` abaixo, escreva testes `pytest` que cubram operações válidas e cenários de exceção.

```python
class Calculadora:
    def somar(self, a, b):
        return a + b

    def dividir(self, a, b):
        if b == 0:
            raise ZeroDivisionError('Divisão por zero não é permitida')
        return a / b
```

Os testes devem validar: soma de inteiros e floats, divisão com números positivos e negativos, divisão por zero e tipos inválidos (strings).

**Resolução.**

```python
import pytest

class TestCalculadora:
    @pytest.fixture
    def calculadora(self):
        return Calculadora()

    @pytest.mark.parametrize('a, b, esperado', [
        (2, 3, 5),
        (-1, 4, 3),
        (2.5, 1.5, 4.0),
    ])
    def test_somar(self, calculadora, a, b, esperado):
        assert calculadora.somar(a, b) == esperado

    @pytest.mark.parametrize('a, b, esperado', [
        (10, 2, 5),
        (-10, 2, -5),
        (7.5, 2.5, 3.0),
    ])
    def test_dividir(self, calculadora, a, b, esperado):
        assert calculadora.dividir(a, b) == esperado

    def test_dividir_por_zero(self, calculadora):
        with pytest.raises(ZeroDivisionError):
            calculadora.dividir(10, 0)

    def test_dividir_com_tipo_invalido(self, calculadora):
        with pytest.raises(TypeError):
            calculadora.dividir('10', 2)
```

**Por que funciona.** A combinação de fixtures com `parametrize` reduz repetição de código e cobre cenários variados.

---

## TEST02 — Testando Serviços com Fixtures

**Enunciado.** Considere um `RepositorioClientes` com métodos `adicionar(cliente)` e `buscar_email(cliente_id)`. Escreva testes com fixtures que garantam isolamento entre os casos e cobrem tentativas de busca inválidas.

**Resolução.**

```python
import pytest


class RepositorioClientes:
    def __init__(self):
        self._clientes = {}

    def adicionar(self, cliente_id: int, email: str) -> None:
        self._clientes[cliente_id] = email

    def buscar_email(self, cliente_id: int) -> str:
        if cliente_id not in self._clientes:
            raise KeyError('Cliente não encontrado')
        return self._clientes[cliente_id]


def test_repositorio_deve_guardar_clientes():
    repo = RepositorioClientes()
    repo.adicionar(1, 'alice@example.com')

    assert repo.buscar_email(1) == 'alice@example.com'


def test_repositorio_raise_para_ids_inexistentes():
    repo = RepositorioClientes()

    with pytest.raises(KeyError):
        repo.buscar_email(99)
```

**Por que funciona.** Cada teste instancia um repositório separado, evitando interferência entre cenários. O uso de `KeyError` reforça boas práticas para coleções.

---

## DDD01 — Modelagem de Pedidos

**Enunciado.** Modele o domínio de pedidos de uma loja online seguindo os conceitos básicos de DDD:

- `Cliente` como entidade com identidade (`cliente_id`).
- `EnderecoEntrega` como objeto de valor imutável.
- `ItemPedido` como objeto de valor com `produto_id`, `quantidade` e `preco_unitario`.
- `Pedido` como raiz de agregado contendo itens e responsável por garantir que o total nunca seja negativo.

Implemente métodos `adicionar_item`, `total` e `alterar_endereco` (substituindo o endereço por outro objeto de valor).

**Resolução.**

```python
from dataclasses import dataclass
from decimal import Decimal
from typing import List

@dataclass(frozen=True)
class EnderecoEntrega:
    rua: str
    numero: str
    cidade: str
    estado: str
    cep: str

    def __post_init__(self):
        if not all([self.rua.strip(), self.numero.strip(), self.cidade.strip(), self.estado.strip(), self.cep.strip()]):
            raise ValueError('Todos os campos do endereço são obrigatórios')

@dataclass(frozen=True)
class Cliente:
    cliente_id: str
    nome: str


@dataclass(frozen=True)
class ItemPedido:
    produto_id: str
    quantidade: int
    preco_unitario: Decimal

    def __post_init__(self):
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
```

**Por que funciona.** Os objetos de valor (`EnderecoEntrega`, `ItemPedido`) são imutáveis, reforçando invariantes. A `Pedido` mantém o agregado consistente e concentra as regras de negócio.

---

## Próximos Passos

- Reimplemente os exercícios modificando requisitos (ex.: adicionar descontos progressivos, políticas de frete, validações extras).
- Transforme as soluções em testes unitários adicionais para checar regressões ao evoluir o código.
- Combine decorators com classes abstratas para criar soluções híbridas (ex.: validação automática de formulários).
