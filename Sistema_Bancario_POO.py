from datetime import datetime
from abc import ABC, abstractmethod

# Classe base para clientes do banco
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []  # Lista de contas associadas ao cliente

    def adicionar_conta(self, conta):
        self.contas.append(conta)  # Adiciona uma conta ao cliente

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)  # Realiza uma transação (depósito/saque) na conta informada

# Classe para clientes do tipo pessoa física
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe base para contas bancárias
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()  # Histórico de transações

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)  # Cria uma nova conta para o cliente

    @property
    def saldo(self):  # Retorna saldo atual da conta
        return self._saldo

    @property
    def numero(self):  # Retorna número da conta
        return self._numero

    @property
    def agencia(self):  # Retorna número da agência
        return self._agencia

    @property
    def cliente(self):  # Retorna o titular da conta
        return self._cliente

    @property
    def historico(self):  # Retorna o histórico de transações
        return self._historico

    def sacar(self, valor):
        # Verifica se há saldo suficiente para sacar
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False
        if valor <= 0:
            print("Valor inválido.")
            return False
        self._saldo -= valor
        print("Saque realizado!")
        return True

    def depositar(self, valor):
        # Realiza um depósito se o valor for válido
        if valor <= 0:
            print("Valor inválido.")
            return False
        self._saldo += valor
        print("Depósito realizado!")
        return True

# Classe para contas correntes, com limite e limite de saques
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        # Conta o número de saques já realizados
        num_saques = len([t for t in self.historico.transacoes if t["tipo"] == "Saque"])
        # Verifica se excedeu o limite de valor ou o número de saques
        if valor > self.limite:
            print("Limite excedido.")
            return False
        if num_saques >= self.limite_saques:
            print("Máximo de saques atingido.")
            return False
        return super().sacar(valor)

    def __str__(self):
        return f"Agência: {self.agencia}\nConta: {self.numero}\nTitular: {self.cliente.nome}"

# Classe que registra o histórico de transações da conta
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):  # Retorna lista de transações
        return self._transacoes

    def adicionar_transacao(self, transacao):
        # Adiciona uma transação ao histórico com data/hora
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%y %H:%M:%S"),
        })

# Classe abstrata para operações bancárias (Saque/Depósito)
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):  # Retorna o valor da transação
        pass

    @abstractmethod
    def registrar(self, conta):  # Realiza e registra a transação na conta
        pass

# Classe para operação de saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        # Realiza o saque e registra se for bem-sucedido
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

# Classe para operação de depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        # Realiza o depósito e registra se for bem-sucedido
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

# Função para criar um novo cliente
def criar_cliente(clientes):
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento: ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("Cliente criado!")

# Função para criar uma nova conta para um cliente já cadastrado
def criar_conta(numero, clientes, contas):
    cpf = input("CPF do titular: ")
    cliente = next((c for c in clientes if isinstance(c, PessoaFisica) and c.cpf == cpf), None)
    if not cliente:
        print("Cliente não encontrado.")
        return
    conta = ContaCorrente(numero, cliente)
    cliente.adicionar_conta(conta)
    contas.append(conta)
    print("Conta criada!")

# Lista todas as contas cadastradas
def listar_contas(contas):
    for conta in contas:
        print("="*20)
        print(conta)

# Realiza um depósito em uma conta existente
def realizar_deposito(contas):
    numero = int(input("Número da conta: "))
    conta = next((c for c in contas if c.numero == numero), None)
    if not conta:
        print("Conta não encontrada.")
        return
    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)
    conta.cliente.realizar_transacao(conta, transacao)

# Realiza um saque em uma conta existente
def realizar_saque(contas):
    numero = int(input("Número da conta: "))
    conta = next((c for c in contas if c.numero == numero), None)
    if not conta:
        print("Conta não encontrada.")
        return
    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)
    conta.cliente.realizar_transacao(conta, transacao)

# Mostra o extrato de uma conta
def mostrar_extrato(contas):
    numero = int(input("Número da conta: "))
    conta = next((c for c in contas if c.numero == numero), None)
    if not conta:
        print("Conta não encontrada.")
        return
    print(f"Extrato da conta {conta.numero}:")
    for t in conta.historico.transacoes:
        print(f"{t['data']}: {t['tipo']} de R$ {t['valor']:.2f}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")

# Mostra o menu do sistema
def menu():
    print('-' * 30)
    print('MENU BANCÁRIO'.center(30))
    print('-' * 30)
    print('''[1] Depósito
[2] Saque
[3] Extrato
[4] Novo Cliente
[5] Nova Conta
[6] Lista de Contas
[7] Sair''')
    return input("Escolha uma opção: ")

# Função principal do programa
def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()
        if opcao == "1":
            realizar_deposito(contas)
        elif opcao == "2":
            realizar_saque(contas)
        elif opcao == "3":
            mostrar_extrato(contas)
        elif opcao == "4":
            criar_cliente(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            print('Saindo do sistema. Obrigado!')
            break
        else:
            print('Opção inválida. Tente novamente.')

# Executa o programa, se for o arquivo principal
if __name__ == "__main__":
    main()