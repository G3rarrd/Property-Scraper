from dataclasses import dataclass

@dataclass
class PlaywrightConfig:
    headless : bool = True,
    timeout : int = 300000
    # browser_type : str = "chromium"