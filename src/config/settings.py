from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    headless: bool = True
    start_page: int = 1
    end_page : int = 2100
    worker_count: int = 3
    navigation_timeout: int = 300
    request_timeout: int = 300
    network_retry_count: int = 3
    log_level: str = "INFO"


settings = Settings()