from enum import Enum, auto


class BrowserType(Enum):
    CHROME = auto()
    CHROME_HEADLESS = auto()

    @classmethod
    def get_browser(cls, name: str) -> 'BrowserType':
        try:
            return cls[name.upper()]
        except KeyError:
            raise KeyError(f"[{name.upper()}] browser isn't supported "
                           f"- choose one of {list(map(lambda l: str(l).split('.')[1], cls))}")
