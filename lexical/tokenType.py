class TokenType:
    RESERVED_WORDS = {
        'program': 'PROGRAM', 'var': 'VAR', 'integer': 'INTEGER', 'real': 'REAL',
        'string': 'STRING', 'begin': 'BEGIN', 'end': 'END', 'for': 'FOR', 'to': 'TO',
        'while': 'WHILE', 'do': 'DO', 'break': 'BREAK', 'continue': 'CONTINUE',
        'if': 'IF', 'else': 'ELSE', 'then': 'THEN', 'write': 'WRITE', 'writeln': 'WRITELN',
        'read': 'READ', 'readln': 'READLN'
    }

    OPERATORS = {
        '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', 'mod': 'MOD', 'div': 'INT_DIV',
        'or': 'OR', 'and': 'AND', 'not': 'NOT', '==': 'EQ', '<>': 'NEQ', '>': 'GT',
        '>=': 'GTE', '<': 'LT', '<=': 'LTE', ':=': 'ASSIGN'
    }

    SYMBOLS = {
        ';': 'SEMICOLON', ',': 'COMMA', '.': 'DOT', ':': 'COLON',
        '(': 'LPAREN', ')': 'RPAREN'
    }

    @staticmethod
    def get_token_type(word):
        """
        Retorna o tipo de token com base no mapeamento.
        """
        # Verifica palavras reservadas
        if word in TokenType.RESERVED_WORDS:
            return TokenType.RESERVED_WORDS[word]

        # Verifica operadores
        if word in TokenType.OPERATORS:
            return TokenType.OPERATORS[word]

        # Verifica símbolos
        if word in TokenType.SYMBOLS:
            return TokenType.SYMBOLS[word]

        # Verifica identificadores
        if word.isidentifier():
            return 'IDENTIFIER'

        # Verifica números
        if word.isdigit():
            return 'DECIMAL'
        if word.startswith('0x') and all(c in '0123456789ABCDEFabcdef' for c in word[2:]):
            return 'HEXADECIMAL'
        if word.startswith('0') and all(c in '01234567' for c in word[1:]):
            return 'OCTAL'
        if '.' in word and word.replace('.', '').isdigit():
            return 'FLOAT'

        # Verifica strings
        if word.startswith('"') and word.endswith('"'):
            return 'STRING'

        # Caso não seja reconhecido
        return 'UNKNOWN'