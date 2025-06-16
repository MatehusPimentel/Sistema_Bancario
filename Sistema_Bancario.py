def menu():
    print('-' * 30)
    print('MENU BANCÁRIO'.center(30))
    print('-' * 30)

saldo = 0
limite = 500
extrato = ''
numero_saques = 0
limite_saques = 3


menu()
print('''[1] Depósito
[2] Sacar
[3] Extrato
[4] Sair''')

while True:

    escolha = int(input('Escolha: '))

    if escolha == 1:
        print('Opção de Depósito escolhida.')
        deposito = float(input('Quanto deseja depositar? R$ '))  
        
        if deposito > 0:  
            saldo += deposito
            extrato += f"Depósito: R${deposito:.2f}"
            print(f'O usuário acabou de realizar um depósito de R${deposito:.2f}')
            print(f'Seu saldo atual é de R${saldo:.2f}')
            
        else:
            print('Valor inválido para depósito.')

    elif escolha == 2:
        print('Opção de Saque escolhida.')
        if numero_saques >= limite_saques:
            print('Limite de saques diários atingido.')
            continue

        saque = float(input('Quanto deseja sacar? R$ '))

        if saque > 0 and saque <= saldo and saque <= limite:
            saldo -= saque
            numero_saques += 1
            extrato += f"Saque:    R${saque:.2f}\n"
            print(f'O usuário acabou de realizar um saque de R${saque:.2f}')
            print(f'Seu saldo atual é de R${saldo:.2f}')
        else:
            print('O valor desejado para saque é inválido ou maior do que o saldo disponível.')
        
    elif escolha == 3:
        print('Extrato'.center(30, '='))
        print('Não foram realizadas movimentações.' if not extrato else extrato)
        print(f'Saldo atual: R${saldo:.2f}')
        print('=' * 30)

    elif escolha == 4:
        print('Saindo do sistema. Obrigado por usar nosso banco!')
        break

    else:
        print('Opção inválida. Tente novamente.')




