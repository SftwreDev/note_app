import logging
from typing import List

from crud.tags import retrieve_tags_list_query
from dependencies.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.tags import TagsOutputSchema

from sqlalchemy.orm import Session

from crud.tags import retrieved_tags_and_its_notes_query

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
logger = logging.getLogger("default")
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/api",
    tags=["Tags API Endpoints"],
)


@router.get("/tags", response_model=List[TagsOutputSchema])
async def tags_list(db: Session = Depends(get_db)):
    """Endpoint to retrieve a list of all tags.

    Args:
        - db (Session): Database session.

    Returns:
        List[TagsOutputSchema]: A list of tag objects serialized into the `TagsOutputSchema`.

    Raises:
        HTTPException: If an error occurs during the retrieval.
    """
    return retrieve_tags_list_query(db=db)


@router.get("/tags/{tags_name}")
async def retrieve_tags_and_its_notes(tags_name: str, db: Session = Depends(get_db)) -> dict:
    """
    Retrieve a tag and its corresponding notes.

    This endpoint fetches a tag by its name and retrieves all notes associated with it.

    Args:
        - tags_name (str): The name of the tag to search for.
        - db (Session): Database session.

    Returns:
        dict: A dictionary containing the tag name and a list of corresponding notes.

    Raises:
        HTTPException: If the tag is not found or an unexpected error occurs.
    """
    return retrieved_tags_and_its_notes_query(db=db, tags_name=tags_name)
