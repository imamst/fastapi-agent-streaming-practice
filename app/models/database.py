from sqlmodel import Field, SQLModel


class ChatSession(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
