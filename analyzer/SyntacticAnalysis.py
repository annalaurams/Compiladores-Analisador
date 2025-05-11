from analyzer.lexeme import Lexeme  
class SyntaxError(Exception):
    def __init__(self, message, token):
        self.token = token
        self.line = token.line
        self.column = token.column
        super().__init__(f"{message} at line {self.line}, column {self.column}")

class SyntacticAnalysis:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        print("\n_______________________________________________________________________________________________________________\n")
        print("\nParsing program\n")
        self.program()

    def expect(self, expected_type):
        if not self.match(expected_type):
            current_token = self.tokens[self.current] if self.current < len(self.tokens) else None
            if current_token:
                raise SyntaxError(
                    f"Expected {expected_type}, but got {current_token.token_type} ('{current_token.value}')",
                    current_token
                )
            else:
                raise SyntaxError(f"Unexpected end of input, expected {expected_type}", Lexeme(expected_type, "", -1, -1))

    def match(self, expected_type):
        if self.current < len(self.tokens) and self.tokens[self.current].token_type == expected_type:
            print(f"Matched {expected_type}: {self.tokens[self.current].value}")
            self.current += 1
            return True
        return False

    def program(self):
        print("Entering <program>")
        self.expect("PROGRAM")
        self.expect("IDENTIFIER")
        self.expect("SEMICOLON")
        self.declarations()
        self.expect("BEGIN")
        self.stmtList()
        self.expect("END")
        self.expect("DOT")
        print("Exiting <program>")

    def declarations(self):
        print("Entering <declarations>")
        self.expect("VAR")
        self.declaration()
        while self.current < len(self.tokens) and self.tokens[self.current].token_type == "IDENTIFIER":
            self.declaration()
        print("Exiting <declarations>")

    def declaration(self):
        print("Entering <declaration>")
        self.listaIdent()
        self.expect("COLON")
        self.type()
        self.expect("SEMICOLON")
        print("Exiting <declaration>")

    def listaIdent(self):
        print("Entering <listaIdent>")
        self.expect("IDENTIFIER")
        while self.match("COMMA"):
            self.expect("IDENTIFIER")
        print("Exiting <listaIdent>")

    def type(self):
        print("Entering <type>")
        if not self.match("INTEGER"):
            if not self.match("REAL"):
                self.expect("STRING")
        print("Exiting <type>")

    def stmtList(self):
        print("Entering <stmtList>")
        while self.current < len(self.tokens):
            if self.tokens[self.current].token_type in {"END", "ELSE", "DOT"}:
                break
            self.stmt()
        print("Exiting <stmtList>")

    def stmt(self):
        print(f"Entering <stmt> with token {self.tokens[self.current].token_type}")
        token = self.tokens[self.current].token_type
        if token == "FOR":
            self.forStmt()
        elif token in {"READ", "WRITE", "READLN", "WRITELN"}:
            self.ioStmt()
        elif token == "WHILE":
            self.whileStmt()
        elif token == "IF":
            self.ifStmt()
        elif token == "BREAK":
            self.expect("BREAK")
            self.expect("SEMICOLON")
        elif token == "CONTINUE":
            self.expect("CONTINUE")
            self.expect("SEMICOLON")
        elif token == "SEMICOLON":
            self.expect("SEMICOLON")
        elif token == "BEGIN":
            self.bloco()
        elif token == "IDENTIFIER":
            self.atrib()
            self.expect("SEMICOLON")
        else:
            raise SyntaxError("Unexpected token in statement", self.tokens[self.current])
        print("Exiting <stmt>")

    def bloco(self):
        print("Entering <bloco>")
        self.expect("BEGIN")
        self.stmtList()
        self.expect("END")
        self.expect("SEMICOLON")
        print("Exiting <bloco>")

    def forStmt(self):
        print("Entering <forStmt>")
        self.expect("FOR")
        self.atrib()
        self.expect("TO")
        if not self.match("IDENTIFIER"):
            self.expect("DECIMAL")
        self.expect("DO")
        self.stmt()
        print("Exiting <forStmt>")

    def ioStmt(self):
        print("Entering <ioStmt>")
        token = self.tokens[self.current].token_type
        self.current += 1 
        self.expect("LPAREN")
        if token in {"READ", "READLN"}:
            self.expect("IDENTIFIER")
        else:
            self.outList()
        self.expect("RPAREN")
        self.expect("SEMICOLON")
        print("Exiting <ioStmt>")

    def outList(self):
        print("Entering <outList>")
        self.out()
        while self.match("COMMA"):
            self.out()
        print("Exiting <outList>")

    def out(self):
        if not self.match("STRING"):
            if not self.match("IDENTIFIER"):
                if not self.match("DECIMAL"):
                    self.expect("FLOAT")

    def whileStmt(self):
        print("Entering <whileStmt>")
        self.expect("WHILE")
        self.expr()
        self.expect("DO")
        self.stmt()
        print("Exiting <whileStmt>")

    def ifStmt(self):
        print("Entering <ifStmt>")
        self.expect("IF")
        self.expr()
        self.expect("THEN")
        self.stmt()
        if self.match("ELSE"):
            self.stmt()
        print("Exiting <ifStmt>")

    def atrib(self):
        print("Entering <atrib>")
        self.expect("IDENTIFIER")
        self.expect("ASSIGN")
        self.expr()
        print("Exiting <atrib>")

    def expr(self):
        self.orExpr()

    def orExpr(self):
        self.andExpr()
        while self.match("OR"):
            self.andExpr()

    def andExpr(self):
        self.notExpr()
        while self.match("AND"):
            self.notExpr()

    def notExpr(self):
        if self.match("NOT"):
            self.notExpr()
        else:
            self.rel()

    def rel(self):
        self.add()
        while self.match("EQ") or self.match("NEQ") or self.match("LT") or self.match("LTE") or self.match("GT") or self.match("GTE"):
            self.add()

    def add(self):
        self.mult()
        while self.match("ADD") or self.match("SUB"):
            self.mult()

    def mult(self):
        self.uno()
        while self.match("MUL") or self.match("DIV") or self.match("MOD") or self.match("INT_DIV"):
            self.uno()

    def uno(self):
        if self.match("ADD") or self.match("SUB"):
            self.uno()
        else:
            self.fator()

    def fator(self):
        if not self.match("DECIMAL"):
            if not self.match("FLOAT"):
                if not self.match("IDENTIFIER"):
                    if self.match("LPAREN"):
                        self.expr()
                        self.expect("RPAREN")
                    else:
                        self.expect("STRING")

