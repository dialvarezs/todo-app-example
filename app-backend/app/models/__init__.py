from advanced_alchemy.base import CommonTableAttributes
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, CommonTableAttributes):
    pass
