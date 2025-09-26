# Projeto_Sofia-Compet_Médio
É um curso que ensina técnicas de aprendizagem sobre python e demais tecnologias...

Link do Colab de todos os exercicios passado nas aulas:
https://colab.research.google.com/drive/1UR0vndY5eYrmfQ9YOXTdjxjRbqJMSObx#scrollTo=NHS7D3LsImWY

Nesse Projeto, "Sofia - Compet Médio", como minha certificação de aprendizado do "MÓDULO 1", Desenvolvi um sistema de boletim escolar em Python, capaz de cadastrar, listar, alterar e excluir alunos, armazenando os dados em arquivo .txt para persistência. O projeto calcula automaticamente a média das notas, determina a situação do aluno (Aprovado, Recuperação ou Reprovado) e exibe tudo em formato tabular no terminal. Implementei validações para matrícula, nome e notas, além de um menu interativo que facilita o uso por qualquer pessoa, simulando um sistema simples de gestão escolar.

# 📚 EducaIA - Plataforma Concurseiro com IA  

O **EducaIA** é uma plataforma em **Python + Streamlit** voltada para concurseiros, unindo gestão de estudos e inteligência artificial com **Groq**.  

O sistema permite:  
- 👤 Cadastro e login de usuários (SQLite).  
- 📊 Dashboard com progresso de estudos.  
- 📂 Upload de arquivos CSV com questões/materiais.  
- 🖋️ Geração de textos com IA (Groq).  
- 📄 Leitura de PDFs com perguntas e respostas automáticas.  

---

## 💻 Tecnologias usadas  
- Python 3.11+  
- Streamlit  
- SQLite (`educaia.db` e `concurseiro.db`)  
- Pandas  
- Plotly  
- Groq (IA generativa)  
- PyPDF  

---

## 📁 Estrutura do projeto real  
educaia/
├─ app.py              # Arquivo principal do Streamlit
├─ concurseiro.db      # Banco SQLite auxiliar
├─ educaia.db          # Banco SQLite principal
└─ requirements.txt    # Dependências do projeto

---

## ⚙️ Configuração do ambiente
Criar ambiente virtual:
python -m venv venv

Ativar ambiente:

Windows

.\venv\Scripts\activate
