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
        #Leitura caracter por caracter
        while self.current_index < len(self.source_code):
            char = self.source_code[self.current_index]

            if self.source_code[self.current_index:self.current_index + 2] == '\\\\' or char == '{':
                self._handle_comment()
                continue

            # Ignorar espaços em branco 
            if char.isspace():
                self._handle_whitespace(char)
                self.current_index += 1
                continue

            # Identificar identificadores ou palavras reservadas
            if char.isalpha():
                self._handle_identifier_or_reserved_word()
                continue
    
            # Identificar operadores (como ':=', '+', '-', etc.)
            if self._is_operator_start(char):
                self._handle_operator()
                continue

            # Identificar símbolos únicos (como ';', ',', etc.)
            if char in TokenType.SYMBOLS:
                self._add_token(TokenType.SYMBOLS[char], char)
                self.current_index += 1
                continue

            # Identificar números
            if char.isdigit():
                self._handle_number()
                continue


            # Identificar strings
            if char == '"':
                self._handle_string()
                continue

            # Símbolo não encontrado
            #self._add_token("UNKNOWN", char)
            raise LexicalError("INVALID TOKEN", self.current_line, self.current_column)

        return self.tokens

    def _handle_whitespace(self, char):
        if char == '\n': 
            self.current_line += 1
            self.current_column = 1
        else:  # Espaços ou tabulação
            self.current_column += 1

    def _is_operator_start(self, char):

        all_operators = list(TokenType.ARITHMETIC_OPERATORS.keys()) + list(TokenType.LOGICAL_OPERATORS.keys())
        return any(op.startswith(char) for op in all_operators)

    def _handle_operator(self):
        operator = ""
        all_operators = list(TokenType.ARITHMETIC_OPERATORS.keys()) + list(TokenType.LOGICAL_OPERATORS.keys())

        # Tenta montar o maior operador possível
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
                    # Apenas processar como UNKNOWN se for realmente um caractere inválido
                    op_char = operator[idx]
                    if op_char.isalpha():
                        # Se for uma letra, não deve ser tratada como operador
                        break
                    token_type = TokenType.LOGICAL_OPERATORS.get(op_char, "UNKNOWN")
                    self._add_token(token_type, op_char)
                    idx += 1
    
    def _handle_number(self):
        start_index = self.current_index
        number = ""
        has_dot = False

        # HEXADECIMAL: começa com 0x ou 0X
        
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

        # OCTAL: começa com '0' seguido de 0-7
        
        if self.source_code[self.current_index] == '0':
            number += '0'
            self.current_index += 1

            while (self.current_index < len(self.source_code) and 
                self.source_code[self.current_index] in '01234567'):
                number += self.source_code[self.current_index]
                self.current_index += 1

            # se vier 8 ou 9 após dígitos octais, invalida tudo
            if (self.current_index < len(self.source_code) and 
                self.source_code[self.current_index].isdigit() and 
                self.source_code[self.current_index] not in '01234567'):
                while (self.current_index < len(self.source_code) and 
                    self.source_code[self.current_index].isdigit()):
                    number += self.source_code[self.current_index]
                    self.current_index += 1

                raise LexicalError("INVALID TOKEN", self.current_line, self.current_column )

            # em '0' isolado é decimal; em '0' + [0-7]+ é OCTAL
            if len(number) > 1:
                self._add_token("OCTAL", number)
            else:
                self._add_token("DECIMAL", number)
            return

        # FLOAT ou DECIMAL
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

        # Se terminou com '.', completa para "x.0"
        if has_dot and number.endswith('.'):
            number += '0'

        # Para FLOAT: checa vírgula, parênteses ou ponto extra como erro
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

        # FLOAT ou DECIMAL
        if has_dot:
            self._add_token("FLOAT", number)
        else:
            self._add_token("DECIMAL", number)
        return

    def _handle_identifier_or_reserved_word(self):
        start_index = self.current_index
        identifier = ""
       

        # Identificadores ou palavras reservadas
        while self.current_index < len(self.source_code) and self.source_code[self.current_index].isalnum():
            identifier += self.source_code[self.current_index]
            self.current_index += 1

        if identifier in TokenType.RESERVED_WORDS:
            print(f"Identificador: {self.identifier}")  
            self._add_token(TokenType.RESERVED_WORDS[identifier], identifier)
        else:
            print(f"Identificador A: {identifier}")
            self._add_token("IDENTIFIER", identifier)

    def _add_token(self, token_type, value):
        lexeme = Lexeme(token_type, value, self.current_line, self.current_column)
        self.tokens.append(lexeme)
        self.symbol_table.add(lexeme)
        self.current_column += len(value)

    def _handle_comment(self):
        # Comentario uma linha: começa com '\\' termina no  '\n'
        if self.source_code[self.current_index:self.current_index + 2] == '\\\\':
            self.current_index += 2  # Pula os dois caracteres '\\'
            self.current_column += 2 
            while self.current_index < len(self.source_code) and self.source_code[self.current_index] != '\n':
                self.current_index += 1  # Avança para o próximo caractere no comentário
                self.current_column += 1 
            if self.current_index < len(self.source_code) and self.source_code[self.current_index] == '\n':
                self.current_index += 1  # Pula o caractere de nova linha
                self.current_line += 1 
                self.current_column = 1
            return

        # Comentario multiplas linhas: começa com '{' termina com '}'
        if self.source_code[self.current_index] == '{':
            self.current_index += 1  # Pula o caractere '{'
            self.current_column += 1 
            while self.current_index < len(self.source_code):
                if self.source_code[self.current_index] == '}':
                    self.current_index += 1  # Pula o caractere '}'
                    self.current_column += 1
                    return
                elif self.source_code[self.current_index] == '\n':
                    self.current_index += 1  # Pula o caractere de nova linha
                    self.current_line += 1  
                    self.current_column = 1 
                else:
                    self.current_index += 1  # Avança para o próximo caractere
                    self.current_column += 1 
            # Se '}' não for encontrado
            raise ValueError("Unterminated multi-line comment")
        
    def _handle_string(self):   
        string_value = ""
        self.current_index += 1  # Pula o caractere inicial de aspas

        while self.current_index < len(self.source_code) and self.source_code[self.current_index] != '"':
            if self.source_code[self.current_index] == '\n':
                raise ValueError("Unclosed string literal")
            string_value += self.source_code[self.current_index]
            self.current_index += 1
            

        # Fecha a string se encontrar aspas finais
        if self.current_index < len(self.source_code) and self.source_code[self.current_index] == '"':
            self.current_index += 1 
            self.current_column += 1
            self._add_token("STRING", string_value)
            self.current_column += 1
            
        else:
            raise ValueError("Unclosed string literal")