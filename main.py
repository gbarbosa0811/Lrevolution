from sqlalchemy import create_engine, Text, Column, Uuid, String, Enum, TIMESTAMP, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

db = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=db)
session = Session()


Base = declarative_base()

#Banco usuário
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String)
    password_hash = Column("password_hash", String)
    avatar_url = Column("avatar_url", String) #foto de perfil
    bio = Column("bio", String)
    role = Column("role", Enum)
    created_at = Column(TIMESTAMP, server_default=func.now())

    def __init__ (self, name, email, password_hash, avatar_url, bio, role, created_at):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.avatar_url = avatar_url
        self.bio = bio
        self.role = role
        self.created_at = created_at

#Banco metas de leitura
class Reading_goal(Base):
    __tablename__ = "Reading_goals"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    target_books = Column("target_books", Integer)
    complete_books = Column("complete_books", Integer)
    year = Column("year", Integer)
    create_at = Column("create_at", TIMESTAMP)

    def __init__ (self, id, user_id, target_books, complete_books, year, create_at):
        self.user_id = user_id
        self.target_books = target_books
        self.complete_books = complete_books
        self.year = year
        self.create_at = create_at

#Banco livros
class Book(Base):
    __tablename__ = "books"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String)
    author = Column("author", String)
    isbn = Column("isbn", String)
    cover_url = Column("cover_url", String) # URl da capa do livro
    description = Column("description", String)
    genre = Column("genre", String)
    page_count = Column("page_count", Integer)
    published_year = Column("published_year", Integer)
    avg_rating = Column("avg_rating", Float)

    def __init__(self, id, title, author, isbn, cover_url, description, genre, page_count, published_year, avg_rating):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.cover_url = cover_url
        self.description = description
        self.genre = genre
        self.page_count = page_count
        self.published_year = published_year
        self.avg_rating = avg_rating

#banco livros do usuário
class User_book(Base):
    __tablename__ = "user_books"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"))
    book_id = Column("book_id", Integer, ForeignKey("books.id"))
    status = Column("status", Enum)
    current_page = Column("current_page", Integer)
    rating = Column("rating", Integer)
    review = Column("review", Text)
    started_at = Column("started_at", TIMESTAMP)
    finished_at = Column("finished_at", TIMESTAMP)
    added_at = Column("added_at", TIMESTAMP)

    def __init__(self, id, user_id, book_id, status, current_page, rating, review, started_at, finished_at, added_at):
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.status = status
        self.current_page = current_page
        self.rating = rating
        self.review = review
        self.started_at = started_at
        self.finished_at = finished_at
        self.added_at = added_at

#Banco tag dos livros
class Book_tag(Base):
    __tablename__ = "book_tags"

    id = Column("id", Integer, primary_key=True)
    book_id = Column("book_id", Integer, ForeignKey("books.id"))
    tag_id = Column("tag_id", Integer)

    def __init__(self, id, book_id, tag_id):
        self.id = id
        self.book_id = book_id
        self.tag_id = tag_id

#Banco tags
class Tag(Base):
    __tablename__ = "tags"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    slug = Column("slug", String) #é a parte final e legível de uma URL

    def __init__(self, id, name, slug):
        self.id = id
        self.name = name
        self.slug = slug

#Banco leitura compartilhada
class Shared_reading(Base):
    __tablename__ = "shared_readings"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book_id = Column("book_id", ForeignKey("books.id"))
    created_by = Column("created_by", Uuid)
    title = Column("title", String)
    start_page = Column("start_page", Integer)
    end_page = Column("end page", Integer)
    status = Column("status", Enum)
    max_participants = Column("max_participants", Integer)
    scheduled_at = Column("scheduled_at", TIMESTAMP)
    ended_at = Column("ended_at", TIMESTAMP)

    def __init__ (self, id, book_id, created_by, title, start_page, end_page, status, max_participants, scheduled_at, ended_at):
        self.id = id
        self.book_id = book_id
        self.created_by = created_by
        self.title = title
        self.start_page = start_page
        self.end_page = end_page
        self.status = status
        self.max_participants = max_participants
        self.scheduled_at = scheduled_at
        self.ended_at = ended_at

#Banco participantes da sessão
class Session_participant(Base):
    __tablename__ = "session_participants"

    id = Column("id", Integer, primary_key=True)
    session_id = Column("session_id", Uuid)
    user_id = Column("user_id", ForeignKey("users.id"))
    current_page = Column("current_page", Integer)
    joined_at = Column("joined_at", TIMESTAMP)

    def __init__ (self, id, session_id, user_id, current_page, joined_at):
        self.id = id
        self.session_id = session_id
        self.user_id = user_id
        self.current_page = current_page
        self.joined_at = joined_at
            
#Banco notas da sessão
class Session_note(Base):
    __tablename__ = "session_notes"

    id = Column("id", Integer, primary_key=True)
    session_id = Column("session_id", Uuid)
    user_id = Column("user_id", ForeignKey("users.id"))
    page_ref = Column("page_ref", Integer)
    content = Column("content", Text)
    created_at = Column("created_at", TIMESTAMP)

    def __init__ (self, id, session_id, user_id, page_ref, content, created_at):
        self.id = id
        self.session_id = session_id
        self.user_id = user_id
        self.page_ref = page_ref
        self.content = content
        self.created_at = created_at

#banco Debates
class Debate(Base):
    __tablename__ = "debates"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book_id = Column("book_id", ForeignKey("books.id"))
    host_id = Column("host_id", Uuid)
    title = Column("title", String)
    description = Column("description", String)
    status = Column("status", Enum)
    max_participants = Column("max_participants", Integer)
    schedulet_at = Column("scheduled_at", TIMESTAMP)
    started_at = Column("started_at", TIMESTAMP)
    ended_at = Column("ended_at", TIMESTAMP)

    def __init__ (self, book_id, host_id, title, description, status, max_participants, schedulet_at, started_at, ended_at):
        self.book_id = book_id
        self.host_id = host_id
        self.title = title
        self.description = description
        self.status = status
        self.max_participants = max_participants
        self.schedulet_at = schedulet_at
        self.started_at = started_at
        self.ended_at = ended_at

#Banco participantes do debate
class Debate_participant(Base):
    __tablename__ = "debate_participants"

    id = Column("id", Integer, primary_key=True)
    debate_id = Column("debate_id", ForeignKey("debates.id"))
    user_id = Column("user_id", ForeignKey("users.id"))
    role = Column("role", Enum)
    joined_at = Column("joined_at", TIMESTAMP)

    def __init__ (self, id, debate_id, user_id, role, joinet_at):
        self.id = id
        self.debate_id = debate_id
        self.user_id = user_id
        self.role = role
        self.joined_at = joinet_at

#Banco mensagens do debate
class Debate_message(Base):
    __tablename__ = "debate_messages"

    id = Column("id", Integer, primary_key=True)
    debate_id = Column("debate_id", Uuid)
    user_id = Column("user_id", ForeignKey("users.id"))
    content = Column("content", Text)
    reply_to = Column("reply_to", Uuid)
    sent_at = Column("sent_at", TIMESTAMP)

    def __init__ (self, id, debate_id, user_id, content, reply_to, sent_at):
        self.id = id
        self.debate_id = debate_id
        self.user_id = user_id
        self.content = content
        self.reply_to = reply_to
        self.sent_at = sent_at
    
#Banco recomendações
class Recomendation(Base):
    __tablename__ = "recomendations"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", ForeignKey("users.id"))
    book_id = Column("book_id", ForeignKey("books.id"))
    score = Column("score", Float)
    reason = Column("reason", String)
    seen = Column("seen", Boolean)
    dismissed = Column("dismissed", Boolean)
    generated_at = Column("genereted_at", TIMESTAMP)

    def __init__ (self, id, user_id, book_id, score, reason, dismissed, generated_at):
        self.id = id
        self.user_id = user_id
        self.book_id = book_id
        self.score = score
        self.reason = reason
        self.dismissed = dismissed
        self.generated_at = generated_at

#Banco feedback das recomendações
class Recomendation_feedback(Base):
    __tablename__ = "recomendations_feedbacks"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    recomendation_id = Column("recomendation_id", Uuid)
    user_id = Column("user_id", ForeignKey("users.id"))
    action = Column("action", Enum)
    created_at = Column("created_at", TIMESTAMP)

    def __init__ (self, id, recomendation_id, user_id, action, created_at):
        self.id = id
        self.recomendation_id = recomendation_id
        self.user_id = user_id
        self.action = action
        self.created_at = created_at

        
Base.metadata.create_all(bind=db)