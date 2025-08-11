#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import requests
import json

def test_admin_endpoints():
    """Testar endpoints do admin diretamente"""
    print("🔍 Testando endpoints do admin...")
    
    base_url = "http://localhost:8000"
    
    # 1. Fazer login como admin
    print("\n1️⃣ Fazendo login como admin...")
    login_data = {
        "email": "admin@advtransito.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get('access_token')
            print(f"✅ Login realizado! Token: {token[:50]}...")
            
            # 2. Testar endpoint de clientes
            print("\n2️⃣ Testando /api/admin/clients...")
            headers = {"Authorization": f"Bearer {token}"}
            
            clients_response = requests.get(f"{base_url}/api/admin/clients", headers=headers)
            print(f"Status: {clients_response.status_code}")
            
            if clients_response.status_code == 200:
                clients_data = clients_response.json()
                print(f"✅ Clientes recebidos: {len(clients_data)}")
                print("📋 Dados dos clientes:")
                for client in clients_data:
                    print(f"   - ID: {client.get('id')} | Nome: {client.get('name')} | Email: {client.get('email')}")
            else:
                print(f"❌ Erro ao buscar clientes: {clients_response.text}")
            
            # 3. Testar endpoint de casos
            print("\n3️⃣ Testando /api/admin/cases...")
            cases_response = requests.get(f"{base_url}/api/admin/cases", headers=headers)
            print(f"Status: {cases_response.status_code}")
            
            if cases_response.status_code == 200:
                cases_data = cases_response.json()
                print(f"✅ Casos recebidos: {len(cases_data)}")
                print("📋 Dados dos casos:")
                for case in cases_data:
                    print(f"   - ID: {case.get('id')} | Título: {case.get('title')} | Status: {case.get('status')}")
            else:
                print(f"❌ Erro ao buscar casos: {cases_response.text}")
                
        else:
            print(f"❌ Erro no login: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_admin_endpoints()
