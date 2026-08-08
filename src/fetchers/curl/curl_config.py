from dataclasses import dataclass

@dataclass(frozen=True)
class CurlConfig:
    impoersonate: str
    accept_language : str
    timeout : float = 30.0