class Lexeme:
    def __init__(self, token_type, value, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Lexeme(token_type='{self.token_type}', value='{self.value}', line={self.line}, column={self.column})"