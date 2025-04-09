from lexical.lexeme import Lexeme
from lexical.tokenType import TokenType
from lexical.symbolTable import SymbolTable

class LexicalAnalysis:
    def __init__(self, source_code):
        self.source_code = source_code
        self.symbol_table = SymbolTable()
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.current_index = 0  # Índice atual no código-fonte

    def analyze(self):
        #Aqui ele le caracter por caracter
        while self.current_index < len(self.source_code):
            char = self.source_code[self.current_index]

            # Ignorar espaços em branco e atualizar posição
            if char.isspace():
                self._handle_whitespace(char)
                self.current_index += 1
                continue

            # Identificar símbolos únicos (como ';', ',', etc.)
            if char in TokenType.SYMBOLS:
                self._add_token(TokenType.SYMBOLS[char], char)
                self.current_index += 1
                continue

            # Identificar operadores (como ':=', '+', '-', etc.)
            if self._is_operator_start(char):
                self._handle_operator()
                continue

            # Identificar números
            if char.isdigit():
                self._handle_number()
                continue

            # Identificar identificadores ou palavras reservadas
            if char.isalpha():
                self._handle_identifier_or_reserved_word()
                continue

            # Identificar strings
            if char == '"':
                self._handle_string()
                continue

            # Caso não reconhecido, avança e marca como desconhecido
            self._add_token("UNKNOWN", char)
            self.current_index += 1

        return self.tokens

    def _handle_whitespace(self, char):
        if char == '\n':  # Nova linha
            self.current_line += 1
            self.current_column = 1
        else:  # Espaços ou tabulação
            self.current_column += 1

    def _is_operator_start(self, char):
        # Verifica se o caractere inicial pode ser parte de um operador
        return any(op.startswith(char) for op in TokenType.OPERATORS)

    def _handle_operator(self):
        start_index = self.current_index
        operator = self.source_code[self.current_index]

        # Tenta formar operadores compostos (como ':=' ou '>=')
        while (self.current_index + 1 < len(self.source_code) and
               any(op.startswith(operator + self.source_code[self.current_index + 1]) for op in TokenType.OPERATORS)):
            self.current_index += 1
            operator += self.source_code[self.current_index]

        if operator in TokenType.OPERATORS:
            self._add_token(TokenType.OPERATORS[operator], operator)
        else:
            self._add_token("UNKNOWN", operator)

        self.current_index += 1

    def _handle_number(self):
        start_index = self.current_index
        number = ""

        # Lê dígitos inteiros ou flutuantes
        while self.current_index < len(self.source_code) and (self.source_code[self.current_index].isdigit() or self.source_code[self.current_index] == '.'):
            number += self.source_code[self.current_index]
            self.current_index += 1

        # Verifica se é um número válido
        if '.' in number:
            self._add_token("FLOAT", number)
        else:
            self._add_token("DECIMAL", number)

    def _handle_identifier_or_reserved_word(self):
        start_index = self.current_index
        identifier = ""

        # Lê caracteres alfanuméricos para formar identificadores ou palavras reservadas
        while self.current_index < len(self.source_code) and self.source_code[self.current_index].isalnum():
            identifier += self.source_code[self.current_index]
            self.current_index += 1

        # Verifica se é uma palavra reservada
        if identifier in TokenType.RESERVED_WORDS:
            self._add_token(TokenType.RESERVED_WORDS[identifier], identifier)
        else:
            self._add_token("IDENTIFIER", identifier)

    def _handle_string(self):
        start_index = self.current_index
        string_value = ""
        self.current_index += 1  # Pula o caractere inicial de aspas

        while self.current_index < len(self.source_code) and self.source_code[self.current_index] != '"':
            string_value += self.source_code[self.current_index]
            self.current_index += 1

        # Fecha a string se encontrar aspas finais
        if self.current_index < len(self.source_code) and self.source_code[self.current_index] == '"':
            self.current_index += 1  # Pula o caractere final de aspas
            self._add_token("STRING", string_value)
        else:
            self._add_token("UNKNOWN", string_value)  # String mal formada

    def _add_token(self, token_type, value):
        lexeme = Lexeme(token_type, value, self.current_line, self.current_column)
        self.tokens.append(lexeme)
        self.symbol_table.add(lexeme)
        self.current_column += len(value)