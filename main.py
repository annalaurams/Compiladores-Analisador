import sys
import os
from analyzer.lexicalAnalysis import LexicalAnalysis
from analyzer.SyntacticAnalysis import SyntacticAnalysis
from analyzer.intermediate_code_generator import IntermediateCodeGenerator

def processar_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
        return

    print(f"\nArquivo: {os.path.basename(caminho_arquivo)}\n")
    
    with open(caminho_arquivo, "r", encoding="latin-1") as file:
        source_code = file.read()

    lexer = LexicalAnalysis(source_code)
    tokens = lexer.analyze()

    print("\nTokens gerados:")
    for token in tokens:
        print(token)

    try:
        parser = SyntacticAnalysis(tokens)
        parser.parse()
        print("\n Análise sintática concluída!\n")
    except SyntaxError as e:
        print(f"\n Erro de análise sintática: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho-do-arquivo>")
    else:
        caminho_arquivo = sys.argv[1]
        processar_arquivo(caminho_arquivo)
        path = sys.argv[1]
        code = open(path, encoding='latin-1').read()
        lex = LexicalAnalysis(code)
        tokens = lex.analyze()
        gen = IntermediateCodeGenerator()
        gen.generate_from_tokens(tokens)
        gen.print_instructions()