import logging
from typing import Union

from models.notes import Notes
from models.tags import Tags

from sqlalchemy.orm import Session

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
logger = logging.getLogger("default")
logger.setLevel(logging.DEBUG)


def retrieve_tags_list_query(db: Session) -> Tags:
    """Retrieve a list of all tags from the database.

    Args:
        - db (Session): SQLAlchemy session object.

    Returns:
        list[Tags]: A list of all tag objects from the database.

    Raises:
        Exception: If an error occurs during the database query.
    """
    try:
        db_tags = db.query(Tags)
        return db_tags.all()
    except Exception as e:
        db.rollback()
        logger.error(f"{str(e)}")
        raise e


def retrieved_tags_and_its_notes_query(db: Session, tags_name: str) -> Union[dict, None]:
    """
    Retrieve a tag and its corresponding notes where it is used.

    Args:
        - db (Session): SQLAlchemy session object.
        - tags_name (str): The name of the tag to search for.

    Returns:
        dict: A dictionary containing the tag information and a list of corresponding notes.
    """
    try:
        # Query for the tag by its name
        tag = db.query(Tags).filter(Tags.name == tags_name).first()

        if tag:
            # Get the notes associated with the tag
            notes = db.query(Notes).filter(Notes.tags.any(id=tag.id)).all()

            # Construct a dictionary containing the tag information and its corresponding notes
            tag_and_notes = {
                "tag_name": tag.name,
                "notes": [{"title": note.title, "description": note.description} for note in notes]
            }

            return tag_and_notes
        else:
            return {"message": "Tags not found"}
    except Exception as e:
        # Handle any errors that occur during the database operation
        db.rollback()
        logger.error(f"Error retrieving tag and its corresponding notes: {str(e)}")
        raise e
