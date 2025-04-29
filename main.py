import sys
import os
from lexical.lexicalAnalysis import LexicalAnalysis

def processar_arquivo(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
        return

    print(f"\nArquivo: {os.path.basename(caminho_arquivo)}\n")
    
    with open(caminho_arquivo, "r", encoding="latin-1") as file:
        source_code = file.read()

    lexer = LexicalAnalysis(source_code)
    tokens = lexer.analyze()

    for token in tokens:
        print(token)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Caminho: python main.py <caminho-do-arquivo>")
    else:
        caminho_arquivo = sys.argv[1]
        processar_arquivo(caminho_arquivo)
