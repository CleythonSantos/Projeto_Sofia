import os

class Aluno:
    def __init__(self, matricula, nome, nota1, nota2):
        self.matricula = matricula
        self.nome = nome
        self.nota1 = nota1
        self.nota2 = nota2

    def media(self):
        return (self.nota1 + self.nota2) / 2

    def situacao(self):
        m = self.media()
        if m >= 7:
            return "Aprovado"
        elif m >= 5:
            return "Recuperação"
        else:
            return "Reprovado"

    def to_string(self):
        return f"{self.matricula};{self.nome};{self.nota1};{self.nota2}"

    @staticmethod
    def from_string(data):
        matricula, nome, nota1, nota2 = data.strip().split(";")
        return Aluno(matricula, nome, float(nota1), float(nota2))

alunos = []
ARQUIVO = "alunos.txt"

def carregar_alunos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            for linha in f:
                alunos.append(Aluno.from_string(linha))

def salvar_alunos():
    with open(ARQUIVO, "w") as f:
        for aluno in alunos:
            f.write(aluno.to_string() + "\n")

def validar_matricula(matricula):
    return matricula.isdigit() and not any(a.matricula == matricula for a in alunos)

def validar_nome(nome):
    return bool(nome.strip())

def validar_nota(valor):
    try:
        nota = float(valor)
        return 0 <= nota <= 10, nota
    except:
        return False, None

def cadastrar():
    matricula = input("Digite a matrícula: ").strip()
    if not validar_matricula(matricula):
        print("Entrada inválida ou matrícula já cadastrada.")
        return
    nome = input("Digite o nome: ").strip()
    if not validar_nome(nome):
        print("Nome inválido.")
        return
    valido1, nota1 = validar_nota(input("Digite a 1° nota: "))
    valido2, nota2 = validar_nota(input("Digite a 2° nota: "))
    if not (valido1 and valido2):
        print("Notas inválidas.")
        return
    alunos.append(Aluno(matricula, nome, nota1, nota2))
    salvar_alunos()
    print(f"Aluno '{nome}' cadastrado com sucesso!")

def alterar():
    matricula = input("Digite a matrícula do aluno para alterar: ").strip()
    for aluno in alunos:
        if aluno.matricula == matricula:
            nome = input(f"Novo nome ({aluno.nome}): ") or aluno.nome
            if not validar_nome(nome):
                print("Nome inválido.")
                return
            n1_input = input(f"Nova nota 1 ({aluno.nota1}): ") or str(aluno.nota1)
            n2_input = input(f"Nova nota 2 ({aluno.nota2}): ") or str(aluno.nota2)
            valido1, nota1 = validar_nota(n1_input)
            valido2, nota2 = validar_nota(n2_input)
            if not (valido1 and valido2):
                print("Notas inválidas.")
                return
            aluno.nome = nome
            aluno.nota1 = nota1
            aluno.nota2 = nota2
            salvar_alunos()
            print(f"Aluno '{aluno.nome}' alterado com sucesso!")
            return
    print("Aluno não encontrado.")

def excluir():
    matricula = input("Digite a matrícula do aluno para excluir: ").strip()
    for aluno in alunos:
        if aluno.matricula == matricula:
            alunos.remove(aluno)
            salvar_alunos()
            print(f"Aluno '{aluno.nome}' excluído com sucesso!")
            return
    print("Aluno não encontrado.")

def listar():
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return
    print("\nLista de Alunos:")
    print(f"{'Matrícula':<10} {'Nome':<20} {'Nota1':<5} {'Nota2':<5} {'Média':<6} {'Situação'}")
    print("-" * 60)
    for aluno in alunos:
        print(f"{aluno.matricula:<10} {aluno.nome:<20} {aluno.nota1:<5} {aluno.nota2:<5} {aluno.media():<6.2f} {aluno.situacao()}")
    print()

def menu():
    carregar_alunos()
    while True:
        print("===== Boletim ETEPDSimples =====")
        print("1 - Cadastrar")
        print("2 - Alterar")
        print("3 - Excluir")
        print("4 - Listar")
        print("5 - Sair")
        try:
            opcao = int(input("Escolha uma opção: "))
            print()
            if opcao == 1:
                cadastrar()
            elif opcao == 2:
                alterar()
            elif opcao == 3:
                excluir()
            elif opcao == 4:
                listar()
            elif opcao == 5:
                print("Sistema finalizado com sucesso!")
                break
            else:
                print("Opção inválida! Digite um número entre 1 e 5.")
        except:
            print("Digite um número válido para a opção.")

menu()