from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from app.models import Lead, Operator, OperatorCompetency
import random


class LeadDistributionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assign_operator_to_lead(self, lead: Lead) -> Optional[Operator]:
        """
        Асинхронно распределяет лида между операторами
        """
        source_id = lead.source_id
        stmt = (
            select(OperatorCompetency)
            .join(Operator)
            .where(
                and_(
                    Operator.is_active == True,
                    OperatorCompetency.source_id == source_id,
                    Operator.current_leads < Operator.max_leads
                )
            )
        )

        result = await self.db.execute(stmt)
        competencies = result.scalars().all()

        if not competencies:
            return None

        # Создаем взвешенный список операторов
        weighted_operators = []
        for comp in competencies:
            operator = comp.operator
            available_capacity = operator.max_leads - operator.current_leads
            weight = comp.weight * available_capacity

            repeat_count = max(1, int(weight * 10))
            weighted_operators.extend([operator] * repeat_count)

        if not weighted_operators:
            return None

        # Выбираем случайного оператора с учетом весов
        selected_operator = random.choice(weighted_operators)

        # Обновляем счетчик лидов оператора
        selected_operator.current_leads += 1

        # Сохраняем изменения
        await self.db.commit()
        await self.db.refresh(selected_operator)

        return selected_operator

    async def get_available_operators_for_source(self, source_id: int) -> List[Operator]:
        """Асинхронно получает доступных операторов для источника"""
        stmt = (
            select(Operator)
            .join(OperatorCompetency)
            .where(
                and_(
                    Operator.is_active == True,
                    Operator.current_leads < Operator.max_leads,
                    OperatorCompetency.source_id == source_id
                )
            )
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()