from sqlalchemy import Column, Boolean, DateTime, ForeignKey, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship

import uuid
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    max_leads = Column(Integer, default=10)
    current_leads = Column(Integer, default=0)

    competencies = relationship("OperatorCompetency", back_populates="operator")
    leads = relationship("Lead", back_populates="operator")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Связь с компетенциями и лидами
    competencies = relationship("OperatorCompetency", back_populates="source")
    leads = relationship("Lead", back_populates="source")


class OperatorCompetency(Base):
    __tablename__ = "operator_competencies"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    weight = Column(Float, default=1.0)

    # Связи
    operator = relationship("Operator", back_populates="competencies")
    source = relationship("Source", back_populates="competencies")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(Integer, ForeignKey("sources.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)
    contact_info = Column(String)

    # Связи
    source = relationship("Source", back_populates="leads")
    operator = relationship("Operator", back_populates="leads")