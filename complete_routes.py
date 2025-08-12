#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODAS AS ROTAS NECESSÁRIAS PARA O SISTEMA BERNARDO & STAHLHÖFER
Este arquivo contém todas as rotas que devem ser adicionadas ao main.py
"""

# ==================== ROTAS DE SERVIÇOS ====================
@app.get("/api/services")
async def get_services(db_session=Depends(get_db)):
    """Listar todos os serviços"""
    try:
        print("🔍 Buscando todos os serviços...")
        
        query = """
        SELECT id, name, description, price, category, created_at, updated_at
        FROM services
        ORDER BY name
        """
        result = db_session.execute(text(query))
        services = result.fetchall()
        
        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': float(service.price) if service.price else 0.0,
                'category': service.category,
                'created_at': service.created_at.isoformat() if service.created_at else None,
                'updated_at': service.updated_at.isoformat() if service.updated_at else None
            })
        
        print(f"✅ {len(services_list)} serviços encontrados")
        return {"data": services_list}
        
    except Exception as e:
        print(f"❌ Erro ao buscar serviços: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# ==================== ROTAS DE CLIENTE ====================
@app.get("/api/client/cases")
async def get_client_cases(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter casos do cliente logado"""
    try:
        user_id = current_user.get('user_id')
        print(f"🔍 Buscando casos do cliente ID: {user_id}")

        query = """
        SELECT cc.id, cc.service_id, cc.title, cc.description, cc.status, 
               cc.created_at, cc.updated_at,
               s.name as service_name
        FROM client_cases cc
        LEFT JOIN services s ON cc.service_id = s.id
        WHERE cc.user_id = %s
        ORDER BY cc.created_at DESC
        """
        result = db_session.execute(text(query), (user_id,))
        cases = result.fetchall()

        cases_list = []
        for case in cases:
            cases_list.append({
                'id': case.id,
                'service_id': case.service_id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'created_at': case.created_at.isoformat() if case.created_at else None,
                'updated_at': case.updated_at.isoformat() if case.updated_at else None,
                'service_name': case.service_name
            })

        print(f"✅ {len(cases_list)} casos encontrados para o cliente")
        return {"data": cases_list}

    except Exception as e:
        print(f"❌ Erro ao buscar casos do cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/client/stats")
async def get_client_stats(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter estatísticas do cliente logado"""
    try:
        user_id = current_user.get('user_id')
        print(f"🔍 Buscando estatísticas do cliente ID: {user_id}")

        # Contar casos por status
        query = """
        SELECT 
            COUNT(*) as total_cases,
            SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) as pending_cases,
            SUM(CASE WHEN status = 'em_andamento' THEN 1 ELSE 0 END) as active_cases,
            SUM(CASE WHEN status = 'concluido' THEN 1 ELSE 0 END) as completed_cases
        FROM client_cases 
        WHERE user_id = %s
        """
        result = db_session.execute(text(query), (user_id,))
        stats = result.fetchone()

        # Contar arquivos
        files_query = "SELECT COUNT(*) as total_files FROM process_files WHERE user_id = %s"
        files_result = db_session.execute(text(files_query), (user_id,))
        files_count = files_result.fetchone()

        stats_data = {
            'total_cases': stats.total_cases or 0,
            'pending_cases': stats.pending_cases or 0,
            'active_cases': stats.active_cases or 0,
            'completed_cases': stats.completed_cases or 0,
            'total_files': files_count.total_files if files_count else 0
        }

        print(f"✅ Estatísticas calculadas: {stats_data}")
        return {"data": stats_data}

    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas do cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# ==================== ROTAS ADMIN ADICIONAIS ====================
@app.get("/api/admin/clients/{client_id}/cases")
async def get_admin_client_cases(client_id: int, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter casos de um cliente específico (admin)"""
    try:
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        print(f"🔍 Buscando casos do cliente ID: {client_id}")

        query = """
        SELECT cc.id, cc.service_id, cc.title, cc.description, cc.status, 
               cc.created_at, cc.updated_at,
               s.name as service_name
        FROM client_cases cc
        LEFT JOIN services s ON cc.service_id = s.id
        WHERE cc.user_id = %s
        ORDER BY cc.created_at DESC
        """
        result = db_session.execute(text(query), (client_id,))
        cases = result.fetchall()

        cases_list = []
        for case in cases:
            cases_list.append({
                'id': case.id,
                'service_id': case.service_id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'created_at': case.created_at.isoformat() if case.created_at else None,
                'updated_at': case.updated_at.isoformat() if case.updated_at else None,
                'service_name': case.service_name
            })

        print(f"✅ {len(cases_list)} casos encontrados para o cliente {client_id}")
        return {"data": cases_list}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar casos do cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# ==================== ROTAS DE ANALYTICS ====================
@app.get("/api/analytics/stats")
async def get_analytics_stats(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter estatísticas gerais do sistema (admin)"""
    try:
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        print("🔍 Calculando estatísticas do sistema...")

        # Estatísticas gerais
        stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM users WHERE type = 'cliente') as total_clients,
            (SELECT COUNT(*) FROM client_cases) as total_cases,
            (SELECT COUNT(*) FROM client_cases WHERE status = 'pendente') as pending_cases,
            (SELECT COUNT(*) FROM client_cases WHERE status = 'em_andamento') as active_cases,
            (SELECT COUNT(*) FROM client_cases WHERE status = 'concluido') as completed_cases,
            (SELECT COUNT(*) FROM process_files) as total_files,
            (SELECT COUNT(*) FROM services) as total_services
        """
        result = db_session.execute(text(stats_query))
        stats = result.fetchone()

        analytics_data = {
            'total_clients': stats.total_clients or 0,
            'total_cases': stats.total_cases or 0,
            'pending_cases': stats.pending_cases or 0,
            'active_cases': stats.active_cases or 0,
            'completed_cases': stats.completed_cases or 0,
            'total_files': stats.total_files or 0,
            'total_services': stats.total_services or 0
        }

        print(f"✅ Estatísticas calculadas: {analytics_data}")
        return {"data": analytics_data}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao calcular estatísticas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
