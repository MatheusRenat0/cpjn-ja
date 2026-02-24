import requests

def buscar_dados_cnpj(cnpj):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json(), 200
        elif response.status_code == 404:
            return {"erro": "CNPJ não encontrado na base de dados."}, 404
        else:
            return {"erro": "Erro ao consultar o serviço externo."}, 500
            
    except requests.exceptions.RequestException:
        return {"erro": "Serviço indisponível no momento."}, 503