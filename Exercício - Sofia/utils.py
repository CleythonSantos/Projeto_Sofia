def ler_float(msg):

    while True:
        try:
            valor = float(input(msg))
            return valor
        except ValueError:
            print("Erro: Digite um número válido!")