from pydantic import BaseModel, ConfigDict, Field, EmailStr

class UserBase(BaseModel):
  email: EmailStr = Field(min_length=1, max_length=120)
  nome: str | None = Field(default= None, min_length=1, max_length=100)
  cognome: str | None = Field(default= None, min_length=1, max_length=100)

class UserCreate(UserBase):
  password: str = Field(min_length=8)

class UserPatch(UserBase):
  email: EmailStr | None = Field(default = None, min_length=1, max_length=120)

class UserResponsePrivate(UserBase):
  id: int

  model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
  acces_token: str
  type: str