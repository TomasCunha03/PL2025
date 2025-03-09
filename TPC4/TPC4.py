import ply.lex as lex

# Definição de palavras-chave
keywords = {
    'select': 'KW_SELECT',
    'where': 'KW_WHERE',
    'limit': 'KW_LIMIT',
}

# Lista de tipos de tokens
tokens = [
    'ID', 'TEXT', 'INTEGER',
    'PERIOD', 'QUESTION', 'ASSIGN', 'OPEN_BRACE', 'CLOSE_BRACE',
] + list(keywords.values())

# Definição de padrões para tokens específicos
t_PERIOD = r'\.'
t_QUESTION = r'\?'
t_ASSIGN = r'='
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'

# Identificadores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_:]*'
    t.type = keywords.get(t.value.lower(), 'ID')
    return t

# Cadeias de texto
def t_TEXT(t):
    r'"[^"]*"(?:@[a-zA-Z]+)?'
    return t

# Valores numéricos
def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Reconhecimento de novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Comentários
def t_COMMENT(t):
    r'\#.*'
    pass

# Tratamento de caracteres inválidos
def t_error(t):
    print(f"Caractere não reconhecido: '{t.value[0]}'")
    t.lexer.skip(1)

# Construção do analisador léxico
lexer = lex.lex()

# Exemplo de entrada
test_data = '''
# Consulta para dados de um artista musical
select ?name ?info where { 
    ?s a dbo:MusicalArtist. 
    ?s foaf:name "Quim Barreiros Barros"@en . 
    ?w dbo:artist ?s. 
    ?w foaf:name ?name. 
    ?w dbo:abstract ?info 
} limit 1000
'''

lexer.input(test_data)

print("Tokens encontrados:")
for token in lexer:
    print(token)
