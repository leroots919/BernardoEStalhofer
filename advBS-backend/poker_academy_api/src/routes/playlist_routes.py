# src/routes/playlist_routes.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app
from src.models import db, Playlists, PlaylistClasses, Classes
from src.auth import token_required

playlist_bp = Blueprint("playlist_bp", __name__)

# Rota para listar playlists do usuário
@playlist_bp.route("/api/playlists", methods=["GET"])
@token_required
def get_user_playlists(current_user):
    try:
        playlists = Playlists.query.filter_by(user_id=current_user.id).all()
        
        result = []
        for playlist in playlists:
            # Contar número de aulas na playlist
            class_count = PlaylistClasses.query.filter_by(playlist_id=playlist.id).count()
            
            result.append({
                "id": playlist.id,
                "name": playlist.name,
                "description": playlist.description,
                "class_count": class_count
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar playlists: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar playlists"), 500

# Rota para criar nova playlist
@playlist_bp.route("/api/playlists", methods=["POST"])
@token_required
def create_playlist(current_user):
    try:
        data = request.get_json()
        if not data:
            return jsonify(error="Dados não fornecidos"), 400
        
        name = data.get('name')
        if not name:
            return jsonify(error="Nome da playlist é obrigatório"), 400
        
        new_playlist = Playlists(
            user_id=current_user.id,
            name=name,
            description=data.get('description', '')
        )
        
        db.session.add(new_playlist)
        db.session.commit()
        
        return jsonify({
            "id": new_playlist.id,
            "name": new_playlist.name,
            "description": new_playlist.description,
            "class_count": 0
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar playlist: {e}", exc_info=True)
        return jsonify(error="Erro ao criar playlist"), 500

# Rota para obter detalhes de uma playlist
@playlist_bp.route("/api/playlists/<int:playlist_id>", methods=["GET"])
@token_required
def get_playlist_details(current_user, playlist_id):
    try:
        playlist = Playlists.query.filter_by(
            id=playlist_id,
            user_id=current_user.id
        ).first()
        
        if not playlist:
            return jsonify(error="Playlist não encontrada"), 404
        
        # Buscar aulas da playlist
        playlist_classes = db.session.query(PlaylistClasses, Classes).join(
            Classes, PlaylistClasses.class_id == Classes.id
        ).filter(PlaylistClasses.playlist_id == playlist_id).all()
        
        classes_list = []
        for playlist_class, class_obj in playlist_classes:
            classes_list.append(class_obj.to_dict())
        
        return jsonify({
            "id": playlist.id,
            "name": playlist.name,
            "description": playlist.description,
            "classes": classes_list
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar playlist: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar playlist"), 500

# Rota para adicionar aula à playlist
@playlist_bp.route("/api/playlists/<int:playlist_id>/classes/<int:class_id>", methods=["POST"])
@token_required
def add_class_to_playlist(current_user, playlist_id, class_id):
    try:
        # Verificar se a playlist pertence ao usuário
        playlist = Playlists.query.filter_by(
            id=playlist_id,
            user_id=current_user.id
        ).first()
        
        if not playlist:
            return jsonify(error="Playlist não encontrada"), 404
        
        # Verificar se a aula existe
        class_obj = Classes.query.get(class_id)
        if not class_obj:
            return jsonify(error="Aula não encontrada"), 404
        
        # Verificar se a aula já está na playlist
        existing = PlaylistClasses.query.filter_by(
            playlist_id=playlist_id,
            class_id=class_id
        ).first()
        
        if existing:
            return jsonify(error="Aula já está na playlist"), 409
        
        # Adicionar aula à playlist
        new_playlist_class = PlaylistClasses(
            playlist_id=playlist_id,
            class_id=class_id
        )
        
        db.session.add(new_playlist_class)
        db.session.commit()
        
        return jsonify(message="Aula adicionada à playlist"), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao adicionar aula à playlist: {e}", exc_info=True)
        return jsonify(error="Erro ao adicionar aula à playlist"), 500

# Rota para remover aula da playlist
@playlist_bp.route("/api/playlists/<int:playlist_id>/classes/<int:class_id>", methods=["DELETE"])
@token_required
def remove_class_from_playlist(current_user, playlist_id, class_id):
    try:
        # Verificar se a playlist pertence ao usuário
        playlist = Playlists.query.filter_by(
            id=playlist_id,
            user_id=current_user.id
        ).first()
        
        if not playlist:
            return jsonify(error="Playlist não encontrada"), 404
        
        # Buscar a relação playlist-aula
        playlist_class = PlaylistClasses.query.filter_by(
            playlist_id=playlist_id,
            class_id=class_id
        ).first()
        
        if not playlist_class:
            return jsonify(error="Aula não está na playlist"), 404
        
        db.session.delete(playlist_class)
        db.session.commit()
        
        return jsonify(message="Aula removida da playlist"), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao remover aula da playlist: {e}", exc_info=True)
        return jsonify(error="Erro ao remover aula da playlist"), 500

# Rota para deletar playlist
@playlist_bp.route("/api/playlists/<int:playlist_id>", methods=["DELETE"])
@token_required
def delete_playlist(current_user, playlist_id):
    try:
        playlist = Playlists.query.filter_by(
            id=playlist_id,
            user_id=current_user.id
        ).first()
        
        if not playlist:
            return jsonify(error="Playlist não encontrada"), 404
        
        db.session.delete(playlist)
        db.session.commit()
        
        return jsonify(message="Playlist deletada com sucesso"), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao deletar playlist: {e}", exc_info=True)
        return jsonify(error="Erro ao deletar playlist"), 500
