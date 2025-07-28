### Contexto: O desafio dos dados inconsistentes

Profissionais de marketing que trabalham com campanhas de **SMS** e **WhatsApp** Business enfrentam um desafio recorrente: a **inconsistência nos formatos de números de telefone**.

Ao importar uma base de contatos de diferentes fontes (landing pages, CRM, cadastros manuais, etc.), é comum encontrar números em formatos variados como:

- 27981275377
- (21) 98599-45299
- 5519991772715

Esse cenário impede que ferramentas de automação reconheçam corretamente os números — o que compromete a entrega das mensagens e os resultados das campanhas.

Para resolver esse problema, o código abaixo padroniza todos os números para o **formato internacional E.164**, exigido por plataformas como **Twilio**, **Bird**, **Zenvia**, **360Dialog** (WhatsApp API), entre outras.

### O que é o formato E.164?

O **formato E.164** é o padrão internacional para formatação de números de telefone. Ele garante que o número:

- Comece com um sinal de `+`
- Seja seguido do **DDI (código do país)**, como `55` para o Brasil
- Inclua o **DDD** e o número local

Exemplo:
Número local: `21 98599-4529` → Formato E.164: `+5521985994529`

### Código explicado passo a passo

```python
import pandas as pd
import re
```

Importa as bibliotecas necessárias:

- `pandas`: para criar e exportar a planilha
- `re`: para manipular e limpar os números usando expressões regulares

#### 1. Entrada dos dados

```python
numeros_raw = """
27981275377
(21) 98599-45299
5519991772715
"""
```

Simula uma base de dados com números em formatos diferentes.

:::warning
⚠️ Em um uso real, esses dados poderiam vir de um CSV, planilha, banco de dados, formulário etc.
:::

#### 2. Preparação da lista

```python
numeros = [linha.strip() for linha in numeros_raw.strip().splitlines() if linha.strip()]
```

Essa linha faz a limpeza dos dados:

- Remove espaços em branco antes/depois de cada número
- Descarta linhas vazias

### 3. Função de formatação

```python
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
```

Essa função:

- Remove tudo que não é número, como parênteses, traços, espaços, etc.
- Remove o DDI “55”, caso o número já tenha
- Valida se tem pelo menos 10 dígitos (DDD + número)
- Retorna o número formatado no padrão `+55xxxxxxxxxx`
- Caso contrário, sinaliza que o número é inválido

#### 4. Aplicação da função

```python
numeros_formatados = [formatar_e164(n) for n in numeros]
```

Aplica a formatação em todos os números da lista.

#### 5. Exportar para Excel

```python
df = pd.DataFrame({'Telefone': numeros_formatados})
df.to_excel('numeros_formatados.xlsx', index=False)
```

Cria uma planilha chamada `numeros_formatados.xlsx` com os números já prontos para uso em ferramentas de disparo.

### Resultado final (exemplo da planilha)

| Telefone  |
| ------------ |
| +5527981275377  |
| +55219859945299  |
| +5519991772715 |

### Conclusão

Esse pequeno script em Python ajuda times de marketing a economizar tempo e evitar erros ao padronizar seus contatos para campanhas de **WhatsApp** e **SMS**.

Ele garante que os números estejam no formato exigido pelas plataformas de disparo, evitando bloqueios, rejeições e melhorando a taxa de entrega das mensagens.

Você pode adaptar esse código para:

- Ler direto de um `.csv` ou `.xlsx`
- Validar números por DDD
- Enviar relatórios com números inválidos
- Rodar como parte de uma automação (ex: via Airflow ou cron job)

No meu caso, eu copiei a coluna de números de telefones de uma planilha enviada a mim com vários números em formatos diferentes, apliquei na função e depois colei de volta na planilha já com os números no formato E.164 na mesma ordem.

Essa é uma das pequenas situações onde [profissionais de marketing que sabem programar](/aprender-python/ "Porque aprender a programar?") se destacam.
