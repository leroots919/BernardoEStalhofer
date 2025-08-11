# list_routes.py - Listar todas as rotas disponíveis
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app

def list_all_routes():
    with app.app_context():
        print("🔍 Listando todas as rotas disponíveis...")
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'rule': rule.rule
            })
        
        # Ordenar por endpoint
        routes.sort(key=lambda x: x['rule'])
        
        print(f"\n✅ Encontradas {len(routes)} rotas:")
        for route in routes:
            methods = [m for m in route['methods'] if m not in ['HEAD', 'OPTIONS']]
            print(f"   {route['rule']} - {methods} - {route['endpoint']}")
        
        # Procurar especificamente por rotas de casos
        print("\n🔍 Rotas relacionadas a casos:")
        case_routes = [r for r in routes if 'case' in r['rule'].lower() or 'case' in r['endpoint'].lower()]
        for route in case_routes:
            methods = [m for m in route['methods'] if m not in ['HEAD', 'OPTIONS']]
            print(f"   ✅ {route['rule']} - {methods}")

if __name__ == "__main__":
    list_all_routes()
