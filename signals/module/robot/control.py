from module.robot.config import ROBOT as Config

class Scope:

    def __init__(
            self,
        ):
        pass


class SynthController:

    def __init__(
            self,
    ):
        pass 

    def api_key(self):
        return Config.Config.OpenAI.Account
    
    def open_api(self):
        return Config.Config.OpenAI().Client()

    def get_settings(self):
        return Config.Config.OpenAI().Settings()
    

class RobotController:

    def __init__(
            self,
        ):
        pass

    def certPath(self)->str:
        return Config.Sys.CERT_PATH
    
    def timestamp(self):
        return Config.Region.getTimestampLocal()
    
    def getPayloadParams(self):
        return Config.Options.PAYLOAD_PARAMS


    def getToken(
            self, 
            un,
            pw,
            sub
            ):
        from module.robot.action.meter import Charon 
        return Charon.get_token(locals)


class MeterController:
    def __init__(
            self,
        ):
        pass

    def certPath(self)->str:
        return Config.Sys.CERT_PATH

class LLM:


    class Control:


        class ModelController:

            pass