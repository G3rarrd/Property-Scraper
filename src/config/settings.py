from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    headless: bool = True
    start_page: int = 1100
    end_page : int = 2200
    worker_count: int = 5
    navigation_timeout: int = 300
    request_timeout: int = 300
    log_level: str = "INFO"


settings = Settings()