
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
  database_hostname: str
  database_port: int
  database_password: str
  database_name: str
  database_username: str
  
  jwt_secret_key: SecretStr
  algorithm: str
  access_token_expire_minutes: int

  password_reset_token_expiration_minutes: int
  mail_server: str
  mail_port: int
  mail_username: str
  mail_password: SecretStr
  mail_from: str
  mail_use_tls: bool

  password_reset_frontend_url: str

  model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


settings = Settings()