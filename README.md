<h1 align="center" font-size="200em"><b>📘 Compilador Pascal--: Analisador Léxico e Sintático</b></h1>

<div align = "center" >

[![requirement](https://img.shields.io/badge/IDE-Visual%20Studio%20Code-informational)](https://code.visualstudio.com/docs/?dv=linux64_deb)
![Linguagem](https://img.shields.io/badge/Linguagem-Python-orange)
</div>

## ✒️ Descrição
Este projeto é a implementação das etapas **1 e 2 do Trabalho Prático** da disciplina de Compiladores. Foi desenvolvido as etapas de **análise léxica** e **análise sintática** para a linguagem fictícia Pascal--., uma versão simplificada da linguagem Pascal.

## 🧠 Objetivo

Implementar um compilador parcial para Pascal--, realizando a leitura de um código-fonte `.pmm` e analisando se ele é válido segundo as regras léxicas e sintáticas da linguagem.


## 📦 Módulos do Projeto

### 🔹 Módulo 1 — Analisador Léxico

Identifica e classifica os **tokens** do código-fonte (palavras-chave, operadores, símbolos, etc.) e informa a **linha e coluna** de cada item.

**Exemplo de saída:**
```
Token: KEYWORD, Lexema: program, Linha: 1, Coluna: 1
Token: IDENTIFIER, Lexema: exemplo, Linha: 1, Coluna: 9
```

**Erros léxicos** também são detectados e informados com a posição do erro.

---

### 🔸 Módulo 2 — Analisador Sintático

Verifica se os tokens formam uma estrutura sintaticamente válida, com base na **gramática da linguagem Pascal--**.

**Exemplo de erro sintático:**
```
Erro sintático na linha 10, coluna 5: esperado 'end' antes de 'else'
```

## 🗂 Estrutura do Projeto

- `main.py`: Ponto de entrada do projeto (executa analisador léxico e sintático).
- `lexical/`: Código do analisador léxico.
- `syntactic/`: Código do analisador sintático.
- `lista1/`: Arquivos de teste `.pmm`.
- 

## ⚙️ Como Executar

1. Certifique-se de ter **Python 3** instalado.
2. No terminal, execute:

```bash
python3 main.py codigos_pascal/<arquivo>.pmm
```

3. O analisador vai imprimir os tokens encontrados e a análise sintárica é feita, em caso de erros é exibido o motivo do erro e a linha e coluna do arquivo `.pmm` em que houve o erro
4. Para limpar o terminal basta rodar o comando: `clear`
   
## ✅ Funcionalidades Implementadas

- Identificação correta de todos os tokens da linguagem Pascal--
- Detecção de tokens inválidos com mensagens de erro e posição no código
- Entrada via linha de comando com nome do arquivo
- Modularização do código para facilitar manutenção e legibilidade
- Analisador sintático para verificar a estrutura correta do código Pascal, com detecção de erros de sintaxe com mensagens detalhadas.

<!-- 
## 📦 Resultado Esperado

Ao executar o analisador em um código `.pmm`, o retorno será uma lista de tokens válidos encontrados, ou uma mensagem de erro informando onde há um token inválido. Exemplo:

```
Token: KEYWORD, Lexema: program, Linha: 1, Coluna: 1  
Token: IDENTIFIER, Lexema: exemplo, Linha: 1, Coluna: 9  
...  
Erro: Token inválido "$" na linha 5, coluna 12
```
-->
## 📌 Conclusão

O projeto foi dividido em etapas para facilitar o aprendizado e a organização. Primeiro, implementamos a análise léxica, depois partimos para a análise sintática. Isso nos ajudou a compreender melhor como um compilador identifica e interpreta o código-fonte em etapas bem definidas.


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
