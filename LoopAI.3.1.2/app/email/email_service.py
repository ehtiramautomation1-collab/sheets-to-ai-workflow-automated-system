from config.configure import *
from config.logging_configure import setup_loggging
from error.errors import *
import smtplib
from email.message import EmailMessage
logger=setup_loggging("email_logger","log/email.log")
class EmailService:
    def __init__(self):
        self.account=get_gmail_adress()
        self.password=get_google_password()
        self.server=get_smtp_server()
    def smtp_connection(self):
        logger.info("Server is getting ready for building smtp connection...")
        try:
            connection=smtplib.SMTP(
                self.server,
                587
            )
            connection.starttls()
            connection.login(
                self.account,
                self.password
            )
            return connection
        except smtplib.SMTPAuthenticationError as err:
            logger.error(f"Authentication failed error:{err}")
            raise
        except smtplib.SMTPConnectError as err:
            logger.error(f"SMTP connection error:{err}")
            raise
        except smtplib.SMTPException as err:
            logger.error(f"SMTP error:{err}")
            raise
    def validate_input(self,recipent,subject,body):
        logger.info("Server is now checking and validate email before sending mail...")
        if not recipent:
               raise InvalideInputError("recipient is required")
        if not subject:
            raise InvalideInputError(" subject is required")
        if not body:
            raise InvalideInputError("Body of mail is required")
    def send_mail(self,recipt,sub,body):
        connection=None
        self.validate_input(recipt,sub,body)
        logger.info("Server is now sending mail to customer with secure tls connection...")
        try:
            message=EmailMessage()
            message["From"]=self.account
            message["To"]=recipt
            message["Subject"]=sub
            message.set_content(body)
            connection=self.smtp_connection()
            connection.send_message(message)
            logger.info("Server has send mail successfully")
        except smtplib.SMTPException as err:
            logger.error(f"SMTP ERROR:{err}")
            raise
        finally:
            if connection is not None:
                connection.quit()
                logger.info("SMTP connection is closed...")

        
