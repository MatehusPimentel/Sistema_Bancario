def menu():
    print('-' * 30)
    print('MENU BANCÁRIO'.center(30))
    print('-' * 30)
    print('''[1] Depósito
[2] Sacar
[3] Extrato
[4] Novo Usuário
[5] Nova Conta
[6] Lista de Contas
[7] Sair''')

def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R${valor:.2f}\n"
        print(f'Depósito de R${valor:.2f}\n--- realizado com sucesso ---')
    else:
        print('Valor inválido para depósito.')
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    limite_do_saldo = valor > saldo
    limite_do_limite = valor > limite
    limite_do_saques = numero_saques >= limite_saques

    if limite_do_saldo:
        print('Erro na operação: você não possui saldo suficiente.')
    elif limite_do_limite:
        print('Erro na operação: você não pode sacar mais que o limite de R$500.')
    elif limite_do_saques:
        print('Erro na operação: você não pode sacar mais que o limite de saques diários.')
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:    R${valor:.2f}\n"
        numero_saques += 1
        print(f'O usuário acabou de realizar um saque de R${valor:.2f}')
    else:
        print('O valor desejado para saque é inválido ou maior do que o saldo disponível.')
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato):
    print('Extrato'.center(30, '='))
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'Saldo atual: R${saldo:.2f}')
    print('=' * 30)

def filtra_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None

def novo_usuario(usuarios):
    cpf = input('Informe o CPF (apenas números): ')
    usuario = filtra_usuario(cpf, usuarios)
    if usuario:
        print('O usuário já existe com esse CPF.')
        return

    nome = input('Informe o nome: ')
    data_nascimento = input('Informe a data de nascimento (dd/mm/aaaa): ')
    endereco = input('Informe o endereço: ')

    usuarios.append({'cpf': cpf, 'nome': nome, 'data_nascimento': data_nascimento, 'endereco': endereco})
    print(f'Usuário cadastrado! Nome: {nome}')

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtra_usuario(cpf, usuarios)

    if usuario:
        print('Conta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}
    print('Usuário não encontrado.')

def listar_contas(contas):
    if not contas:
        print('Nenhuma conta cadastrada.')
        return
    for conta in contas:
        print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}")

# Variáveis principais
saldo = 0
limite = 500
extrato = ''
numero_saques = 0
limite_saques = 3
usuarios = []
contas = []
AGENCIA = '0001'

menu()

while True:
    escolha = int(input('Escolha: '))

    if escolha == 1:
        print('Opção de Depósito escolhida.')
        valor = float(input('Quanto deseja depositar? R$ '))
        saldo, extrato = deposito(saldo, valor, extrato)

    elif escolha == 2:
        print('Opção de Saque escolhida.')
        valor = float(input('Informe o valor do saque: '))
        saldo, extrato, numero_saques = saque(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=limite_saques,
        )

    elif escolha == 3:
        mostrar_extrato(saldo, extrato=extrato)

    elif escolha == 4:
        novo_usuario(usuarios)

    elif escolha == 5:
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas.append(conta)

    elif escolha == 6:
        listar_contas(contas)

    elif escolha == 7:
        print('Saindo do sistema. Obrigado por usar nosso banco!')
        break

    else:
        print('Opção inválida. Tente novamente.')




