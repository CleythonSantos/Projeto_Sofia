import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
from groq import Groq
from pypdf import PdfReader

# Configurações iniciais
st.set_page_config(page_title="ETE PD - Sistema de Cadastro + IA", layout="wide")

# Banco de dados SQLite
def init_db():
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            data_cadastro TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_usuario(nome, email, senha):
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO usuarios (nome, email, senha, data_cadastro) VALUES (?, ?, ?, ?)", 
                   (nome, email, senha, data))
    conn.commit()
    conn.close()

def get_usuarios():
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Inicializa o banco
init_db()

# Menu lateral
menu = st.sidebar.radio("Escolha:", ["Cadastro", "Upload", "Gráficos", "Geração de Texto", "Leitura de PDF"])

# Cabeçalho geral
st.markdown("<h1 style='text-align: center;'>ETE PD - Sistema de Cadastro + IA</h1>", unsafe_allow_html=True)
st.write("Bem-vindo! Aqui você pode cadastrar usuários, enviar arquivos, gerar gráficos e usar inteligência artificial para gerar textos ou interagir com PDFs.")

# Página 1 - Cadastro
if menu == "Cadastro":
    st.markdown("## Cadastro de Usuários")

    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar"):
        if nome and email and senha:
            add_usuario(nome, email, senha)
            st.success("Cadastro realizado com sucesso!")
        else:
            st.warning("Preencha todos os campos antes de cadastrar.")

    if st.checkbox("Mostrar cadastros"):
        usuarios = get_usuarios()
        if usuarios:
            df = pd.DataFrame(usuarios, columns=["ID", "Nome", "Email", "Senha", "Data Cadastro"])
            st.dataframe(df)
            st.download_button("Baixar usuários em CSV", df.to_csv(index=False), "usuarios.csv", "text/csv")
        else:
            st.info("Nenhum usuário cadastrado.")

# Página 2 - Upload
elif menu == "Upload":
    st.markdown("## Upload de Arquivos")

    uploaded_file = st.file_uploader("Envie um arquivo CSV", type=["csv"])
    if uploaded_file is not None:
        df_upload = pd.read_csv(uploaded_file)
        st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")
        st.dataframe(df_upload)

# Página 3 - Gráficos
    elif menu == "Gráficos":
    st.markdown("## Gráficos de Usuários")

    usuarios = get_usuarios()
    if usuarios:
        df = pd.DataFrame(usuarios, columns=["ID", "Nome", "Email", "Senha", "Data Cadastro"])

        # Cards principais
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Usuários", len(df))
        col2.metric("Último Cadastro", df["Data Cadastro"].max())
        col3.metric("Domínios de Email", df["Email"].str.split("@").str[1].nunique())

        # Gráfico de usuários por domínio de email
        df["Dominio"] = df["Email"].str.split("@").str[1]
        dominio_count = df["Dominio"].value_counts().reset_index()
        dominio_count.columns = ["Dominio", "Quantidade"]

        fig1 = px.bar(dominio_count, x="Dominio", y="Quantidade", title="Usuários por domínio de e-mail", text="Quantidade")
        st.plotly_chart(fig1, use_container_width=True)

        # Gráfico de evolução dos cadastros ao longo do tempo
        df["Data Cadastro"] = pd.to_datetime(df["Data Cadastro"])
        cadastros_por_dia = df.groupby(df["Data Cadastro"].dt.date).size().reset_index(name="Quantidade")

        fig2 = px.line(cadastros_por_dia, x="Data Cadastro", y="Quantidade", markers=True, title="Evolução de cadastros")
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("Nenhum dado disponível para gerar gráficos.")

# Página 4 - Geração de Texto com IA
    elif menu == "Geração de Texto":
    st.markdown("## Geração de Textos com IA")

    chave = st.text_input("Digite sua chave da Groq", type="password")
    modelo = st.selectbox("Escolha o modelo", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ])
    titulo = st.text_input("Título do Texto")
    tema = st.text_area("Tema/Assunto")

    if st.button("Gerar Texto"):
        if chave and tema:
            try:
                client = Groq(api_key=chave)

                resposta = client.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": "Você é um assistente que escreve textos claros e bem estruturados."},
                        {"role": "user", "content": f"Escreva um texto sobre: {tema}"}
                    ],
                    max_tokens=600
                )

                texto_final = resposta.choices[0].message.content

                st.success("Texto gerado com sucesso!")
                st.write(f"**Título:** {titulo if titulo else 'Sem título'}")
                st.markdown("---")
                st.write(texto_final)

                st.download_button("Baixar Texto", texto_final, "texto_gerado.txt")

            except Exception as e:
                st.error(f"Erro ao gerar texto: {e}")
        else:
            st.warning("Preencha todos os campos antes de gerar o texto.")

# Página 5 - Leitura de PDF com IA
    elif menu == "Leitura de PDF":
    st.markdown("## Leitura de PDF com IA")

    chave = st.text_input("Digite sua chave da Groq", type="password")
    modelo = st.selectbox("Escolha o modelo", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ])

    uploaded_file = st.file_uploader("Envie um PDF", type=["pdf"])

    if uploaded_file is not None:
        st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")

        # Ler texto do PDF
        pdf_reader = PdfReader(uploaded_file)
        texto_pdf = ""
        for page in pdf_reader.pages:
            texto_pdf += page.extract_text() + "\n"

        st.subheader("Pré-visualização do Conteúdo")
        st.text_area("Texto extraído do PDF:", texto_pdf[:2000], height=200)

        pergunta = st.text_input("Digite uma pergunta sobre o PDF")

        if st.button("Perguntar à IA"):
            if chave and pergunta:
                try:
                    client = Groq(api_key=chave)

                    resposta = client.chat.completions.create(
                        model=modelo,
                        messages=[
                            {"role": "system", "content": "Você é um assistente especializado em responder perguntas sobre documentos PDF."},
                            {"role": "user", "content": f"Documento:\n{texto_pdf[:4000]}"},
                            {"role": "user", "content": f"Pergunta: {pergunta}"}
                        ],
                        max_tokens=500
                    )

                    resposta_final = resposta.choices[0].message.content
                    st.markdown("### Resposta da IA:")
                    st.write(resposta_final)

                except Exception as e:
                    st.error(f"Erro ao processar pergunta: {e}")
            else:
                st.warning("Digite sua chave da Groq e uma pergunta antes de continuar.")
