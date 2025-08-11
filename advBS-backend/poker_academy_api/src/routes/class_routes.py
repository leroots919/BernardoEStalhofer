# src/routes/class_routes.py
import sys
import os

# Adiciona o diretório pai de 'src' (ou seja, 'poker_academy_api') ao sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app, send_from_directory
from src.models import db, Classes, UserProgress, ClassViews, Users, UserType
from src.auth import token_required, admin_required
from datetime import datetime
from sqlalchemy import desc
import os
from werkzeug.utils import secure_filename

class_bp = Blueprint("class_bp", __name__)

# Configurações de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads', 'videos')
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'}

# Criar pasta de upload se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Pasta de upload: {UPLOAD_FOLDER}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota de teste sem autenticação
@class_bp.route("/api/test", methods=["GET"])
def test_route():
    try:
        print("🧪 Rota de teste chamada!")

        # Testar conexão com banco
        all_classes = Classes.query.all()
        print(f"📊 Total de aulas: {len(all_classes)}")

        return jsonify({
            "status": "OK",
            "message": "Backend funcionando",
            "total_classes": len(all_classes)
        }), 200
    except Exception as e:
        print(f"❌ Erro na rota de teste: {e}")
        return jsonify(error=str(e)), 500

# Rota para listar todas as aulas
@class_bp.route("/api/classes", methods=["GET"])
@token_required
def get_all_classes(current_user):
    try:
        print("🔍 Buscando aulas...")

        # Buscar todas as aulas (agora todas têm vídeo)
        all_classes = Classes.query.all()
        print(f"📊 Total de aulas: {len(all_classes)}")

        result = [c.to_dict() for c in all_classes]
        print(f"✅ Retornando {len(result)} aulas")

        return jsonify(result), 200
    except Exception as e:
        print(f"❌ Erro ao buscar aulas: {e}")
        current_app.logger.error(f"Erro ao buscar classes: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar dados das aulas."), 500

# Rota para buscar detalhes de uma aula específica
@class_bp.route("/api/classes/<int:class_id>", methods=["GET"])
def get_class_details(class_id):
    try:
        single_class = Classes.query.get(class_id)
        if not single_class:
            return jsonify(error="Aula não encontrada"), 404
        return jsonify(single_class.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar detalhes da aula {class_id}: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar dados da aula."), 500

# Rota para criar uma nova aula (apenas admin)
@class_bp.route("/api/classes", methods=["POST"])
@admin_required
def create_class(current_user):
    data = request.get_json()
    print(f"🔍 Dados recebidos para criar aula: {data}")

    if not data:
        return jsonify(error="Dados não fornecidos"), 400

    # Campos obrigatórios básicos
    required_fields = ["name", "instructor", "date", "category", "video_type"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify(error=f"Campo obrigatório ausente ou vazio: {field}"), 400

    # Validação específica para vídeo (apenas para novas aulas)
    if not data.get("video_path"):
        return jsonify(error="É obrigatório fazer upload de um vídeo"), 400

    try:
        new_class = Classes(
            name=data["name"],
            instructor=data["instructor"],
            date=data["date"], # Certifique-se que o formato da data é compatível (ex: YYYY-MM-DD)
            category=data["category"],
            video_type=data["video_type"],
            video_path=data.get("video_path"),
            priority=data.get("priority", 5),
            views=data.get("views", 0)
        )
        db.session.add(new_class)
        db.session.commit()
        return jsonify(new_class.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar classe: {e}", exc_info=True)
        return jsonify(error=f"Erro ao criar nova aula: {str(e)}"), 500


@class_bp.route("/api/classes/<int:class_id>", methods=["PUT"])
def update_class(class_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(error="Dados não fornecidos"), 400

        cls_to_update = Classes.query.get(class_id)
        if not cls_to_update:
            return jsonify(error="Aula não encontrada"), 404

        # Campos que podem ser atualizados
        if "name" in data:
            cls_to_update.name = data["name"]
        if "instructor" in data:
            cls_to_update.instructor = data["instructor"]
        if "date" in data:
            cls_to_update.date = data["date"]
        if "category" in data:
            cls_to_update.category = data["category"]
        if "video_type" in data:
            cls_to_update.video_type = data["video_type"]
        if "video_path" in data: # Adicionado para consistência
            cls_to_update.video_path = data["video_path"]
        if "priority" in data:
            cls_to_update.priority = data["priority"]
        
        db.session.commit()
        return jsonify(cls_to_update.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar aula {class_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao atualizar aula: {str(e)}"), 500

# Rota para excluir uma aula
@class_bp.route("/api/classes/<int:class_id>", methods=["DELETE"])
def delete_class(class_id):
    cls_to_delete = Classes.query.get(class_id)
    if not cls_to_delete:
        return jsonify(error="Aula não encontrada"), 404
    
    try:
        db.session.delete(cls_to_delete)
        db.session.commit()
        return jsonify(message="Aula excluída com sucesso"), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir aula {class_id}: {e}", exc_info=True)
        return jsonify(error=f"Erro ao excluir aula: {str(e)}"), 500

# Rota para marcar progresso de uma aula
@class_bp.route("/api/classes/<int:class_id>/progress", methods=["POST"])
@token_required
def update_class_progress(current_user, class_id):
    try:
        data = request.get_json()
        progress = data.get('progress', 0)
        watched = data.get('watched', False)
        video_time = data.get('current_time', 0.0)

        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404

        # Buscar ou criar progresso do usuário
        user_progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            class_id=class_id
        ).first()

        if user_progress:
            user_progress.progress = progress
            user_progress.watched = watched
            user_progress.video_time = video_time
            user_progress.last_watched = datetime.utcnow()
        else:
            user_progress = UserProgress(
                user_id=current_user.id,
                class_id=class_id,
                progress=progress,
                watched=watched,
                video_time=video_time,
                last_watched=datetime.utcnow()
            )
            db.session.add(user_progress)

        # Incrementar views se assistiu pela primeira vez
        if watched and (not user_progress or not user_progress.watched):
            class_obj.views += 1
            print(f"Views incrementadas para aula {class_id}: {class_obj.views}")

        db.session.commit()
        return jsonify(message="Progresso atualizado com sucesso"), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar progresso: {e}", exc_info=True)
        return jsonify(error="Erro ao atualizar progresso"), 500

# Rota para obter progresso do usuário
@class_bp.route("/api/classes/<int:class_id>/progress", methods=["GET"])
@token_required
def get_class_progress(current_user, class_id):
    try:
        user_progress = UserProgress.query.filter_by(
            user_id=current_user.id,
            class_id=class_id
        ).first()

        if user_progress:
            return jsonify({
                "progress": user_progress.progress,
                "watched": user_progress.watched,
                "current_time": user_progress.video_time,
                "last_watched": user_progress.last_watched.isoformat() if user_progress.last_watched else None
            }), 200
        else:
            return jsonify({
                "progress": 0,
                "watched": False,
                "current_time": 0.0,
                "last_watched": None
            }), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar progresso: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar progresso"), 500

# Rota para obter histórico de aulas assistidas pelo usuário
@class_bp.route("/api/classes/history", methods=["GET"])
@token_required
def get_user_history(current_user):
    try:
        # Buscar aulas que o usuário já assistiu (com progresso > 0)
        history = db.session.query(UserProgress, Classes).join(
            Classes, UserProgress.class_id == Classes.id
        ).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.progress > 0
        ).order_by(desc(UserProgress.last_watched)).all()

        result = []
        for user_progress, class_obj in history:
            class_data = class_obj.to_dict()
            class_data.update({
                'progress': user_progress.progress,
                'watched': user_progress.watched,
                'current_time': user_progress.video_time,
                'last_watched': user_progress.last_watched.isoformat() if user_progress.last_watched else None
            })
            result.append(class_data)

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar histórico: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar histórico"), 500

# Rota para registrar visualização de aula
@class_bp.route("/api/classes/<int:class_id>/view", methods=["POST"])
@token_required
def register_view(current_user, class_id):
    try:
        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404

        # Obter informações da requisição
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
        user_agent = request.headers.get('User-Agent')

        # Registrar a visualização
        new_view = ClassViews(
            user_id=current_user.id,
            class_id=class_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(new_view)

        # Incrementar contador de views na aula
        class_obj.views += 1

        db.session.commit()

        return jsonify({
            'message': 'Visualização registrada com sucesso',
            'total_views': class_obj.views
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao registrar visualização: {e}", exc_info=True)
        return jsonify(error="Erro ao registrar visualização"), 500

# Rota para obter estatísticas de visualizações (apenas admin)
@class_bp.route("/api/classes/<int:class_id>/views", methods=["GET"])
@admin_required
def get_class_views(current_user, class_id):
    try:
        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404

        # Buscar todas as visualizações da aula
        views = ClassViews.query.filter_by(class_id=class_id).order_by(desc(ClassViews.viewed_at)).all()

        # Estatísticas
        total_views = len(views)
        unique_users = len(set(view.user_id for view in views))

        result = {
            'class_id': class_id,
            'class_name': class_obj.name,
            'total_views': total_views,
            'unique_users': unique_users,
            'views': [view.to_dict() for view in views]
        }

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar visualizações: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar visualizações"), 500

# Rota de teste para upload
@class_bp.route("/api/classes/upload-test", methods=["GET"])
def upload_test():
    return jsonify(message="Rota de upload funcionando!", upload_folder=UPLOAD_FOLDER)

# Rota para listar instrutores (admins) disponíveis
@class_bp.route("/api/instructors", methods=["GET"])
@admin_required
def get_instructors(current_user):
    try:
        # Buscar todos os usuários admin
        instructors = Users.query.filter_by(type=UserType.admin).all()

        result = []
        for instructor in instructors:
            result.append({
                'id': instructor.id,
                'name': instructor.name,
                'email': instructor.email
            })

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar instrutores: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar instrutores"), 500

# Rota para obter estatísticas do painel de analytics (apenas admin)
@class_bp.route("/api/analytics/stats", methods=["GET"])
@admin_required
def get_analytics_stats(current_user):
    try:
        # Total de alunos (usuários do tipo student)
        total_students = Users.query.filter_by(type=UserType.student).count()

        # Total de aulas
        total_classes = Classes.query.count()

        # Aula mais visualizada
        most_popular_class = Classes.query.order_by(desc(Classes.views)).first()
        most_popular_class_name = most_popular_class.name if most_popular_class else "Nenhuma aula"
        most_popular_class_views = most_popular_class.views if most_popular_class else 0

        # Total de visualizações
        total_views = db.session.query(db.func.sum(Classes.views)).scalar() or 0

        # Aulas com vídeo
        classes_with_video = Classes.query.filter(Classes.video_path.isnot(None)).count()

        # Estudantes que já assistiram pelo menos uma aula
        active_students = db.session.query(UserProgress.user_id).distinct().count()

        return jsonify({
            'total_students': total_students,
            'total_classes': total_classes,
            'most_popular_class': most_popular_class_name,
            'most_popular_class_views': most_popular_class_views,
            'total_views': total_views,
            'classes_with_video': classes_with_video,
            'active_students': active_students
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar estatísticas: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar estatísticas"), 500

# Rota para upload de vídeo (apenas admin)
@class_bp.route("/api/classes/upload-video", methods=["POST"])
@admin_required
def upload_video(current_user):
    print("Rota de upload chamada!")
    try:
        if 'video' not in request.files:
            return jsonify(error="Nenhum arquivo enviado"), 400

        file = request.files['video']
        if file.filename == '':
            return jsonify(error="Nenhum arquivo selecionado"), 400

        if file and allowed_file(file.filename):
            # Gerar nome seguro para o arquivo
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
            filename = timestamp + filename

            # Salvar arquivo
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            return jsonify({
                'message': 'Vídeo enviado com sucesso',
                'filename': filename,
                'path': filepath
            }), 200
        else:
            return jsonify(error="Tipo de arquivo não permitido"), 400

    except Exception as e:
        current_app.logger.error(f"Erro no upload: {e}", exc_info=True)
        return jsonify(error="Erro ao fazer upload do vídeo"), 500

# Rota para servir vídeos (com autenticação via query parameter)
@class_bp.route("/api/videos/<filename>")
def serve_video(filename):
    try:
        # Verificar autenticação via query parameter ou header
        token = request.args.get('token') or request.headers.get('Authorization')

        if not token:
            return jsonify(error="Token de acesso necessário"), 401

        # Se o token vem do header, remover 'Bearer '
        if token.startswith('Bearer '):
            token = token[7:]

        # Verificar se o token é válido (simplificado)
        import jwt
        try:
            jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify(error="Token inválido"), 401

        # Verificar se o arquivo existe
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify(error="Vídeo não encontrado"), 404

        response = send_from_directory(UPLOAD_FOLDER, filename)
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
    except Exception as e:
        current_app.logger.error(f"Erro ao servir vídeo: {e}", exc_info=True)
        return jsonify(error="Erro ao carregar vídeo"), 500

# Rota para servir vídeos com autenticação simplificada
@class_bp.route("/api/videos-public/<filename>")
@token_required
def serve_video_public(current_user, filename):
    try:
        print(f"Usuário {current_user.name} acessando vídeo: {filename}")

        # Verificar se o arquivo existe
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify(error="Vídeo não encontrado"), 404

        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        print(f"Erro ao servir vídeo: {e}")
        current_app.logger.error(f"Erro ao servir vídeo: {e}", exc_info=True)
        return jsonify(error="Erro ao carregar vídeo"), 500

