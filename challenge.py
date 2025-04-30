#************** Regras para desenvolvimento *****************

# Novas Funções

# - Criar Usuário (cliente)
#   - Armazenar os usuários em uma lista com:
#        - Nome
#        - Data Nascimento
#        - CPF (apenas números)
#        - Endereço (Logradouro, nro - Bairro, Cidade/UF)
#   - Não podem haver CPFs repetidos

# - Criar Conta Corrente
#   - Armazenar as contas em uma lista com:
#        - Agência (Fixo: '0001')
#        - Nro Conta (sequencial, iniciado em 1)
#   - Um usuário pode ter mais de uma conta, mas uma conta pertence apenas a um usuário

import os

def new_window(title=''):
    os.system('cls')
    WIDTH = 100
    BANK_NAME = f"{' Mu Bank '.center(WIDTH, '=')}\n"

    print(BANK_NAME)

    if title:
        print(title.upper().center(WIDTH))
    

def menu():
    new_window()
    menu = f'''[1] - Cadastrar Usuário
[2] - Cadastrar Conta Corrente
[3] - Depósito
[4] - Saque
[5] - Extrato
[6] - Listar Usuários
[7] - Listar Contas Correntes
[0] - Sair
    '''
    print(menu)
    
    option = int(input('Digite a opção desejada: '))
    
    return option 

def deposit(deposits, /):
    new_window('DEPÓSITO')
    value = float(input('Valor do depósito: R$'))

    if value > 0:
        deposits.append(value)
        print('\nDepósito realizado com sucesso!\n')
    else:
        value = 0
        print('\nValor inválido!\n')
    
    return value

def withdraw(*, withdrawals, balance, remaining_withdrawals, withdrwal_limit):
    new_window('SAQUE')
    value = float(input('Valor do saque: R$'))

    if value > 0:
        if value > withdrwal_limit:
            value = 0
            print('\nOperação não permitida!\n\nO valor escede seu limite por saque.\n')
        elif remaining_withdrawals == 0:
            value = 0
            print('\nOperação não permitida!\n\nVocê atingiu a quantidade máxima de saques.\n')
        elif value > balance:
            value = 0
            print('\nOperação não permitida!\n\nNão há saldo suficiente para realizar esta operação.\n')
        else:
            withdrawals.append(value)
            print('\nSaque realizado com sucesso!\n')
    else:
        print('\nValor inválido!\n')

    return value

def extract(balance, /, *, deposits, withdrawals):
    new_window('EXTRATO')
    if deposits or withdrawals:
        if deposits:
            print('DEPÓSITOS')
            for deposit in deposits:
                print(f'+ R${deposit:.2f}')
        
        if withdrawals:
            print(f'*' * 50)
            print('SAQUES')
            for withdraw in withdrawals:
                print(f'- R${withdraw:.2f}')

        print(f'\nSALDO ATUAL: R${balance:.2f}')
    else:
        print('\nNão foram realizadas movimentações.\n')

def get_user(doc_id, users):
    user = [user for user in users if user['doc_id'] == doc_id]
    return user[0] if user else None

def create_user(users):
    new_window('CADASTRO DE USUÁRIO')
    doc_id = input('CPF (apenas números): ')
    found_user = get_user(doc_id, users)

    if not found_user:
        user = dict()
        
        user['name'] = input('Nome: ')
        user['date_of_birth'] = input('Data Nascimento (dd/mm/aaa): ')
        user['doc_id'] = doc_id
        
        print('\nEndereço\n')
        
        user['address'] = f'{input('Logradouro: ')}, {input('Número: ')} - {input('Bairro: ')}, {input('Cidade: ')}/{input('UF: ')}'
        users.append(user)
        print('\nCadastro realizado com sucesso!\n')
    else:
        print('\nCadastro não permitido!\nJá existe um usuário cadastrado com o CPF informado\n')

def list_users(users):
    new_window('USUÁRIOS CADASTRADOS')
    if users:
        for user in users:
            print(f'Nome: {user['name']}')
            print(f'Data de Nascimento: {user['date_of_birth']}')
            print(f'CPF: {user['doc_id']}')
            print(f'Endereço: {user['address']}')
            print(f"\n{'-' * 20}\n")
    else:
        print('\nNão existem usuários cadastrados\n')

def create_account(agency, accounts, users):
    new_window('CADASTRO DE CONTAS')
    doc_id = input('CPF do cliente (apenas números): ')
    user = get_user(doc_id, users)
    if user:
        account_number = len(accounts) + 1
        account = dict()
        account['agency'] = agency
        account['account'] = account_number
        account['user'] = user
        accounts.append(account)
        print(f'\nConta {account_number} criada com sucesso para o cliente {user['name']}\n')
    else:
        print('\nUsuário não encontrado!\nVerifique o CPF informado e tente novamente.\n')

def lis_accounts(accounts):
    new_window('CONTAS CADASTRADAS')
    if accounts:
        for account in accounts:
            print(f'Agência: {account['agency']}')
            print(f'C/C: {account['account']}\n')
            print(f'Nome: {account['user']['name']}')
            print(f'CPF: {account['user']['doc_id']}')
            print('-' * 30, end='\n')
    else:
        print('\nNão existem contas cadastradas\n')

def main():
    WITHDRAWAL_LIMIT = 500
    OPTIONS = [0, 1, 2, 3, 4, 5, 6, 7]
    AGENCY = '0001'
    
    remaining_withdrawals = 3
    balance = 0
    deposits = []
    withdrawals = []
    users = []
    accounts = []

    while True:
        option = menu()

        if option in OPTIONS:
            if option == 1:
                create_user(users)
            elif option == 2:
                create_account(AGENCY, accounts, users)
            elif option == 3:
                deposit_value = deposit(deposits)
                
                if deposit_value:
                    balance += deposit_value    
            elif option == 4:
                withdraw_value = withdraw(
                    withdrawals=withdrawals,
                    balance=balance,
                    remaining_withdrawals=remaining_withdrawals,
                    withdrwal_limit=WITHDRAWAL_LIMIT)
                
                if withdraw_value:
                    balance -= withdraw_value
                    remaining_withdrawals -= 1
                
            elif option == 5:
                extract(balance, withdrawals=withdrawals, deposits=deposits)
            elif option == 6:
                list_users(users)
            elif option == 7:
                lis_accounts(accounts)
            else:
                os.system('cls')
                print('\nPrograma encerrado!')
                break

            input('Pressione ENTER para voltar ao menu principal.')
        else:
            print('\nOpção inválida!\n')
            input('Pressione ENTER para voltar ao menu principal.')

if __name__ == '__main__':
    main()