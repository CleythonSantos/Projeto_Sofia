# Projeto_Sofia-Compet_Médio
É um curso que ensina técnicas de aprendizagem sobre python e demais tecnologias...

Link do Colab de todos os exercicios passado nas aulas:
https://colab.research.google.com/drive/1UR0vndY5eYrmfQ9YOXTdjxjRbqJMSObx#scrollTo=NHS7D3LsImWY

Nesse Projeto, "Sofia - Compet Médio", como minha certificação de aprendizado do "MÓDULO 1", Desenvolvi um sistema de boletim escolar em Python, capaz de cadastrar, listar, alterar e excluir alunos, armazenando os dados em arquivo .txt para persistência. O projeto calcula automaticamente a média das notas, determina a situação do aluno (Aprovado, Recuperação ou Reprovado) e exibe tudo em formato tabular no terminal. Implementei validações para matrícula, nome e notas, além de um menu interativo que facilita o uso por qualquer pessoa, simulando um sistema simples de gestão escolar.

EducaIA - Plataforma Concurseiro com IA

O EducaIA é uma plataforma desenvolvida em Python com Streamlit para auxiliar estudantes e concurseiros em sua preparação.
O sistema integra banco de dados, geração de textos e análise de documentos com IA generativa via Groq.

O sistema permite:

👤 Gerenciar usuários (cadastro e login com banco SQLite).

📊 Dashboard interativo com progresso de estudos por matéria.

📂 Upload de arquivos CSV com questões ou materiais.

🖋️ Geração de textos com IA (Groq).

📄 Leitura de PDFs com perguntas e respostas automáticas usando IA.

💻 Tecnologias usadas

Python 3.11+

Streamlit

SQLite (banco local educaia.db)

Pandas

Plotly (para gráficos interativos)

Groq (IA generativa)

PyPDF (para leitura de PDFs)

📁 Estrutura do projeto
educaia/
├─ app.py              # Arquivo principal do Streamlit
├─ educaia.db          # Banco de dados SQLite
└─ uploads/            # (opcional) pasta para arquivos enviados

⚙️ Configuração do ambiente
Criar o ambiente virtual:
python -m venv venv

Ativar o ambiente:

Windows

.\venv\Scripts\activate


Linux / Mac

source venv/bin/activate

Atualizar o pip:
python -m pip install --upgrade pip

Instalar dependências:
pip install streamlit pandas plotly sqlite3 groq pypdf

Gerar requirements.txt (opcional):
pip freeze > requirements.txt

🚀 Rodando o projeto

Verifique se o arquivo educaia.db existe.

Se não existir, será criado automaticamente.

Execute o Streamlit:

streamlit run app.py


Navegue pelo menu lateral:

Login / Cadastro: criação de conta e autenticação de usuário.

Dashboard: progresso de estudos por matéria (métricas + gráficos).

Upload: carregar CSVs com materiais e visualizar dados.

Geração de Texto: criar textos educativos com IA (requer chave Groq).

Leitura de PDF: enviar PDFs e fazer perguntas sobre o conteúdo (requer chave Groq).

📊 Funcionalidades do Dashboard

Métricas rápidas de progresso por matéria.

Gráficos interativos (concluído x a estudar).

Visualização amigável do progresso do aluno.

Exemplo de código para gráfico:

df_prog = pd.DataFrame({
    "Matéria": materias,
    "Concluído": concluido,
    "A Estudar": a_estudar
})

fig_prog = px.bar(
    df_prog, x="Matéria", y=["Concluído", "A Estudar"],
    text_auto=True, labels={"value": "Conteúdos", "variable": "Status"},
    color_discrete_sequence=["#2ca02c", "#ff7f0e"],
    title="📊 Progresso por Matéria"
)

st.plotly_chart(fig_prog, use_container_width=True)

📝 Observações

A tabela usuarios é criada automaticamente no banco educaia.db.

Senhas não possuem criptografia neste protótipo (apenas uso didático).

Para reiniciar o banco, basta deletar educaia.db e rodar o app novamente.

A integração com IA requer chave da Groq fornecida pelo usuário.

🔗 Referências

Streamlit

Plotly

Groq AI

📸 Sugestões de melhoria

Adicionar criptografia de senhas (bcrypt).

Criar perfis diferentes (admin x aluno).

Salvar progresso real do usuário no banco de dados.

Melhorar UI com componentes extras do Streamlit ou Plotly Dash.
