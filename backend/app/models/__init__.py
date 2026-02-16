"""SQLAlchemy models – import all models here so Alembic can detect them."""

from app.models.user import User  # noqa: F401
from app.models.client import Client  # noqa: F401
from app.models.brief import Brief  # noqa: F401
from app.models.campaign import Campaign  # noqa: F401
from app.models.asset import Asset  # noqa: F401
from app.models.task import AgentTask, AgentMessage  # noqa: F401
from app.models.platform_credential import PlatformCredential  # noqa: F401
