class TokenType:
    RESERVED_WORDS = {
        'program': 'PROGRAM', 'var': 'VAR', 'integer': 'INTEGER', 'real': 'REAL',
        'string': 'STRING', 'begin': 'BEGIN', 'end': 'END', 'for': 'FOR', 'to': 'TO',
        'while': 'WHILE', 'do': 'DO', 'break': 'BREAK', 'continue': 'CONTINUE',
        'if': 'IF', 'else': 'ELSE', 'then': 'THEN', 'write': 'WRITE', 'writeln': 'WRITELN',
        'read': 'READ', 'readln': 'READLN'
    }

    ARITHMETIC_OPERATORS = {
        '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', 'mod': 'MOD', 'div': 'INT_DIV'
    }

    LOGICAL_OPERATORS = {
        'or': 'OR', 'and': 'AND', 'not': 'NOT', '==': 'EQ', '<>': 'NEQ', '>': 'GT',
        '>=': 'GTE', '<': 'LT',  '<=': 'LTE', ':=': 'ASSIGN', '=': 'EQUALS'
    }

    SYMBOLS = {
        ';': 'SEMICOLON', ',': 'COMMA', '.': 'DOT', ':': 'COLON',
        '(': 'LPAREN', ')': 'RPAREN'
    }
