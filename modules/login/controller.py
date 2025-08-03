from flask import Blueprint, make_response, jsonify

import jwt
import os
from datetime import datetime, timedelta
from flask import request

app_login = Blueprint('login_blueprint', __name__)

# Chave secreta (NUNCA expor isso em produção; use variáveis de ambiente)
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-super-secreta")

@app_login.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data["email"], data["password"])
    
    if not data:
        return jsonify(message="Dados de login não fornecidos!"), 400
    if "email" not in data or "password" not in data:
        return jsonify(message="Campos 'email' e 'password' são obrigatórios!"), 400
    if data["email"] == "admin" and data["password"] == "admin":
        
        print(data["email"], data["password"])
        
        # Gerar o token com expiração
        token = jwt.encode(
            {"user": data["email"], "exp": datetime.utcnow() + timedelta(minutes=30)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify(token=token)

    return jsonify(message="Credenciais inválidas!"), 401