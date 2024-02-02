from sqlalchemy import create_engine,Column,Integer,String,DateTime,ForeignKey, func
from sqlalchemy.orm import sessionmaker,Session 
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# create engine and session
url="postgresql://postgres:post@localhost/library_mngt" 
engine=create_engine(url)
Session=sessionmaker(bind=engine)
Base=declarative_base()


# define the database models
class user_model(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)
    Email = Column(String, unique=True, index=True)
    MembershipDate = Column(DateTime)
    borrowed_books = relationship("BorrowedBooks", back_populates="user")

class Book(Base):
    __tablename__ = "Book"
    BookID = Column(Integer, primary_key=True, index=True)
    Title = Column(String)
    ISBN = Column(String, unique=True)
    PublishedDate = Column(DateTime)
    Genre = Column(String)
    book_details = relationship("BookDetails", back_populates="book")
    borrowed_books = relationship("BorrowedBooks", back_populates="book")

class BookDetails(Base):
    __tablename__ = "Book_Details"
    DetailsID = Column(Integer, primary_key=True, index=True)
    BookID = Column(Integer, ForeignKey("Book.BookID"))
    NumberOfPages = Column(Integer)
    Publisher = Column(String)
    Language = Column(String)
    book = relationship("Book", back_populates="book_details")

class BorrowedBooks(Base):
    __tablename__ = "Borrowed_books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey("users.UserID", ondelete="CASCADE"))  
    BookID = Column(Integer, ForeignKey("Book.BookID", ondelete="CASCADE"))
    BorrowDate = Column(DateTime(timezone=True), server_default=func.now())
    ReturnDate = Column(DateTime,nullable=True)

    user = relationship("user_model", back_populates="borrowed_books")
    book = relationship("Book", back_populates="borrowed_books")



# Create tables in the database
Base.metadata.create_all(engine)


