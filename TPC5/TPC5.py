import ply.lex as lex
import json
import sys

# Carregar o stock do arquivo

def load_stock():
    try:
        with open('stock.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_stock():
    with open('stock.json', 'w') as f:
        json.dump(stock, f)

def format_currency(value):
    return f"{value:.2f}".replace('.', 'e') + 'c'

# Definição de tokens

tokens = ['LISTAR', 'MOEDA', 'SELECIONAR', 'SAIR', 'CODIGO', 'VALOR', 'VIRGULA', 'PONTO']

def t_LISTAR(t): r'LISTAR'; return t

def t_MOEDA(t): r'MOEDA'; return t

def t_SELECIONAR(t): r'SELECIONAR'; return t

def t_SAIR(t): r'SAIR'; return t

def t_CODIGO(t): r'[A-Z]\d\d'; return t

def t_VALOR(t): r'\d+[ce]?'; return t

t_VIRGULA = r','  
t_PONTO = r'\.'  
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[LEXER] Caráter não reconhecido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Variáveis globais

stock = load_stock()
balance = 0.0
inserted_coins = []

def process_list():
    print("cod | nome | quantidade | preço")
    print("---------------------------------")
    for product in stock:
        print(f"{product['cod']} | {product['nome']} | {product['quant']} | {product['preco']:.2f}€")

def process_coin(cmd):
    global balance, inserted_coins
    coins = [(int(v[:-1]) / 100 if v.endswith('c') else int(v[:-1])) for tok in cmd if (v := tok.value)]
    balance += sum(coins)
    inserted_coins.extend(coins)
    print(f"maq: Saldo = {format_currency(balance)}")

def process_selection(cmd):
    global balance
    if len(cmd) < 2 or cmd[1].type != 'CODIGO':
        print("maq: Comando inválido. Use SELECIONAR <codigo_produto>")
        return
    
    code = cmd[1].value
    product = next((p for p in stock if p['cod'] == code), None)
    
    if not product:
        print("maq: Produto não existe no stock.")
        return
    if product['quant'] == 0:
        print("maq: Produto esgotado.")
        return
    if balance >= product['preco']:
        product['quant'] -= 1
        balance -= product['preco']
        print(f"maq: Pode retirar o produto dispensado: \"{product['nome']}\"")
        print(f"maq: Saldo = {format_currency(balance)}")
    else:
        print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
        print(f"maq: Saldo = {format_currency(balance)}; Pedido = {format_currency(product['preco'])}")

def process_exit():
    global balance, inserted_coins
    change = calculate_change(balance)
    print("maq: Pode retirar o troco: ", ", ".join(change))
    balance, inserted_coins = 0.0, []
    save_stock()
    print("maq: Até à próxima!")
    sys.exit()

def process_command(user_input):
    lexer.input(user_input)
    cmd = [tok for tok in iter(lexer.token, None)]
    
    if not cmd:
        return
    
    match cmd[0].type:
        case 'LISTAR': process_list()
        case 'MOEDA': process_coin(cmd)
        case 'SELECIONAR': process_selection(cmd)
        case 'SAIR': process_exit()
        case _: print("maq: Comando não reconhecido.")

def calculate_change(value):
    available_coins = [2.00, 1.00, 0.50, 0.20, 0.10, 0.05, 0.02]
    change = []
    for coin in available_coins:
        while value >= coin:
            change.append(coin)
            value -= coin
    return [f"{change.count(c)}x {int(c) if c >= 1 else int(c*100)}{'e' if c >= 1 else 'c'}" for c in set(change)]

def main():
    print(f"maq: {sys.argv[0]}, Stock {'carregado' if stock else 'não carregado'}, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    while True:
        try:
            user_input = input(">> ")
            process_command(user_input)
        except EOFError:
            print("\nmaq: xau")
            break

if __name__ == "__main__":
    main()
