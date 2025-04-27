<h1 align="center" font-size="200em"><b>📘 Analisador Léxico - Compiladores</b></h1>

<div align = "center" >

[![requirement](https://img.shields.io/badge/IDE-Visual%20Studio%20Code-informational)](https://code.visualstudio.com/docs/?dv=linux64_deb)
![Linguagem](https://img.shields.io/badge/Linguagem-Python-orange)
</div>

## ✒️ Descrição
Este projeto é a implementação do **Trabalho Prático 01** da disciplina de Compiladores. Foi desenvolvido um **analisador léxico** para uma linguagem chamada **Pascal--**, uma versão simplificada da linguagem Pascal.

## 🧠 Objetivo

Criar um programa capaz de **ler arquivos .pmm escritos em Pascal--** e identificar todos os **tokens válidos**, retornando:

- O tipo do token (ex: palavra reservada, operador, número, etc.)
- O lexema (valor do token no código)
- Linha e coluna onde foi encontrado
- Retornado erro em casos de não reconhecimento do token retornando a linha e a coluna do problema.

## 🛠 Estrutura do Projeto

- `main.py`: Arquivo principal. Executa o analisador léxico.
- `lexical/`: Pasta com os módulos que contêm a lógica de análise léxica (reconhecimento de tokens, tratamento de erros, etc.).
- `codigos_pascal/`: Exemplos de arquivos `.pmm` escritos em Pascal-- para teste do analisador.

## 🔍 Tipos de tokens reconhecidos
Os tokens que são reconhecidos em nosso projeto são:

- **Operadores Aritméticos**: `+`, `-`, `*`, `/`, `mod`, `div`
- **Operadores Lógicos e Relacionais**: `and`, `or`, `not`, `=`, `<>`, `<`, `<=`, `>`, `>=`, `:=`
- **Palavras Reservadas**: `program`, `var`, `integer`, `real`, `string`, `begin`, `end`, `if`, `then`, `else`, `for`, `to`, `while`, `do`, `break`, `continue`, `read`, `readln`, `write`, `writeln`
- **Símbolos**: `;`, `:`, `,`, `.`, `(`, `)`
- **Strings**: delimitadas por aspas duplas (`"`)
- **Números**:
  - Octais: `0[0-7]+`
  - Decimais: `[1-9][0-9]*`
  - Hexadecimais: `0x[0-9A-F]+`
  - Flutuantes: `[0-9]+\.[0-9]*`
- **Identificadores**: Letras seguidas de letras ou dígitos
- **Comentários**: `//` ou `{ ... }`

## ⚙️ Como Executar

1. Certifique-se de ter **Python 3** instalado.
2. No terminal, execute:

```bash
python3 main.py codigos_pascal/<nome_arquivo>.pmm
```
3. O analisador vai imprimir os tokens encontrados, junto com seus lexemas, linhas e colunas.
4. Para limpar o terminal basta rodar o comando: `clear`
   
## ✅ Funcionalidades Implementadas

- Identificação correta de todos os tokens da linguagem Pascal--
- Detecção de tokens inválidos com mensagens de erro e posição no código
- Entrada via linha de comando com nome do arquivo
- Modularização do código para facilitar manutenção e legibilidade

## 📦 Resultado Esperado

Ao executar o analisador em um código `.pmm`, o retorno será uma lista de tokens válidos encontrados, ou uma mensagem de erro informando onde há um token inválido. Exemplo:

```
Token: KEYWORD, Lexema: program, Linha: 1, Coluna: 1  
Token: IDENTIFIER, Lexema: exemplo, Linha: 1, Coluna: 9  
...  
Erro: Token inválido "$" na linha 5, coluna 12
```

## 📌 Conclusão

Esse trabalho nos ajudou a entender melhor o funcionamento da parte de análise léxica em compiladores. Vimos na prática como reconhecer os elementos da linguagem, separar corretamente cada parte do código (como palavras-chave, variáveis, números etc.), lidar com erros e organizar tudo de um jeito claro no código.

## Contato
<div>
 <p align="justify"> Anna Laura Moura Santana</p>
 <a href="https://t.me/annalaurams">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:nalauramoura@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>nalauramoura@gmail.com</i>
</a>

<div>
 <br><p align="justify"> Jullia Fernandes</p>
 <a href="https://t.me/JulliaFernandes">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:julliacefet@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>julliacefet@gmail.com</i>
</a>

<div>
 <br><p align="justify"> Letícia de Oliveira</p>
 <a href="https://t.me/letolsilva">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:letolsilva22@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>letolsilva22@gmail.com</i>
</a>

<div>
 <br><p align="justify"> Thaissa Vitoria Guimarães Daldegan de Sousa</p>
 <a href="https://t.me/thaissadaldegan">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:thaissavivi@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>thaissavivi@gmail.com</i>
</a>
