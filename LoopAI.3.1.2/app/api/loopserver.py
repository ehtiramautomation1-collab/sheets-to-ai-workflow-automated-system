from config.logging_configure import setup_loggging
from app.ai.ai_service import AI_MODEL
from app.email.email_service import EmailService
from app.gspreed.gspreed_service import Gspreed_Service
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import smtplib
from error.errors import *
import json

logger = setup_loggging("server_logger", "log/server.log")
ai = AI_MODEL()
email = EmailService()
sheet=Gspreed_Service()
class Order(BaseModel):
    Product: str
    Quantity: int
    Price: float
    Email: str
    Address: str
app = FastAPI()

@app.exception_handler(TooManyRequestERROR)
async def too_many_request(req: Request, exc: TooManyRequestERROR):
    logger.error(f"TooManyRequestERROR: {str(exc)}")
    return JSONResponse(
        status_code=429,
        content={
            "error": "too many request at a time please try latter",
            "message": str(exc)
        }
    )

@app.exception_handler(InternalServerError)
async def internal_server_hanlder(req: Request, exc: InternalServerError):
    logger.error(f"InternalServerError: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "internal server crashed",
            "error": str(exc)
        }
    )

@app.exception_handler(UnauthorizedcrentialError)
async def unauthorized_credin_handler(req: Request, exc: UnauthorizedcrentialError):
    logger.error(f"UnauthorizedcrentialError: {str(exc)}")
    return JSONResponse(
        status_code=401,
        content={
            "error": "unauthorized credintial please provide authorized credential",
            "message": str(exc)
        }
    )

@app.exception_handler(InvalideInputError)
async def invalide_input_hanlder(req: Request, exc: InvalideInputError):
    logger.error(f"InvalideInputError: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "invalide input enter by the system to server please try latter",
            "message": str(exc)
        }
    )

@app.exception_handler(smtplib.SMTPAuthenticationError)
async def smtp_auth_handler(req: Request, exc: smtplib.SMTPAuthenticationError):
    logger.error(f"SMTPAuthenticationError: {str(exc)}")
    return JSONResponse(
        status_code=401,
        content={
            "error": "error occur in smtpauthentication internal system error we will direct you shortly",
            "messge": str(exc)
        }
    )

@app.exception_handler(smtplib.SMTPException)
async def smtp_exception_hanlder(req: Request, exc: smtplib.SMTPException):
    logger.error(f"SMTPException: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal smtp error this is system error we will direct you shortly",
            "message": str(exc)
        }
    )

@app.exception_handler(InternetConnectionError)
async def inernet_hanlder(req: Request, exc: InternetConnectionError):
    logger.error(f"InternetConnectionError: {str(exc)}")
    return JSONResponse(
        status_code=408,
        content={
            "error": "it seem like you are offline please try latter",
            "message": str(exc)
        }
    )

@app.exception_handler(UnexpectedStatusCodeError)
async def unexpexted_code_handler(req: Request, exc: UnexpectedStatusCodeError):
    logger.error(f"UnexpectedStatusCodeError: {str(exc)}")
    return JSONResponse(
        status_code=502,
        content={
            "error": "unexpected status code return by the system this is system error we will redirect you shortly",
            "message": str(exc)
        }
    )

@app.get("/")
def home():
    return {"role": "shopify endpoint", "Message": "Thank for shopping with shopire"}

@app.post("/Order")
def place_order(data: Order):
    logger.info(f"Processing order for {data.Email}")
    print(data.Product)
    print(data.Email)
    print(data.Address)
    
    formatted_price = f"${data.Price:.2f}"
    
    system_prompt = (
        "Imagine you are a person shopify automated email generator your business name is Shopinity you will write email in a form where you will say thanks to customer that you placer order with us and say your product is send to this address like top automated system do in their autoamtion system you will create email in a human form also you will redesing the customer email subject like a top automated system "
        f"A customer submitted this request: Product: {data.Product} Quantity: {data.Quantity} Price: {formatted_price} Email address: {data.Email} Address: {data.Address} "
        "Analyze the customer's request and write a helpful response."
    )
    logger.info("Creating db reqeust for user...")
    db_request=sheet.create_requst(
        data.Product,
        data.Quantity,
        data.Price,
        data.Email,
        data.Address
    )
    try:
        ai_response = ai.get_response(system_prompt).strip()
        recipt=data.Email
        subj=f"Order confirmation {data.Product}"
        body=ai_response
        logger.info("Server si now sending the mail")
        email.send_mail(
            recipt,
            subj,
            body
        )
        logger.info("Emails is send seccuessfuly")
        sheet.update_request(
            db_request,
            "Completed"
        )
        logger.info("status updated ok 200")
    except Exception as err:
        sheet.update_request(
            db_request,
            "FAILED",
        )
        raise
    

