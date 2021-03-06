from fastapi import Depends, APIRouter, HTTPException, status

from anonymizer.controllers import anonymize_data, deanonymize_data

from models import User, UserSen
from anonymizer.mongodb import get_nosql_db, MongoClient
from anonymizer.requests import AnonymizeRequest, UserTokenRequest
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/anonymize", tags=["Anonymization"])
async def anonymize(
    data: AnonymizeRequest,
    db: MongoClient = Depends(get_nosql_db),
    # current_user: User = Depends(get_current_active_user),
):
    """
    Recieves token and some data to Anonymize
    Returns anonymized dataset
    """

    row = await anonymize_data(data.username, data.password, data.data)
    if row:
        return User(**row)
    else:
        HTTPException(400, detail="No rows anonymized")


@router.post("/deanonymize", tags=["Anonymization"])
async def deanonymize(data: UserTokenRequest, db: MongoClient = Depends(get_nosql_db)):
    """
    Recieves login details and returns deanonymized data
    """
    row = await deanonymize_data(data.username, data.password)
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return UserSen(**row)
