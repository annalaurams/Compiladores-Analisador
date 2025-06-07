from typing import List, Tuple
from analyzer.lexeme import Lexeme

class IntermediateCodeGenerator:
    def __init__(self):
        self.instructions: List[Tuple[str, str, str, str]] = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self) -> str:
        temp = f"T{self.temp_count+1}"
        self.temp_count += 1
        return temp

    def new_label(self) -> str:
        label = f"L{self.label_count+1}"
        self.label_count += 1
        return label

    def emit(self, op: str, arg1: str, arg2: str, result: str):
        self.instructions.append((op, arg1, arg2, result))

    def generate_from_tokens(self, tokens: List[Lexeme]):
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok.token_type == 'IDENTIFIER' and i + 1 < len(tokens) and tokens[i+1].token_type == 'ASSIGN':
                i = self._handle_assignment(tokens, i)
            elif tok.token_type == 'IF':
                i = self._handle_if(tokens, i)
            elif tok.token_type == 'WHILE':
                i = self._handle_while(tokens, i)
            elif tok.token_type == 'FOR':
                i = self._handle_for(tokens, i)
            else:
                i += 1

    def _handle_assignment(self, tokens: List[Lexeme], i: int) -> int:
        # Parse: <id> := <expr>;
        var_name = tokens[i].value
        i += 2  # skip IDENTIFIER and ASSIGN

        # Collect expression tokens until semicolon
        expr_tokens = []
        while i < len(tokens) and tokens[i].token_type != 'SEMICOLON':
            expr_tokens.append(tokens[i])
            i += 1

        # Evaluate expression left-to-right for binary ops
        if expr_tokens:
            current = expr_tokens[0].value
            j = 1
            while j < len(expr_tokens):
                op_tok = expr_tokens[j]
                right = expr_tokens[j+1].value if (j+1) < len(expr_tokens) else ''
                temp = self.new_temp()
                self.emit(op_tok.token_type, temp, current, right)
                current = temp
                j += 2
            # Final assignment
            self.emit('ATT', var_name, current, 'NONE')

        # Skip the semicolon
        return i + 1

    # def _handle_if(self, tokens: List[Lexeme], i: int, end_label: str) -> int:
    def _handle_if(self, tokens: List[Lexeme], i: int, end_label: str = None) -> int:

        left = tokens[i + 1].value
        op = tokens[i + 2].token_type
        right = tokens[i + 3].value
        temp = self.new_temp()
        self.emit(op, left, right, temp)

        true_label = self.new_label()
        false_label = self.new_label()
        if not end_label:
            end_label = self.new_label()

        self.emit('IF', temp, true_label, false_label)

        # Parte do THEN
        self.emit('LABEL', true_label, 'NONE', 'NONE')
        i += 4  # pula IF condicional
        if tokens[i].token_type == 'THEN':
            i += 1

        # Verifica se o THEN começa com BEGIN
        if tokens[i].token_type == 'BEGIN':
            i += 1
            while tokens[i].token_type != 'END':
                i = self._handle_command(tokens, i)
            i += 1  # pula END
            if tokens[i].token_type == 'SEMICOLON':
                i += 1
        else:
            i = self._handle_command(tokens, i)

        self.emit('JUMP', end_label, 'NONE', 'NONE')
        self.emit('LABEL', false_label, 'NONE', 'NONE')

        # Parte do ELSE IF
        if i < len(tokens) and tokens[i].token_type == 'ELSE':
            i += 1
            if i < len(tokens) and tokens[i].token_type == 'IF':
                return self._handle_if(tokens, i, end_label)

            # Parte do ELSE normal
            if tokens[i].token_type == 'BEGIN':
                i += 1
                while tokens[i].token_type != 'END':
                    i = self._handle_command(tokens, i)
                i += 1  # pula END
                if tokens[i].token_type == 'SEMICOLON':
                    i += 1
            else:
                i = self._handle_command(tokens, i)

        self.emit('LABEL', end_label, 'NONE', 'NONE')
        return i

    def _handle_while(self, tokens: List[Lexeme], i: int) -> int:
        start_label = self.new_label()
        true_label = self.new_label()
        end_label = self.new_label()

        self.emit('LABEL', start_label, 'NONE', 'NONE')

        # Exemplo: WHILE <left> <op> <right> DO ...
        left = tokens[i + 1].value
        op = tokens[i + 2].token_type
        right = tokens[i + 3].value

        temp = self.new_temp()
        self.emit(op, left, right, temp)

        self.emit('IF', temp, true_label, end_label)

        self.emit('LABEL', true_label, 'NONE', 'NONE')
        i += 4  # pula WHILE + condicional
        if tokens[i].token_type == 'DO':
            i += 1

        if tokens[i].token_type == 'BEGIN':
            i += 1
            while tokens[i].token_type != 'END':
                i = self._handle_command(tokens, i)
            i += 1  # pula END
            if i < len(tokens) and tokens[i].token_type == 'SEMICOLON':
                i += 1
        else:
            i = self._handle_command(tokens, i)

        self.emit('JUMP', start_label, 'NONE', 'NONE')
        self.emit('LABEL', end_label, 'NONE', 'NONE')

        return i

    def _handle_for(self, tokens: List[Lexeme], i: int) -> int:
        var_name = tokens[i + 1].value  # variável de controle
        assign_token = tokens[i + 2]
        start_value = tokens[i + 3].value  # valor inicial

        # Inicialização da variável de controle
        self.emit('ATT', var_name, start_value, 'NONE')

        direction = tokens[i + 4].token_type  # TO ou DOWNTO
        end_value = tokens[i + 5].value

        start_label = self.new_label()
        body_label = self.new_label()
        end_label = self.new_label()

        self.emit('LABEL', start_label, 'NONE', 'NONE')

        # Verifica a condição do loop
        temp = self.new_temp()
        if direction == 'TO':
            self.emit('LE', var_name, end_value, temp)
        elif direction == 'DOWNTO':
            self.emit('GE', var_name, end_value, temp)

        self.emit('IF', temp, body_label, end_label)

        # Corpo do laço
        self.emit('LABEL', body_label, 'NONE', 'NONE')
        i += 6
        if tokens[i].token_type == 'DO':
            i += 1

        if tokens[i].token_type == 'BEGIN':
            i += 1
            while tokens[i].token_type != 'END':
                i = self._handle_command(tokens, i)
            i += 1  # END
            if i < len(tokens) and tokens[i].token_type == 'SEMICOLON':
                i += 1
        else:
            i = self._handle_command(tokens, i)

        # Incremento ou decremento
        one = '1'
        temp2 = self.new_temp()
        if direction == 'TO':
            self.emit('ADD', var_name, one, temp2)
        else:
            self.emit('SUB', var_name, one, temp2)
        self.emit('ATT', var_name, temp2, 'NONE')

        self.emit('JUMP', start_label, 'NONE', 'NONE')
        self.emit('LABEL', end_label, 'NONE', 'NONE')

        return i

    def _handle_boolean_expression(self, tokens: List[Lexeme], i: int) -> Tuple[str, int]:
        """
        Trata expressões booleanas com NOT, AND, OR.
        Retorna (temp_name, nova_posição).
        """
        if tokens[i].token_type == 'NOT':
            op1 = tokens[i + 1].value
            temp = self.new_temp()
            self.emit('NOT', temp, op1, 'NONE')
            return temp, i + 2
        else:
            op1 = tokens[i].value
            op = tokens[i + 1].token_type
            op2 = tokens[i + 2].value
            temp = self.new_temp()
            if op in ('AND', 'OR'):
                self.emit(op, temp, op1, op2)
                return temp, i + 3
            # não era boolean expressão
            return op1, i + 1

    def _handle_command(self, tokens: List[Lexeme], i: int) -> int:
        tok = tokens[i]

        if tok.token_type in ('READLN', 'READ'):
            arg = tokens[i+2].value if tokens[i+1].token_type == 'LPAREN' else tokens[i+1].value
            self.emit('CALL', 'READ', arg, 'NONE')
            self.emit('CALL', 'WRITE', '\n', 'NONE')
            return i + 3

        elif tok.token_type in ('WRITELN', 'WRITE'):
            arg = tokens[i+2].value if tokens[i+1].token_type == 'LPAREN' else tokens[i+1].value
            self.emit('CALL', 'WRITE', arg, 'NONE')
            if tok.token_type == 'WRITELN':
                self.emit('CALL', 'WRITE', '\n', 'NONE')
            return i + 3

        elif tok.token_type == 'IDENTIFIER' and tokens[i+1].token_type == 'ASSIGN':
            var_name = tok.value
            i += 2

            # Boolean expressions: NOT x; a AND b; m OR n
            if tokens[i].token_type == 'NOT' or \
               (i+2 < len(tokens) and tokens[i+1].token_type in ('AND', 'OR')):
                temp, i = self._handle_boolean_expression(tokens, i)
                self.emit('ATT', var_name, temp, 'NONE')
                return i

            # Arithmetic assignment
            left = tokens[i].value
            i += 1
            if i < len(tokens) and tokens[i].token_type in ('ADD', 'SUB', 'MUL', 'DIV'):
                op = tokens[i].token_type
                i += 1
                right = tokens[i].value
                temp = self.new_temp()
                self.emit(op, left, right, temp)
                self.emit('ATT', var_name, temp, 'NONE')
                return i + 1
            else:
                self.emit('ATT', var_name, left, 'NONE')
                return i

        else:
            return i + 1

    def _handle_statement(self, tokens: List[Lexeme], i: int) -> int:
        tok = tokens[i]
        # Variable assignment
        if tok.token_type == 'IDENTIFIER':
            return self._handle_assignment(tokens, i)

        # I/O calls
        if tok.token_type in ('READLN', 'READ'):
            arg = tokens[i+1].value
            self.emit('CALL', 'READ', arg, 'NONE')
        elif tok.token_type in ('WRITELN', 'WRITE'):
            arg_index = i+1
            if tokens[arg_index].token_type == 'LPAREN':
                arg_index += 1
            arg = tokens[arg_index].value
            self.emit('CALL', 'WRITE', arg, 'NONE')
            if tok.token_type == 'WRITELN':
                self.emit('CALL', 'WRITE', '\n', 'NONE')

        # Skip tokens until semicolon
        while i < len(tokens) and tokens[i].token_type != 'SEMICOLON':
            i += 1
        return i + 1

    def save_to_file(self, filepath: str):
        """Write the intermediate code instructions to a file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            for idx, inst in enumerate(self.instructions, start=1):
                op, a1, a2, res = inst
                f.write(f"{idx:02} - ({op}, {a1}, {a2}, {res})\n")

    def print_instructions(self):
        for idx, inst in enumerate(self.instructions, start=1):
            print(f"{idx:02} - {inst}")
