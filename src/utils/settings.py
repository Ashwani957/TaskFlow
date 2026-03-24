from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    # Here SettingConfigDict tell from where we take the connection 
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    DB_CONNECTION:str
    SECRET_KEY:str
    ALGORITHM:str
    EXP_Time:int

settings=Settings()


# Here we just make this file to load the env file data so we can make the connection Here 