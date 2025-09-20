import streamlit as st
import pandas as pd
import os

# Defina sua chave de API da Groq
os.environ["GROQ_API_KEY"] = "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"

# ✅ Import corrigido para PyPDFLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq

st.set_page_config(page_title="ETE PORTO DIGITAL - Sistema IA", layout="wide")
st.title("ETE PORTO DIGITAL - Sistema de Cadastro + IA")
st.write("Bem-vindo! Aqui você pode cadastrar usuários, enviar arquivos, gerar gráficos e usar inteligência artificial para gerar textos ou fazer perguntas sobre PDFs.")

# Menu lateral
st.sidebar.title("Menu Lateral")
pagina = st.sidebar.radio("Escolha:", ["Cadastro", "Upload", "Gráficos", "Geração de Texto", "Leitura de PDF"])

# Função para salvar dados
def salvar_dados(nome, email, senha):
    arquivo = 'cadastros.csv'
    if os.path.exists(arquivo):
        tabela = pd.read_csv(arquivo)
    else:
        tabela = pd.DataFrame(columns=['Nome', 'Email', 'Senha'])

    if email in tabela["Email"].values:
        st.warning("Este e-mail já está cadastrado.")
        return False

    tabela.loc[len(tabela)] = [nome, email, senha]
    tabela.to_csv(arquivo, index=False)
    return True

# ------------------ PÁGINAS ------------------

# CADASTRO
if pagina == "Cadastro":
    st.subheader("Cadastro de Usuários")
    with st.form("form_cadastro"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        botao = st.form_submit_button("Cadastrar")

    if botao:
        if nome and email and senha:
            if salvar_dados(nome, email, senha):
                st.success("Cadastro realizado com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos.")

    if st.checkbox("Mostrar cadastros"):
        if os.path.exists("cadastros.csv"):
            tabela = pd.read_csv("cadastros.csv")
            st.dataframe(tabela)
        else:
            st.info("Nenhum cadastro encontrado.")

# UPLOAD
elif pagina == "Upload":
    st.subheader("Upload de Arquivos")
    arquivo_csv = st.file_uploader("Envie um arquivo CSV", type="csv")
    if arquivo_csv is not None:
        tabela = pd.read_csv(arquivo_csv)
        st.dataframe(tabela)

# GRÁFICOS
elif pagina == "Gráficos":
    st.subheader("Gráficos de Usuários")
    if os.path.exists("cadastros.csv"):
        tabela = pd.read_csv("cadastros.csv")
        if not tabela.empty:
            tabela["Dominio"] = tabela["Email"].apply(lambda x: x.split("@")[-1])
            dominios = tabela["Dominio"].value_counts()
            st.bar_chart(dominios)
            st.write("Quantidade de usuários por domínio de e-mail:")
            st.dataframe(dominios)
        else:
            st.info("Ainda não há usuários cadastrados para gerar gráficos.")
    else:
        st.info("Nenhum cadastro encontrado para gerar gráficos.")

# GERAÇÃO DE TEXTO
elif pagina == "Geração de Texto":
    st.subheader("📝 Geração de Texto com IA")
    prompt_usuario = st.text_area("Digite um prompt para gerar texto:")
    if st.button("Gerar Texto"):
        if prompt_usuario:
            st.info("Gerando texto... aguarde ⏳")
            modelo = ChatGroq(model="llama3-8b-8192", temperature=0.7)
            resposta = modelo.invoke(prompt_usuario)
            st.success("Texto gerado com sucesso!")
            st.write("**Resposta da IA:**")
            st.write(resposta)
        else:
            st.warning("Digite um prompt primeiro.")

# LEITURA DE PDF (RAG)
elif pagina == "Leitura de PDF":
    st.subheader("📄 Leitura de PDF com IA (RAG)")
    pdf_file = st.file_uploader("Envie um PDF", type="pdf")
    if pdf_file:
        with open("temp.pdf", "wb") as f:
            f.write(pdf_file.read())

        st.info("Carregando e processando PDF...")
        carregador = PyPDFLoader("temp.pdf")
        documentos = carregador.load()

        separador = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        blocos = separador.split_documents(documentos)
        st.write(f"PDF dividido em {len(blocos)} blocos de texto.")

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        armazenamento_vetorial = FAISS.from_documents(blocos, embeddings)
        buscador = armazenamento_vetorial.as_retriever(search_kwargs={"k": 3})

        modelo = ChatGroq(model="llama3-8b-8192", temperature=0)
        qa_chain = RetrievalQA.from_chain_type(
            llm=modelo,
            retriever=buscador,
            chain_type="stuff",
        )

        pergunta = st.text_input("Faça uma pergunta sobre o PDF:")
        if st.button("Perguntar PDF"):
            if pergunta:
                st.info("Consultando IA... aguarde ⏳")
                resposta = qa_chain.run(pergunta)
                st.success("Resposta encontrada!")
                st.write("**Resposta da IA:**")
                st.write(resposta)
            else:
                st.warning("Digite uma pergunta primeiro.")
