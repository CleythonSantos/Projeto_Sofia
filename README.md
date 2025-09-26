# Projeto_Sofia-Compet_Médio
É um curso que ensina técnicas de aprendizagem sobre python e demais tecnologias...

Link do Colab de todos os exercicios passado nas aulas:
https://colab.research.google.com/drive/1UR0vndY5eYrmfQ9YOXTdjxjRbqJMSObx#scrollTo=NHS7D3LsImWY

Nesse Projeto, "Sofia - Compet Médio", como minha certificação de aprendizado do "MÓDULO 1", Desenvolvi um sistema de boletim escolar em Python, capaz de cadastrar, listar, alterar e excluir alunos, armazenando os dados em arquivo .txt para persistência. O projeto calcula automaticamente a média das notas, determina a situação do aluno (Aprovado, Recuperação ou Reprovado) e exibe tudo em formato tabular no terminal. Implementei validações para matrícula, nome e notas, além de um menu interativo que facilita o uso por qualquer pessoa, simulando um sistema simples de gestão escolar.

---

## 📚 EducaIA - Plataforma Concurseiro com IA

O **EducaIA** é um projeto em Python utilizando **Streamlit** para criar um sistema interativo de apoio a concurseiros, integrado com **IA generativa via Groq**. O sistema permite:

- Cadastrar usuários em bancos locais.

- Gerenciar conteúdos e progresso de estudos.

- Consultar e gerar materiais educativos usando IA.

- Visualizar um dashboard com métricas e gráficos.

- Ler documentos PDF e CSV com suporte a perguntas e respostas.

  ---

## 💻 Tecnologias usadas

- Python 3.11+

- Streamlit

- SQLite (banco local `educaia.db e concurseiro.db`)

- Pandas

- PyPDF2 (para leitura de PDFs)

- Plotly (para gráficos)

- Groq (IA generativa)

- OpenAI / LangChain / LangChain-Groq (IA generativa)
  
- FAISS (indexação vetorial para documentos)

  ---

📁 Estrutura do projeto

```
educaia/
├─ app.py             # Arquivo principal do Streamlit
├─ concurseiro.db     # Banco de dados auxiliar em SQLite
├─ educaia.db         # Banco de dados principal em SQLite
└─ requirements.txt   # Dependências do projeto
```

---

## ⚙️ Configuração do ambiente

1. Criar o ambiente virtual:

```bash
python -m venv venv
```

2. Ativar o ambiente:

**Windows**

```bash
.\venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

3. Atualizar o pip:

```bash
python.exe -m pip install --upgrade pip
```

4. Instalar as dependências:

```bash
pip install streamlit
pandas
plotly
groq
pypdf
```

5. Gerar `requirements.txt` (opcional):

```bash
pip freeze > requirements.txt
```

---

## 🚀 Rodando o projeto

Certifique-se de que o arquivo `data/escola.db` não está corrompido.

Se estiver, delete o arquivo e o banco será recriado automaticamente.

Rodar o Streamlit:

```bash
streamlit run app.py
```

---

Navegue pelo menu lateral:

- **Login/Cadastro:** Gerenciar usuários.

- **Dashboard:** Visualizar métricas e gráficos de desempenho.

- **Upload:** Carregar arquivos CSV para análise.

- **Conteúdo com IA:** Gerar resumos e materiais de estudo. **Requer chave Groq configurada.**

- **Documentos:** Enviar PDFs e consultar usando IA. **Requer chave Groq configurada.**

  ---

## 📊 Funcionalidades do Dashboard

- Total de usuários cadastrados.

- Progresso por matérias.

- Gráficos interativos de desempenho.

- Tabelas de acompanhamento dos estudos.

  ---

Exemplo de código para gráfico de progresso:

```python
df_usuarios = pd.read_sql("SELECT nome, progresso FROM usuarios", conn)
if not df_usuarios.empty:
    st.subheader("Progresso dos Usuários")
    st.bar_chart(df_usuarios.set_index('nome')['progresso'])
else:
    st.info("Nenhum usuário cadastrado ainda para gerar gráfico.")
```

---

## 📝 Observações

- Senhas não estão criptografadas (uso didático).

- Para reiniciar os bancos, basta apagar educaia.db e concurseiro.db.

- A integração com IA requer chave Groq fornecida pelo usuário na interface.

---

## 🔗 Referências

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Groq AI](https://groq.com/)

---

## 📸 Sugestões de melhoria

- Adicionar filtros interativos no dashboard (por matérias, tempo de estudo e progresso).

- Criar gráficos comparativos entre usuários.

- Incluir exportação dos relatórios em PDF ou Excel.

- Melhorar a interface com Streamlit Components ou bibliotecas como Plotly.

  ---
  
