import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
from groq import Groq
from pypdf import PdfReader

# CONFIGURAÇÕES INICIAIS
st.set_page_config(page_title="EducaIA - Plataforma Concurseiro", layout="wide", page_icon="📚")

# BANCO DE DADOS
def init_db():
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            data_cadastro TEXT NOT NULL
        )
    """)
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN role TEXT DEFAULT 'aluno'")
    except sqlite3.OperationalError:
        pass

    # Usuário admin padrão
    cursor.execute("SELECT * FROM usuarios WHERE email='admin@test.com'")
    if not cursor.fetchall():
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO usuarios (nome,email,senha,role,data_cadastro) VALUES (?, ?, ?, ?, ?)",
                       ("Admin Test", "admin@test.com", "admin123", "admin", data))
    conn.commit()
    conn.close()

def add_usuario(nome, email, senha, role="aluno"):
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("INSERT INTO usuarios (nome,email,senha,role,data_cadastro) VALUES (?, ?, ?, ?, ?)",
                       (nome, email, senha, role, data))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_usuario_por_email(email):
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=?", (email,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def get_usuarios():
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Inicializar DB
init_db()

# SESSÃO
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.role = ""
    st.session_state.email = ""
    st.session_state.page = "Login"

# PAGINA LOGIN
def pagina_login():
    st.markdown("<h1 style='text-align:center; color:#2C3E50;'>📚 EducaIA - Login</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        usuario = get_usuario_por_email(email)
        if usuario and usuario[3] == senha:
            st.session_state.logged_in = True
            st.session_state.user_name = usuario[1]
            st.session_state.role = usuario[4]
            st.session_state.email = usuario[2]
            st.session_state.page = "Dashboard"
            st.success(f"Bem-vindo(a), {usuario[1]}!")
            st.stop()
        else:
            st.error("Email ou senha incorretos.")
    st.markdown("---")
    if st.button("Não tem conta? Cadastre-se"):
        st.session_state.page = "Cadastro"
        st.stop()

# PAGINA CADASTRO
def pagina_cadastro():
    st.markdown("<h1 style='text-align:center; color:#2C3E50;'>📝 Cadastro</h1>", unsafe_allow_html=True)
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    role = st.selectbox("Tipo de usuário", ["aluno", "admin"])
    if st.button("Cadastrar"):
        if nome and email and senha:
            sucesso = add_usuario(nome, email, senha, role)
            if sucesso:
                st.success(f"Usuário {nome} cadastrado com sucesso como {role}!")
                st.session_state.page = "Login"
                st.stop()
            else:
                st.error("Email já cadastrado. Tente outro.")
        else:
            st.warning("Preencha todos os campos.")
    st.markdown("---")
    if st.button("Voltar para Login"):
        st.session_state.page = "Login"
        st.stop()

# ÁREA LOGADA
def area_logada():
    st.sidebar.markdown("<h2 style='text-align:center; color:#2C3E50;'>🔹 Menu</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Sair"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.role = ""
        st.session_state.email = ""
        st.session_state.page = "Login"
        st.success("Você saiu da conta com sucesso!")
        st.stop()

    # Menu por função
    if st.session_state.role == "admin":
        opcoes_menu = ["🏠 Dashboard", "📝 Cadastro", "📂 Upload", "🖋️ Geração de Texto", "📄 Leitura de PDF"]
    else:
        opcoes_menu = ["🏠 Dashboard", "📂 Upload", "🖋️ Geração de Texto", "📄 Leitura de PDF"]

    menu = st.sidebar.radio("Navegação", opcoes_menu, index=0)
    st.markdown(f"<h1 style='text-align:center; color:#2C3E50;'>🔹 Bem-vindo(a), {st.session_state.user_name}</h1>", unsafe_allow_html=True)

    # Aqui entram todos os menus: Dashboard, Cadastro, Upload, Geração de Texto, Leitura de PDF

# EXECUÇÃO PRINCIPAL
  if st.session_state.page == "Login":
    if st.session_state.logged_in:
        st.session_state.page = "Dashboard"
        area_logada()
    else:
        pagina_login()
elif st.session_state.page == "Cadastro":
    pagina_cadastro()
else:
    area_logada()
