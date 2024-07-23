from pydantic_settings import BaseSettings


class DataConfig(BaseSettings):
    natural_questions_training_path: str


class RagConfig(BaseSettings):
    prompt_template_path: str
