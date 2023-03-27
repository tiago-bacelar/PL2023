import ply.lex

tokens = ('COMMENT', 'TYPE', 'OP', 'CTRL', 'NUMBER', 'IDENT')
literals = r",;{}[]()"
t_ignore = " \t\n"

t_ignore_COMMENT = r'//.*|/\*[^§]*?\*/'

t_TYPE = r'\b(?:int|long|short|float|double|char)\b'
t_OP = r'\+|-|\*|<=?|>=?|(!|=)=|\.'
t_CTRL = r'\b(?:program|function|if|else|while|for|in)\b|\.\.|='
t_NUMBER = r'(?://///////////){0}-?\d+'
t_IDENT = r'\b\w+\b'


def t_error(t):
    raise ValueError(f"Unexpected token '{t.value}' in line {t.lineno}")

lexer = ply.lex.lex()
lexer.input("""

/* max.p: calcula o maior inteiro duma lista desordenada
-- 2023-03-20 
-- by jcr
*/

int i = 10, a[10] = {1,2,3,4,5,6,7,8,9,10};

// Programa principal
program myMax{
  int max = a[0];
  for i in [1..9]{
    if max < a[i] {
      max = a[i];
    }
  }
  print(max);
}
            
""")

while t:= lexer.token():
    print(t)