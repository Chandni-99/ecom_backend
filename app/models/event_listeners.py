from sqlalchemy import event
from sqlalchemy.sql import func
from app.models.models import BaseClass


@event.listens_for(BaseClass,'before_update',propagate=True)
def receive_before_update(mapper,connection,target):
    target.updated_at = func.now()