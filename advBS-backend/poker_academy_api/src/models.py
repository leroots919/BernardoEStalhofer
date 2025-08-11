# src/models.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAlchemyEnum, Numeric
import enum
from datetime import datetime # Para default=datetime.utcnow ou similar se db.func.current_timestamp() não for o desejado

db = SQLAlchemy()

class UserType(enum.Enum):
    admin = "admin"
    cliente = "cliente"

class ServiceCategory(enum.Enum):
    multas = "multas"
    cnh = "cnh"
    acidentes = "acidentes"
    consultoria = "consultoria"
    recursos = "recursos"

class CaseStatus(enum.Enum):
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluido = "concluido"
    arquivado = "arquivado"

class VideoType(enum.Enum):
    youtube = "youtube"  # Temporário para compatibilidade
    local = "local"

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False) # Nome completo
    username = db.Column(db.String(100), nullable=True, unique=True) # Nome de usuário único (opcional)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False) # Senha hasheada
    type = db.Column(SQLAlchemyEnum(UserType), nullable=False, default=UserType.cliente) # Tipo de usuário
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # Data de registro
    last_login = db.Column(db.DateTime, nullable=True)

    # Campos adicionais para clientes
    cpf = db.Column(db.String(14), nullable=True) # CPF do cliente
    phone = db.Column(db.String(20), nullable=True) # Telefone
    address = db.Column(db.Text, nullable=True) # Endereço completo
    city = db.Column(db.String(100), nullable=True) # Cidade
    state = db.Column(db.String(2), nullable=True) # Estado (UF)
    zip_code = db.Column(db.String(10), nullable=True) # CEP

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'type': self.type.value if self.type else None,
            'register_date': self.register_date.isoformat() if self.register_date else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'cpf': self.cpf,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code
            # Não inclua password_hash no to_dict por segurança
        }

class Services(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(SQLAlchemyEnum(ServiceCategory), nullable=False)
    price = db.Column(Numeric(10, 2), nullable=True)
    duration_days = db.Column(db.Integer, nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value if self.category else None,
            "price": float(self.price) if self.price else None,
            "duration_days": self.duration_days,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class ClientCases(db.Model):
    __tablename__ = "client_cases"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(SQLAlchemyEnum(CaseStatus), nullable=False, default=CaseStatus.pendente)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Favorites(db.Model):
    __tablename__ = "favorites"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete="CASCADE"), primary_key=True)

class Consultations(db.Model):
    __tablename__ = "consultations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(SQLAlchemyEnum(CaseStatus), nullable=False, default=CaseStatus.pendente)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ProcessFiles(db.Model):
    __tablename__ = "process_files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey("client_cases.id", ondelete="CASCADE"), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    uploaded_by_admin = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'case_id': self.case_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'description': self.description,
            'uploaded_by_admin': self.uploaded_by_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

