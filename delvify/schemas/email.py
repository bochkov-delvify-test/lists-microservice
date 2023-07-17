from pydantic import BaseModel, EmailStr

# Ideally, notification service provides a client library to send email
# Copy-Pasting the code here for simplicity


class Email(BaseModel):
    destination: EmailStr
    subject: str
    body: str
