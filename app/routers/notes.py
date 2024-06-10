import logging
from typing import List

from crud.notes import (create_notes_query, delete_notes_query,
                        retrieve_notes_lists_query,
                        retrieve_specific_notes_query, update_notes_query)
from dependencies.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.notes import NotesInputSchema, NotesOutputSchema
from sqlalchemy.orm import Session

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
logger = logging.getLogger("default")
logger.setLevel(logging.DEBUG)

router = APIRouter(
    prefix="/api",
    tags=["Notes API Endpoints"],
)


@router.get("/notes", response_model=List[NotesOutputSchema])
async def notes_lists(db: Session = Depends(get_db)):
    """Retrieves all notes lists

    This endpoint fetches all available notes and returns them in a list format, each entry conforming to the
    NotesOutputSchema.

    :return: A list of notes, where each note is represented by the NotesOutputSchema. This schema includes the
             following fields:
             - id: Unique identifier for the note.
             - name: Name of the note.
             - description: Detailed description of the note.
             - tags (TagsSchema): A tags object representing the tags associated with the note.
    :rtype: List[NotesOutputSchema]
    """

    return retrieve_notes_lists_query(db=db)


@router.post("/notes", response_model=NotesOutputSchema)
async def create_notes(notes: NotesInputSchema, db: Session = Depends(get_db)):
    """Create a new note.

    This endpoint creates a new note based on the provided input data. The input must conform to the
    `NotesInputSchema`, and the created note will be returned in a format that matches the `NotesOutputSchema`.

    Args:
        notes (NotesInputSchema): The input data for the note to be created, which includes fields such as:
            - name (str): The name of the note.
            - description (str): A detailed description of the note.
        db (Session): A database session object.

    Returns:
        NotesOutputSchema: The created note, represented in the output schema format, which includes:
            - id (int): Unique identifier for the note.
            - name (str): Name of the note.
            - description (str): Detailed description of the note.
            - tags (TagsSchema): A tags object representing the tags associated with the note.
    """
    return create_notes_query(db=db, notes=notes)


@router.get(
    "/notes/{notes_id}",
    response_model=NotesOutputSchema,
)
async def notes_get(notes_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific note by its unique identifier.

    Args:
        notes_id (int): The unique identifier of the note to be retrieved.
        db (Session): A database session object.

    Returns:
        NotesOutputSchema: The created note, represented in the output schema format, which includes:
            - id (int): Unique identifier for the note.
            - name (str): Name of the note.
            - description (str): Detailed description of the note.
            - tags (TagsSchema): A tags object representing the tags associated with the note.
    Raises:
        HTTPException: If no note with the given ID is found, a 404 status code is returned with an error message.
    """
    note = retrieve_specific_notes_query(db=db, notes_id=notes_id)
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.put("/notes/{notes_id}", response_model=NotesOutputSchema)
async def update_notes(notes_id: int, notes: NotesInputSchema, db: Session = Depends(get_db)):
    """Update an existing note by ID.

    Args:
        - note_id (int): ID of the note to update.
        - note_data (NotesInputSchema): Data to update the note with.
        - db (Session): Database session.

    Returns:
        NotesOutputSchema: The updated note, represented in the output schema format, which includes:
            - id (int): Unique identifier for the note.
            - name (str): Name of the note.
            - description (str): Detailed description of the note.
            - tags (TagsSchema): A tags object representing the tags associated with the note.

    Raises:
        - HTTPException: If the note is not found.
    """
    update_note = update_notes_query(db=db, notes_id=notes_id, notes=notes)
    if update_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found."
        )
    return update_note


@router.delete("/notes/{notes_id}")
async def delete_notes(notes_id: int, db: Session = Depends(get_db)):
    """Delete a note by its ID.

    Args:
        - note_id (int): The ID of the note to be deleted.
        - db (Session): The database session dependency.

    Returns a success message upon successful deletion.

    Raises:
        - HTTPException: If the note is not found (404).
    """
    delete_note = delete_notes_query(db=db, notes_id=notes_id)
    if delete_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found."
        )
    return {"message": "Note deleted"}
