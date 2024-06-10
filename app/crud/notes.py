import logging

from models.notes import Notes
from models.tags import Tags
from schemas.notes import NotesInputSchema
from sqlalchemy.orm import Session

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
logger = logging.getLogger("default")
logger.setLevel(logging.DEBUG)


def create_notes_query(db: Session, notes: NotesInputSchema) -> Notes:
    """Create a new note with optional tags in the database.

    This function performs the following operations:
    1. Extracts the names of tags from the input.
    2. Retrieves existing tags from the database matching these names.
    3. Creates new tags for names that do not already exist.
    4. Associates the note with both the existing and new tags.
    5. Commits the new note to the database.

    Args:
        - db (Session): SQLAlchemy session object.
        - notes (NotesInputSchema): The input schema containing note details.

    Returns:
        Notes: The newly created note object including its associated tags.

    Raises:
        Exception: For any other unexpected errors.
    """
    try:
        db_tags_query = db.query(Tags)
        db_tags_lists = []

        if notes.tags:
            tag_names = {tag.name for tag in notes.tags}

            # Retrieve existing tags
            existing_tags = db_tags_query.filter(Tags.name.in_(tag_names)).all()
            existing_tag_names = {tag.name for tag in existing_tags}

            db_tags_lists.extend(existing_tags)

            # Create new tags for names not already existing
            new_tag_names = tag_names - existing_tag_names
            new_tags = [Tags(name=name) for name in new_tag_names]
            db.add_all(new_tags)
            db.commit()

            db_tags_lists.extend(new_tags)

        db_note = Notes(
            title=notes.title,
            description=notes.description,
            tags=db_tags_lists
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)

        return db_note
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error when creating notes: {str(e)}")
        raise e


def retrieve_notes_lists_query(db: Session) -> Notes:
    """Retrieve all notes with their associated tags from the database.

    Args:
        db (Session): SQLAlchemy session object.

    Returns:
        List[Notes]: A list of all note objects retrieved from the database.

    Raises:
        Exception: For any other unexpected errors.
    """
    try:
        db_notes = db.query(Notes)
        return db_notes.all()
    except Exception as e:
        db.rollback()
        logger.error(f"{str(e)}")
        raise e


def retrieve_specific_notes_query(db: Session, notes_id: int) -> Notes:
    """Retrieve a specific note by its ID from the database.

    Args:
        - db (Session): SQLAlchemy session object.
        - notes_id (int): The ID of the note to be retrieved.

    Returns:
        Notes: The note object if found, otherwise None.

    Raises:
        Exception: If an error occurs during the database operation.
    """
    try:
        db_notes = db.query(Notes)
        return db_notes.filter(Notes.id == notes_id).first()
    except Exception as e:
        db.rollback()
        logger.error(f"{str(e)}")
        raise e


def update_notes_query(db: Session, notes_id: int, notes: NotesInputSchema) -> Notes:
    """Update a note's title and description by its ID in the database.

     Args:
         - db (Session): Database session.
         - notes_id (int): The ID of the note to be updated.
         - notes (NotesInputSchema): The updated data for the note, including title and description.

     Returns:
         Notes: The updated note object if found and updated, otherwise None.

     Raises:
         Exception: If an error occurs during the database operation.
     """
    try:
        db_note = db.query(Notes).filter(Notes.id == notes_id).first()

        if db_note:
            db_note.title = notes.title
            db_note.description = notes.description
            db.add(db_note)
            db.commit()
            db.refresh(db_note)
        return db_note
    except Exception as e:
        db.rollback()
        logger.error(f"{str(e)}")
        raise e


def delete_notes_query(db: Session, notes_id: int) -> Notes:
    """Delete a note from the database by its ID.

    Args:
        - db (Session): Database session.
        - notes_id (int): The ID of the note to be deleted.

    Returns:
        Notes: The deleted note object if found and deleted, otherwise None.

    Raises:
        Exception: If an error occurs during the database operation.
    """
    try:
        db_note = db.query(Notes).filter(Notes.id == notes_id).first()

        if db_note:
            db.delete(db_note)
            db.commit()
        return db_note
    except Exception as e:
        db.rollback()
        logger.error(f"{str(e)}")
        raise e
