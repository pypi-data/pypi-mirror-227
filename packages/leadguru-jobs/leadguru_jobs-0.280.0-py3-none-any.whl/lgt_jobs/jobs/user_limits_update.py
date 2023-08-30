from abc import ABC
from datetime import datetime
from typing import List, Optional
from lgt_data.engine import UserCreditStatementDocument
from lgt_data.enums import UserAccountState
from lgt_data.model import UserModel
from lgt_data.mongo_repository import UserMongoRepository, DedicatedBotRepository, to_object_id
from pydantic import BaseModel
from lgt.common.python.lgt_logging import log
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
User limits handling
"""


class UpdateUserDataUsageJobData(BaseBackgroundJobData, BaseModel):
    channel_id: str
    bot_name: str
    filtered: bool
    user_ids: List[str]
    message: Optional[str]


class UpdateUserDataUsageJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return UpdateUserDataUsageJobData

    @staticmethod
    def increment(user_id: str, dedicated_bot_id: str = None, bot_name: str = None, message: str = None):
        log.info(f"[UpdateUserDataUsageJob] Updating user: {user_id}")
        UserCreditStatementDocument(
            user_id=to_object_id(user_id),
            created_at=datetime.utcnow(),
            balance=-1,
            action="lead-filtered",
            attributes=[bot_name if bot_name else "", dedicated_bot_id if dedicated_bot_id else "",
                        message if message else ""]
        ).save()

    @staticmethod
    def get_users(user_ids: List[str]) -> List[UserModel]:
        return UserMongoRepository().get_users(users_ids=user_ids)

    def exec(self, data: UpdateUserDataUsageJobData):
        users = self.get_users(data.user_ids)
        for user in users:
            if user.state == UserAccountState.Suspended.value:
                continue

            if user and data.bot_name in user.excluded_workspaces:
                continue

            if user and user.excluded_channels and user.excluded_channels.get(data.bot_name) and \
                    (data.channel_id in user.excluded_channels.get(data.bot_name)):
                continue

            dedicated_bot = DedicatedBotRepository().get_by_user_and_name(user.id, data.bot_name)
            if dedicated_bot and not dedicated_bot.invalid_creds:
                self.increment(f"{user.id}", bot_name=data.bot_name,
                               dedicated_bot_id=str(dedicated_bot.id), message=data.message)
