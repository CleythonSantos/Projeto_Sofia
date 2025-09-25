import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
from groq import Groq
from pypdf import PdfReader

# -----------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------
st.set_page_config(page_title="EducaIA - Plataforma Concurseiro", layout="wide", page_icon="📚")

# -----------------------------
# BANCO DE DADOS
# -----------------------------
def init_db():
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            data_cadastro TEXT NOT NULL,
            role TEXT DEFAULT 'aluno'
        )
    """)
    conn.commit()
    conn.close()

def add_usuario(nome, email, senha):
    conn = sqlite3.connect("educaia.db")
    cursor = conn.cursor()
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("INSERT INTO usuarios (nome,email,senha,data_cadastro,role) VALUES (?, ?, ?, ?, 'aluno')",
                       (nome, email, senha, data))
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

# Inicializar DB
init_db()

# -----------------------------
# SESSÃO
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.email = ""
    st.session_state.page = "Login"

# -----------------------------
# PAGINA LOGIN
# -----------------------------
def pagina_login():
    st.markdown("<h1 style='text-align:center; color:#2C3E50;'>📚 EducaIA - Login</h1>", unsafe_allow_html=True)
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        usuario = get_usuario_por_email(email)
        if usuario and usuario[3] == senha:
            st.session_state.logged_in = True
            st.session_state.user_name = usuario[1]
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

# -----------------------------
# PAGINA CADASTRO
# -----------------------------
def pagina_cadastro():
    st.markdown("<h1 style='text-align:center; color:#2C3E50;'>📝 Cadastro</h1>", unsafe_allow_html=True)
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Cadastrar"):
        if nome and email and senha:
            sucesso = add_usuario(nome, email, senha)
            if sucesso:
                st.success(f"Usuário {nome} cadastrado com sucesso como aluno!")
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

# -----------------------------
# ÁREA LOGADA
# -----------------------------
def area_logada():
    st.sidebar.markdown("<h2 style='text-align:center; color:#2C3E50;'>🔹 Menu</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Sair"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.email = ""
        st.session_state.page = "Login"
        st.success("Você saiu da conta com sucesso!")
        st.stop()

    # Menu fixo para aluno
    opcoes_menu = ["🏠 Dashboard", "📂 Upload", "🖋️ Geração de Texto", "📄 Leitura de PDF"]
    menu = st.sidebar.radio("Navegação", opcoes_menu, index=0)
    st.markdown(f"<h1 style='text-align:center; color:#2C3E50;'>🔹 Bem-vindo(a), {st.session_state.user_name}</h1>", unsafe_allow_html=True)

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    if menu == "🏠 Dashboard":
        st.markdown("## 📊 Dashboard de Estudos - Progresso Visual")
        materias = ["Matemática", "Português", "História", "Geografia", "Informática"]
        total_conteudos = [10, 8, 7, 5, 6]
        concluido = [6, 5, 7, 2, 4]
        porcentagem = [int(c/t*100) if t !=0 else 0 for c,t in zip(concluido, total_conteudos)]
        a_estudar = [t-c for t,c in zip(total_conteudos, concluido)]
        st.markdown("### 📝 Progresso por Matéria")
        cols = st.columns(len(materias))
        for i, col in enumerate(cols):
            col.metric(label=materias[i], value=f"{porcentagem[i]}%", delta=f"{concluido[i]}/{total_conteudos[i]} concluídos")
        df_prog = pd.DataFrame({"Matéria": materias, "Concluído": concluido, "A Estudar": a_estudar})
        fig_prog = px.bar(df_prog, x="Matéria", y=["Concluído", "A Estudar"], text_auto=True,
                          labels={"value": "Conteúdos", "variable": "Status"},
                          color_discrete_sequence=["#2ca02c", "#ff7f0e"], title="📊 Progresso por Matéria")
        st.plotly_chart(fig_prog, use_container_width=True)

    # -----------------------------
    # UPLOAD
    # -----------------------------
    elif menu == "📂 Upload":
        st.markdown("## Upload de Arquivos (CSV)")
        uploaded_file = st.file_uploader("Envie um arquivo CSV com questões ou materiais", type=["csv"])
        if uploaded_file is not None:
            df_upload = pd.read_csv(uploaded_file)
            st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")
            st.dataframe(df_upload)

    # -----------------------------
    # GERAÇÃO DE TEXTO
    # -----------------------------
    elif menu == "🖋️ Geração de Texto":
        st.markdown("## 🖋️ Geração de Texto com IA")
        chave = st.text_input("Digite sua chave da Groq", type="password")
        modelo = st.selectbox("Escolha o modelo", ["llama-3.3-70b-versatile","llama-3.1-8b-instant","mixtral-8x7b-32768"])
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
                    st.write(f"Título: {titulo if titulo else 'Sem título'}")
                    st.markdown("---")
                    st.write(texto_final)
                    st.download_button("Baixar Texto", texto_final, "texto_gerado.txt")
                except Exception as e:
                    st.error(f"Erro ao gerar texto: {e}")
            else:
                st.warning("Preencha todos os campos antes de gerar o texto.")

    # -----------------------------
    # LEITURA DE PDF
    # -----------------------------
    elif menu == "📄 Leitura de PDF":
        st.markdown("## 📄 Leitura de PDF com IA")
        chave = st.text_input("Digite sua chave da Groq", type="password")
        modelo = st.selectbox("Escolha o modelo", ["llama-3.3-70b-versatile","llama-3.1-8b-instant","mixtral-8x7b-32768"])
        uploaded_file = st.file_uploader("Envie um PDF", type=["pdf"])
        if uploaded_file is not None:
            st.success(f"Arquivo {uploaded_file.name} carregado com sucesso!")
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

# -----------------------------
# EXECUÇÃO PRINCIPAL
# -----------------------------
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
