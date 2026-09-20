from error.errors import APImissingError , EmailAdressMissingError , AccountPasswordMissingError 
from config.logging_configure import setup_loggging
from dotenv import load_dotenv
import os
logger=setup_loggging("ENV_logger","log/env.log")
def get_gemini_api():
    logger.info("ENV is init for setup env file for gemini_api...")
    load_dotenv()
    api_key=os.getenv("GEMINI_API")
    logger.info("ENV successfully return gemini_api to program")
    if not api_key:
        raise APImissingError
    return api_key
def get_gmail_adress():
    load_dotenv()
    logger.info("ENV is init for setup env file for google account address...")
    email_add=os.getenv("EMAIL_ADDRESS")
    logger.info("ENV successfully return email address to program")
    if not email_add:
        raise EmailAdressMissingError()
    return email_add
def get_google_password():
    logger.info("ENV is init to setup env file for google account passowrd... ")
    load_dotenv()
    logger.info("ENV successfuly return google account password to server...")
    google_pas=os.getenv("EMAIL_PASSWORD")
    if not google_pas:
        raise AccountPasswordMissingError
    return google_pas
def get_smtp_server():
    load_dotenv()
    logger.info("ENV is init for setup env file for smtp server...")
    server=os.getenv("SMTP_SERVER")
    logger.info("Return server information too loopai server")
    return server

    