from config.logging_configure import setup_loggging
from config.configure import get_gemini_api
from error.errors import *
import requests
import json

logger = setup_loggging("AI_logger", "log/ai.log")

class AI_MODEL:
    def __init__(self):
        self.model = "gemini-2.5-flash"
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        self.api = get_gemini_api()
        

    def get_response(self, prompt):
        logger.info("LoopAI is init for generating resposne...")
        logger.info("System is getting ready header for http response...")
        header = {
            "x-goog-api-key": self.api,
            "Content-type": "application/json"
        }
        logger.info("System is not getting ready to add body for http response...")
        
        body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        logger.info("sending request over loopserver to google core...")
        try:
            loop_response = requests.post(
                self.url,
                headers=header,
                json=body
            )
            if loop_response.status_code == 200:
                data = loop_response.json()
                candidate = data["candidates"][0]
                content = candidate["content"]
                parts = content["parts"][0]
                reponse = parts["text"]
                print(reponse)
                logger.info("Model have extract the answer from candidate json and ready for next operation...")
            elif loop_response.status_code == 401:
                raise UnauthorizedcrentialError()
            elif loop_response.status_code == 429:
                raise TooManyRequestERROR()
            elif loop_response.status_code == 500:
                raise InternalServerError()
            else:
                logger.error(
                    f"Unexpexted code error occur at server {loop_response.status_code}"
                )
                raise UnexpectedStatusCodeError()
            return reponse
        except UnauthorizedcrentialError as err:
            logger.error(f"Unatutorized error: {err}")
            raise
        except TooManyRequestERROR as err:
            logger.error(f"Many request error : {err}")
            raise
        except InternalServerError as err:
            logger.error(f"Intenral server error: {err}")
            raise
        except requests.ConnectionError as err:
            raise InternetConnectionError from err
        except UnexpectedStatusCodeError as err:
            raise
