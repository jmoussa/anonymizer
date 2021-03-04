import logging

from fastapi import Depends, APIRouter

from controllers import anonymize_data  # get_current_active_user

# from models import User
from mongodb import get_nosql_db, MongoClient
from requests import AnonymizeRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/anonymize", tags=["Anonymization"])
async def anonymize(
    _data: AnonymizeRequest,
    db: MongoClient = Depends(get_nosql_db),
    # current_user: User = Depends(get_current_active_user),
):
    """
    Recieves token and some data to Anonymize
    Returns anonymized dataset
    """

    row = anonymize_data(_data.username, _data.password, _data.data)
    return row
