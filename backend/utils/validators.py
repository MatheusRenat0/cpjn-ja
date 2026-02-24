import re

def limpar_cnpj(cnpj):
    
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    return cnpj_limpo

def is_cnpj_valido(cnpj_limpo):

    return len(cnpj_limpo) == 14