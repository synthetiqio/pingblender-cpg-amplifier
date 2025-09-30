from core.config import Network as Config
from typing import List

class EnvironmentController:

    class get:

        def __init__(
                self
        ):
            pass

        def urls(self):
            li = Config.CL
            cors : list = self._default()
            if li != "":
                for i in li:
                    cors.append(i)
                return cors
            else:
                return cors
            
        def _default(self)->List[str]:
            listing = Config.Default['URLS'].value
            return listing