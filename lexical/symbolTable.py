class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, lexeme):
        if lexeme.value not in self.symbols:
            self.symbols[lexeme.value] = lexeme

    def __contains__(self, value):
        return value in self.symbols

    def __repr__(self):
        return f"SymbolTable({self.symbols})"