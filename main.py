import os
from lexical.lexicalAnalysis import LexicalAnalysis

def processar_arquivos(pasta):
    # Itera sobre todos os arquivos na pasta especificada
    for filename in os.listdir(pasta):
        if filename.endswith(".pas"):
            caminho_arquivo = os.path.join(pasta, filename)
            print(f"Analisando {filename}...")
            
            with open(caminho_arquivo, "r") as file:
                source_code = file.read()

            # Executa o analisador léxico
            lexer = LexicalAnalysis(source_code)
            tokens = lexer.analyze()

            # Exibe os tokens encontrados
            for token in tokens:
                print(token)
            print("\n")

if __name__ == "__main__":
    # Define a pasta onde estão os arquivos .pas
    pasta_codigos = "codigos_pascal"
    
    if os.path.exists(pasta_codigos):
        processar_arquivos(pasta_codigos)
    else:
        print(f"A pasta '{pasta_codigos}' não foi encontrada. Crie-a e adicione arquivos .pas para testar.")


#Program nn ta sendo identificado como palavra rerservada 
#fazer caracter por caracter e identificar o ;
#Erros
# tratamento dos numeros
#   