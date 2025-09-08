import streamlit as st
import pandas as pd
import os

st.title("LINKAÊ - Sistema de Cadastro")

st.sidebar.title("Menu Lateral")
pagina = st.sidebar.radio("Escolha:", ["Cadastro", "Upload", "Gráficos"])

def salvar_dados(nome, email, senha):
    arquivo = 'cadastros.csv'
    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo)
    else:
        df = pd.DataFrame(columns=['Nome', 'Email', 'Senha'])

    if email in df["Email"].values:
        st.warning("Este e-mail já está cadastrado.")
        return False

    df.loc[len(df)] = [nome, email, senha]
    df.to_csv(arquivo, index=False)
    return True

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
            df = pd.read_csv("cadastros.csv")
            st.dataframe(df)
        else:
            st.info("Nenhum cadastro encontrado.")

elif pagina == "Upload":
    st.subheader("Upload de Arquivos")
    arquivo = st.file_uploader("Envie um arquivo CSV", type="csv")
    if arquivo is not None:
        df = pd.read_csv(arquivo)
        st.dataframe(df)

else:
    st.subheader("Gráficos de Usuários")

    if os.path.exists("cadastros.csv"):
        df = pd.read_csv("cadastros.csv")

        if not df.empty:
            df["Dominio"] = df["Email"].apply(lambda x: x.split("@")[-1])

            dominios = df["Dominio"].value_counts()

            st.bar_chart(dominios)

            st.write("Quantidade de usuários por domínio de e-mail:")
            st.dataframe(dominios)
        else:
            st.info("Ainda não há usuários cadastrados para gerar gráficos.")
    else:
        st.info("Nenhum cadastro encontrado para gerar gráficos.")