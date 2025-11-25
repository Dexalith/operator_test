from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.database import get_db
from app import models, schemas
from services.lead_distrub import LeadDistributionService

router = APIRouter()


@router.post("/operators/", response_model=schemas.Operator)
async def create_operator(
        operator: schemas.OperatorCreate,
        db: AsyncSession = Depends(get_db)
):
    db_operator = models.Operator(**operator.dict())
    db.add(db_operator)
    await db.commit()
    await db.refresh(db_operator)
    return db_operator


@router.post("/sources/", response_model=schemas.Source)
async def create_source(
        source: schemas.SourceCreate,
        db: AsyncSession = Depends(get_db)
):
    db_source = models.Source(**source.dict())
    db.add(db_source)
    await db.commit()
    await db.refresh(db_source)
    return db_source


@router.post("/competencies/", response_model=schemas.Competency)
async def create_competency(
        competency: schemas.CompetencyCreate,
        db: AsyncSession = Depends(get_db)
):
    db_competency = models.OperatorCompetency(**competency.dict())
    db.add(db_competency)
    await db.commit()
    await db.refresh(db_competency)
    return db_competency


@router.post("/leads/", response_model=schemas.Lead)
async def create_lead(
        lead: schemas.LeadCreate,
        db: AsyncSession = Depends(get_db)
):
    # Создаем лид
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    await db.commit()
    await db.refresh(db_lead)

    # Распределяем оператора через сервис
    distribution_service = LeadDistributionService(db)
    operator = await distribution_service.assign_operator_to_lead(db_lead)

    if operator:
        db_lead.operator_id = operator.id
        db_lead.status = "assigned"
        await db.commit()
        await db.refresh(db_lead)

    return db_lead


@router.get("/operators/{operator_id}", response_model=schemas.Operator)
async def get_operator(
        operator_id: int,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Operator).where(models.Operator.id == operator_id)
    )
    operator = result.scalar_one_or_none()

    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator


@router.put("/leads/{lead_id}/close")
async def close_lead(
        lead_id: str,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Lead).where(models.Lead.id == lead_id)
    )
    lead = result.scalar_one_or_none()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead.operator_id:
        result = await db.execute(
            select(models.Operator).where(models.Operator.id == lead.operator_id)
        )
        operator = result.scalar_one_or_none()

        if operator and operator.current_leads > 0:
            operator.current_leads -= 1

    lead.status = "closed"
    await db.commit()

    return {"message": "Lead closed successfully"}


@router.get("/")
async def read_root():
    return {"message": "Lead Distribution CRM API"}