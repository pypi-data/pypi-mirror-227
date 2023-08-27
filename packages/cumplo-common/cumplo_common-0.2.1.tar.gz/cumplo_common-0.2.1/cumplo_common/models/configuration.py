# pylint: disable=no-member

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, PositiveInt


class Configuration(BaseModel):
    id: int = Field(...)
    name: str = Field("")
    filter_dicom: bool = Field(False)
    irr: Decimal | None = Field(None, ge=0)
    duration: PositiveInt | None = Field(None)
    score: Decimal | None = Field(None, ge=0, le=1)
    amount_requested: PositiveInt | None = Field(None)
    credits_requested: PositiveInt | None = Field(None)
    expiration_minutes: PositiveInt | None = Field(None)
    monthly_profit_rate: Decimal | None = Field(None, ge=0)
    average_days_delinquent: PositiveInt | None = Field(None)
    paid_in_time_percentage: Decimal | None = Field(None, ge=0, le=1)

    def __hash__(self) -> int:
        exclude = {"id", "name", "expiration_minutes"}
        return hash(self.model_dump_json(exclude=exclude, exclude_defaults=True, exclude_none=True))

    def __eq__(self, other: Any) -> bool:
        return self.__hash__() == other.__hash__()

    def serialize(self, for_firestore: bool = False) -> dict[str, Any]:
        """
        Serializes the configuration

        Args:
            for_firestore (bool, optional): Whether to serialize for Firestore or not. Defaults to False.

        Returns:
            dict[str, Any]: The serialized configuration as a dictionary
        """
        if for_firestore:
            content = self.model_dump(exclude_none=True, exclude={"id"})
            for key, value in content.items():
                if isinstance(value, Decimal):
                    content[key] = float(value)
            return content

        return self.model_dump(exclude_none=True)

    # TODO: Add filter by credit type
    # TODO: Add filter by minimum investment amount
    # TODO: Add filter by average investment amount
    # TODO: Add filter by average investments per user
