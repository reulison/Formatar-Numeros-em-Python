import pandas as pd
import re

# Lista de números (exemplo com alguns, substitua pela lista completa no seu código)
numeros_raw = """
27981275377
(21) 98599-45299
5519991772715
"""  # Adicione sua lista completa aqui

# Separar os números em uma lista e limpar espaços
numeros = [linha.strip() for linha in numeros_raw.strip().splitlines() if linha.strip()]

def formatar_e164(numero):
    # Remove tudo que não for dígito
    numero_limpo = re.sub(r'\D', '', numero)

    # Remove DDI se já tiver
    if numero_limpo.startswith("55"):
        numero_limpo = numero_limpo[2:]

    # Garantir que o número tenha pelo menos DDD + número
    if len(numero_limpo) >= 10:
        return f'+55{numero_limpo}'
    else:
        return f'Número inválido: {numero}'

# Aplicar a formatação
numeros_formatados = [formatar_e164(n) for n in numeros]

# Criar planilha Excel
df = pd.DataFrame({'Telefone': numeros_formatados})
df.to_excel('numeros_formatados.xlsx', index=False)
