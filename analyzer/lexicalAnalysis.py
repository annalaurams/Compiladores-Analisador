from lexical.lexeme import Lexeme
from lexical.tokenType import TokenType
from lexical.symbolTable import SymbolTable

class LexicalError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"{message} at line {line}, column {column}")
        self.message = message
        self.line = line
        self.column = column

class LexicalAnalysis:
    def __init__(self, source_code):
        self.source_code = source_code
        self.symbol_table = SymbolTable()
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.current_index = 0  

    def analyze(self):
        while self.current_index < len(self.source_code):
            char = self.source_code[self.current_index]

            if char.isspace():
                self._handle_whitespace(char)
                self.current_index += 1

            elif char.isdigit() or (char == '.' and self.current_index + 1 < len(self.source_code) and self.source_code[self.current_index + 1].isdigit()):
                self._handle_number()

            elif char.isalpha() or char == '_':
                self._handle_identifier_or_reserved_word()

            elif char == '{':
                self._handle_comment()
    
            elif char == ':':
                if self.current_index + 1 < len(self.source_code) and self.source_code[self.current_index + 1] == '=':
                    self._add_token(TokenType.LOGICAL_OPERATORS[':='], ':=')
                    self.current_index += 2 
                else:
                    self._add_token(TokenType.SYMBOLS[':'], ':')
                    self.current_index += 1   

            elif char in TokenType.SYMBOLS:
                self._add_token(TokenType.SYMBOLS[char], char)
                self.current_index += 1

            ## Identificar quando é somente / ou quando é //
            elif char == '/':
                if self.source_code[self.current_index:self.current_index + 2] == '//':
                    self._handle_comment()
                else:
                    self._add_token(TokenType.ARITHMETIC_OPERATORS['/'], '/')
                    self.current_index += 1
                  
            elif self._is_operator_start(char):
                self._handle_operator()
                continue

            elif char == '"' or char == "'":
                self._handle_string()
                continue

            else:
                raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)

        return self.tokens

    def _handle_whitespace(self, char):
        if char == '\n': 
            self.current_line += 1
            self.current_column = 1
        else:
            self.current_column += 1

    def _is_operator_start(self, char):
        return any(op.startswith(char) for op in TokenType.ARITHMETIC_OPERATORS) or any(op.startswith(char) for op in TokenType.LOGICAL_OPERATORS) 

    def _handle_operator(self):
        operator = ""

        while (self.current_index < len(self.source_code) and
            (any(op.startswith(operator + self.source_code[self.current_index]) for op in TokenType.LOGICAL_OPERATORS)) or
            any(op.startswith(operator + self.source_code[self.current_index]) for op in TokenType.ARITHMETIC_OPERATORS)):
            operator += self.source_code[self.current_index]
            self.current_index += 1
        
        if operator in TokenType.ARITHMETIC_OPERATORS or operator in TokenType.LOGICAL_OPERATORS:
            token_type = (TokenType.ARITHMETIC_OPERATORS.get(operator) or
                        TokenType.LOGICAL_OPERATORS.get(operator))
            self._add_token(token_type, operator)
        else:
            idx = 0
            while idx < len(operator):
                matched = False
                for size in range(3, 0, -1):
                    part = operator[idx:idx+size]
                    if part in TokenType.ARITHMETIC_OPERATORS or operator in TokenType.LOGICAL_OPERATORS:
                        token_type = (TokenType.ARITHMETIC_OPERATORS.get(part) or
                                    TokenType.LOGICAL_OPERATORS.get(part))
                        self._add_token(token_type, part)
                        idx += size
                        matched = True
                        break
                if not matched:
                    op_char = operator[idx]
                    if op_char.isalpha():
                        break
    
    def _handle_number(self):
        number = ""
        has_dot = False
        dot_count = 0

        delimiters = {';', '\n', ' ', ',', ':', '(', ')'}

        while self.current_index < len(self.source_code) and \
            self.source_code[self.current_index] not in delimiters and \
            not self._is_operator_start(self.source_code[self.current_index]):
            c = self.source_code[self.current_index]

            self.current_column += 1

            if len(number) == 0 and c == '0':
                number += c
                self.current_index += 1

                # Hexadecimal 
                if self.current_index < len(self.source_code) and self.source_code[self.current_index].lower() == 'x':
                    number += self.source_code[self.current_index]
                    self.current_index += 1
                    self.current_column += 1

                    hexadecimal_set = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'}
                    while self.current_index < len(self.source_code) and \
                            self.source_code[self.current_index].upper() in hexadecimal_set:
                        hex_char = self.source_code[self.current_index]
                        number += hex_char
                        self.current_index += 1
                        self.current_column += 1

                    if self.source_code[self.current_index].upper() not in hexadecimal_set and \
                            self.source_code[self.current_index] not in delimiters and \
                            self.source_code[self.current_index] not in TokenType.SYMBOLS:
                        raise LexicalError("INVALID HEXADECIMAL TOKEN", self.current_line, self.current_column)

                    self._add_token("HEXADECIMAL", number)
                    return

                # Float
                if self.current_index < len(self.source_code) and self.source_code[self.current_index] == '.':
                    has_dot = True
                    dot_count += 1
                    number += '.'
                    self.current_index += 1
                    continue

                # Octal
                while self.current_index < len(self.source_code)and \
                        self.source_code[self.current_index] not in delimiters and \
                        self.source_code[self.current_index] not in TokenType.SYMBOLS and \
                        not self._is_operator_start(self.source_code[self.current_index]):
                    if self.source_code[self.current_index] in {'0', '1', '2', '3', '4', '5', '6', '7'}:
                        number += self.source_code[self.current_index]
                        self.current_index += 1
                        self.current_column += 1
                    else:
                        raise LexicalError("INVALID OCTAL TOKEN: OCTAL NUMBERS CANNOT CONTAIN DOTS, INVALID DIGITS, OR LETTERS", self.current_line, self.current_column)
                self._add_token("OCTAL", number)
                return

            # Verifica se o primeiro caractere é um ponto
            elif len(number) == 0 and c == '.':
                number = '0.' 
                has_dot = True
                dot_count += 1
                self.current_index += 1

            elif c.isdigit() or c == '.':
                if c == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise LexicalError("INVALID FLOAT TOKEN: MULTIPLE DOTS", self.current_line, self.current_column)
                    has_dot = True
                number += c
                self.current_index += 1

            else:
                raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)

        if self.current_index < len(self.source_code) and self.source_code[self.current_index].isalpha():
            raise LexicalError("INVALID NUMBER TOKEN: NUMBERS CANNOT CONTAIN LETTERS", self.current_line, self.current_column)

        if has_dot:
            if number.endswith('.'):
                number += '0' 
            self._add_token("FLOAT", number)
        else:
            self._add_token("DECIMAL", number)

        if self.current_index < len(self.source_code) and self.source_code[self.current_index] == '\n':
            self.current_line += 1
            self.current_column = 1
            self.current_index += 1

    def _handle_identifier_or_reserved_word(self):
        identifier = ""

        if self.current_index < len(self.source_code) and (self.source_code[self.current_index].isalpha() or self.source_code[self.current_index] == '_'):
            identifier += self.source_code[self.current_index]
            self.current_index += 1

        while self.current_index < len(self.source_code) and (self.source_code[self.current_index].isalnum() or self.source_code[self.current_index] == '_'):
            identifier += self.source_code[self.current_index]
            self.current_index += 1

        if identifier in TokenType.RESERVED_WORDS:
            self._add_token(TokenType.RESERVED_WORDS[identifier], identifier)
        else:
            self._add_token("IDENTIFIER", identifier)

    def _add_token(self, token_type, value):
        lexeme = Lexeme(token_type, value, self.current_line, self.current_column)
        self.tokens.append(lexeme)
        self.symbol_table.add(lexeme)
        self.current_column += len(value)

    def _handle_comment(self):
        if self.source_code[self.current_index:self.current_index + 2] == '//':
            self.current_index += 2  
            self.current_column += 2
            while self.current_index < len(self.source_code) and self.source_code[self.current_index] != '\n':
                self.current_index += 1  
                self.current_column += 1
            if self.current_index < len(self.source_code) and self.source_code[self.current_index] == '\n':
                self.current_index += 1 
                self.current_line += 1
                self.current_column = 1
            return

        if self.source_code[self.current_index] == '{':
            self.current_index += 1  
            self.current_column += 1
            while self.current_index < len(self.source_code):
                if self.source_code[self.current_index] == '}':
                    self.current_index += 1  
                    self.current_column += 1
                    return
                elif self.source_code[self.current_index] == '\n':
                    self.current_index += 1  
                    self.current_line += 1
                    self.current_column = 1
                else:
                    self.current_index += 1  
                    self.current_column += 1
            raise ValueError("Unterminated multi-line comment", self.current_line, self.current_column)
        
    def _handle_string(self):   
        string_value = ""
        opening_quote = self.source_code[self.current_index]  
        self.current_index += 1 

        while self.current_index < len(self.source_code) and self.source_code[self.current_index] != opening_quote:
            if self.source_code[self.current_index] == '\n':
                raise ValueError("Unclosed string literal", self.current_line, self.current_column)
            string_value += self.source_code[self.current_index]
            self.current_index += 1

        if self.current_index < len(self.source_code) and self.source_code[self.current_index] == opening_quote:
            self.current_index += 1 
            self.current_column += 1
            interpreted_string = string_value.encode('utf-8').decode('unicode_escape')
            self._add_token("STRING", interpreted_string)
            self.current_column += 1
        else:
            raise ValueError("Unclosed string literal", self.current_line, self.current_column)