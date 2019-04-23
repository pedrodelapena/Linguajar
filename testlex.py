import ply.lex as lex

# List of token names.   This is always required
tokens = (
'PONTO',
'MAIS',
'MENOS',
'OU',
'IG',       # = 
'PABR',     # (
'PFEC',     # )
'IGUAL',    # ==
'DIFER',    # !=
'MAIOR',
'MENOR',
'MAIORIG',  # >=
'MENORIG',  # <=
'MULTIP',
'DIVIDE',   
'ETMB',     # AND
'NOME',     # name
)
 
# Regular expression rules for simple tokens
t_MAIS    = r'\+'
t_MENOS   = r'-'
t_MULTIP   = r'\*'
t_DIVIDE  = r'/'
t_PABR  = r'\('
t_PFEC  = r'\)'
t_IG = r'='
t_IGUAL  = r'\=\='
t_DIFER  = r'\=\!'
t_MAIOR  = r'>'
t_MENOR  = r'<'
t_MAIORIG  = r'\>\='
t_MENORIG  = r'\<\='
t_PONTO  = r'\.'
t_MENOR  = r'<'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()