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
                continue

            if char.isalpha():
                self._handle_identifier_or_reserved_word()
                continue
    
            ## Identificar quando é somente : ou quando é := (atribuição)
            if char == ':':
                if self.current_index + 1 < len(self.source_code) and self.source_code[self.current_index + 1] == '=':
                    self._add_token(TokenType.LOGICAL_OPERATORS[':='], ':=')
                    self.current_index += 2 
                else:
                    self._add_token(TokenType.SYMBOLS[':'], ':')
                    self.current_index += 1 
                continue

            if char in TokenType.SYMBOLS:
                self._add_token(TokenType.SYMBOLS[char], char)
                self.current_index += 1
                continue

            ## Identificar quando é somente /(operacao de divisao) ou quando é //(comentario)
            if char == '/':
                if self.source_code[self.current_index:self.current_index + 2] == '//':
                    self._handle_comment()
                    continue
                else:
                    self._add_token(TokenType.ARITHMETIC_OPERATORS['/'], '/')
                    self.current_index += 1
                    continue

            if self._is_operator_start(char):
                self._handle_operator()
                continue

            if char.isdigit():
                self._handle_number()
                continue

            if char == '"' or char == "'":
                self._handle_string()
                continue

            raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)

        return self.tokens

    def _handle_whitespace(self, char):
        if char == '\n': 
            self.current_line += 1
            self.current_column = 1
        else:
            self.current_column += 1

    def _is_operator_start(self, char):

        all_operators = list(TokenType.ARITHMETIC_OPERATORS.keys()) + list(TokenType.LOGICAL_OPERATORS.keys())
        return any(op.startswith(char) for op in all_operators)

    def _handle_operator(self):
        operator = ""
        all_operators = list(TokenType.ARITHMETIC_OPERATORS.keys()) + list(TokenType.LOGICAL_OPERATORS.keys())

        while (self.current_index < len(self.source_code) and
            any(op.startswith(operator + self.source_code[self.current_index]) for op in all_operators)):
            operator += self.source_code[self.current_index]
            self.current_index += 1

        if operator in all_operators:
            token_type = (TokenType.ARITHMETIC_OPERATORS.get(operator) or
                        TokenType.LOGICAL_OPERATORS.get(operator))
            self._add_token(token_type, operator)
        else:
            idx = 0
            while idx < len(operator):
                matched = False
                for size in range(3, 0, -1):
                    part = operator[idx:idx+size]
                    if part in all_operators:
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
                    token_type = TokenType.LOGICAL_OPERATORS.get(op_char, "UNKNOWN")
                    self._add_token(token_type, op_char)
                    idx += 1
    
    def _handle_number(self):
        start_index = self.current_index
        number = ""
        has_dot = False

        if self.source_code[self.current_index:self.current_index + 2].lower() == "0x":
            number += self.source_code[self.current_index:self.current_index + 2]
            self.current_index += 2

            while (self.current_index < len(self.source_code) and 
                self.source_code[self.current_index].isalnum()):
                number += self.source_code[self.current_index]
                self.current_index += 1

            digits = number[2:]
            if digits and all(c in "0123456789abcdefABCDEF" for c in digits):
                self._add_token("HEXADECIMAL", number)
            else:

                raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)
            return


        if self.source_code[self.current_index] == '0':
            number += '0'
            self.current_index += 1

            while (self.current_index < len(self.source_code) and 
                self.source_code[self.current_index] in '01234567'):
                number += self.source_code[self.current_index]
                self.current_index += 1

            if (self.current_index < len(self.source_code) and 
                self.source_code[self.current_index].isdigit() and 
                self.source_code[self.current_index] not in '01234567'):
                while (self.current_index < len(self.source_code) and 
                    self.source_code[self.current_index].isdigit()):
                    number += self.source_code[self.current_index]
                    self.current_index += 1

                raise LexicalError("INVALID TOKEN", self.current_line, self.current_column )

            if len(number) > 1:
                self._add_token("OCTAL", number)
            else:
                self._add_token("DECIMAL", number)
            return

        dot_count = 0
        while (self.current_index < len(self.source_code) and 
            (self.source_code[self.current_index].isdigit() or 
            self.source_code[self.current_index] == '.' or 
            self.source_code[self.current_index].isalpha())):
            
            c = self.source_code[self.current_index]
            if c == '.':
                dot_count += 1
                if dot_count > 1:
                    number += c
                    self.current_index += 1
    
                    raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)
                has_dot = True
            elif c.isalpha():
                number += c
                self.current_index += 1

                raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)
            number += c
            self.current_index += 1

        if has_dot and number.endswith('.'):
            number += '0'

        if has_dot and self.current_index < len(self.source_code) and \
        self.source_code[self.current_index] in '.':
            number += self.source_code[self.current_index]
            self.current_index += 1
            raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)

        if (self.current_index < len(self.source_code) and
            not self.source_code[self.current_index].isspace() and
            self.source_code[self.current_index] not in TokenType.SYMBOLS):
            while (self.current_index < len(self.source_code) and
                not self.source_code[self.current_index].isspace() and
                self.source_code[self.current_index] not in TokenType.SYMBOLS):
                number += self.source_code[self.current_index]
                self.current_index += 1
            raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)

        if has_dot:
            self._add_token("FLOAT", number)
        else:
            self._add_token("DECIMAL", number)
        return

    def _handle_identifier_or_reserved_word(self):
        start_index = self.current_index
        identifier = ""
       
        while self.current_index < len(self.source_code) and self.source_code[self.current_index].isalnum():
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
            self._add_token("STRING", string_value)
            self.current_column += 1
        else:
            raise ValueError("Unclosed string literal", self.current_line, self.current_column)