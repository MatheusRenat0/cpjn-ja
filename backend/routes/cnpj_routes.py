from flask import Blueprint, jsonify
from utils.validators import limpar_cnpj, is_cnpj_valido
from services.brasilapi import buscar_dados_cnpj

cnpj_bp = Blueprint('cnpj', __name__)

@cnpj_bp.route('/<cnpj_input>', methods=['GET'])
def consultar(cnpj_input):
    cnpj_limpo = limpar_cnpj(cnpj_input)
    
    if not is_cnpj_valido(cnpj_limpo):
        return jsonify({"erro": "CNPJ inválido. Deve conter 14 dígitos numéricos."}), 400
        
    dados, status_code = buscar_dados_cnpj(cnpj_limpo)
    
    return jsonify(dados), status_code