import json
import os
import datetime
from sqlalchemy import func
import uvicorn
from fastapi import Depends,FastAPI,HTTPException
from database import Session,user_model,Book,BookDetails,BorrowedBooks
from model import  UpdateResponse, UserCreate,BookCreate,BookDetailsUpdate

def get_db():
    db=Session()
    try:
        yield db
    finally:
        db.close()

app=FastAPI()



# User APIs

@app.post("/users/",response_model=UserCreate)
def user_create(user:UserCreate,db:Session=Depends(get_db)):
    new_data=user_model(Name=user.Name,Email=user.Email,MembershipDate=user.MembershipDate)
    db.add(new_data)
    db.commit()
    return new_data

@app.get("/user/list/",response_model=list[UserCreate])
def list_users(db:Session=Depends(get_db)):
    return db.query(user_model).all()

@app.get("/user/{user_id}",response_model=UserCreate)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(user_model).filter(user_model.UserID==user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="user not found")
    return user

#Book APIs
@app.post("/books/",response_model=BookCreate)
def create_book(book:BookCreate,db:Session=Depends(get_db)):
    data= Book(Title=book.Title,ISBN=book.ISBN,PublishedDate=book.PublishedDate,Genre=book.Genre)
    db.add(data)
    db.commit()
    return data

@app.get("/book/list/",response_model=list[BookCreate])
def list_users(db:Session=Depends(get_db)):
    return db.query(Book).all()

@app.get("/book/{book_id}",response_model=BookCreate)
def get_user(book_id:int,db:Session=Depends(get_db)):
    book=db.query(Book).filter(Book.BookID==book_id).first()
    if book is None:
        raise HTTPException(status_code=404,detail="book not found")
    return book


@app.post("/add_book_details")
def add_book_details(book_id: int,details: BookDetailsUpdate, db: Session = Depends(get_db)):
    existing_details = db.query(BookDetails).filter(BookDetails.BookID == book_id).first()
    if existing_details:
        raise HTTPException(status_code=400, detail="BookDetails already exists for this BookID")
    try:
        # Create a new BookDetails object
        book_details = BookDetails(
            BookID=book_id,
            NumberOfPages=details.NumberOfPages,
            Publisher=details.Publisher,
            Language=details.Language
        )

        # Add to the session and commit to the database
        db.add(book_details)
        db.commit()

        return {"message": "Book details added successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@app.put("/book/details/{book_id}", response_model=UpdateResponse)
def update_book_details(book_id: int, details: BookDetailsUpdate, db: Session = Depends(get_db)):
    book = db.query(BookDetails).filter(BookDetails.BookID == book_id).first()
    if book is None:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")

    # Update only provided fields
    if details.NumberOfPages is not None:
        book.NumberOfPages = details.NumberOfPages
    if details.Publisher is not None:
        book.Publisher = details.Publisher
    if details.Language is not None:
        book.Language = details.Language

    db.commit()
    db.refresh(book)

    response_data = {
        "message": "Book details updated successfully",
        "NumberOfPages": book.NumberOfPages,
        "Publisher": book.Publisher,
        "Language": book.Language,
    }

    return UpdateResponse(**response_data)

# BorrowedBooks APIs

@app.post("/borrowed_books/{user_id}/{book_id}")
def borrow_book(user_id: int, book_id: int, db: Session = Depends(get_db)):
    # check if the user and book exist
    user = db.query(user_model).filter(user_model.UserID == user_id).first()
    book = db.query(Book).filter(Book.BookID == book_id).first()

    if not user or not book:
        raise HTTPException(status_code=404, detail="User or book not found")

    # check if the book is already borrowed
    if db.query(BorrowedBooks).filter(BorrowedBooks.BookID == book_id, BorrowedBooks.ReturnDate.is_(None)).first():
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    # create the new borrowed book entry
    borrowed_book = BorrowedBooks(UserID=user_id, BookID=book_id)  
    db.add(borrowed_book)
    # db.commit()

    # Get the borrowed date
    BorrowedBooks.BorrowDate  = borrowed_book.BorrowDate 
    db.commit()

    return {"message": "Book borrowed successfully"}

@app.put("/return_book/{user_id}/{book_id}")
def return_book(user_id:int,book_id:int,db: Session = Depends(get_db)):
     # check if the user and book exist
    user = db.query(user_model).filter(user_model.UserID == user_id).first()
    book = db.query(Book).filter(Book.BookID == book_id).first()

    if not user or not book:
        raise HTTPException(status_code=404, detail="User or book not found")

    # check if the book is already borrowed
    book_borrow= db.query(BorrowedBooks).filter(BorrowedBooks.UserID == user_id,BorrowedBooks.BookID == book_id, BorrowedBooks.ReturnDate.is_(None)).first()
    
    if not book_borrow:
        raise HTTPException(status_code=400, detail="Book is not borrowed")
    book_borrow.ReturnDate=func.now()
    # db.commit()
    # Update return date to mark the book as available for borrowing again
    book_borrow.ReturnDate = None
    db.commit()

    return {"message": "Book returned successfully"}

@app.get("/borrowed/book_list/")
def borrowed_book_list(db:Session=Depends(get_db)):
    borrowed_books=db.query(BorrowedBooks).filter(BorrowedBooks.ReturnDate.is_(None)).all()
    return {"borrowed_books":borrowed_books}
