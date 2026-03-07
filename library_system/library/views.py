from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Author, Book, Member, Loan
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    MemberSerializer,
    LoanSerializer
)
from django.http import HttpResponse, JsonResponse
import json


def home(request):
    # Get all data
    authors = Author.objects.all()
    books = Book.objects.all()
    members = Member.objects.all()
    loans = Loan.objects.all()
    
    # Handle POST requests for adding/editing/deleting items
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # AUTHOR ACTIONS
        if action == 'add_author':
            Author.objects.create(
                name=request.POST.get('name'),
                nationality=request.POST.get('nationality')
            )
            return redirect('home')
        
        elif action == 'edit_author':
            author_id = request.POST.get('author_id')
            author = Author.objects.get(id=author_id)
            author.name = request.POST.get('name')
            author.nationality = request.POST.get('nationality')
            author.save()
            return redirect('home')
        
        elif action == 'delete_author':
            author_id = request.POST.get('author_id')
            Author.objects.filter(id=author_id).delete()
            return redirect('home')
        
        # BOOK ACTIONS
        elif action == 'add_book':
            Book.objects.create(
                title=request.POST.get('title'),
                isbn=request.POST.get('isbn'),
                genre=request.POST.get('genre'),
                publication_date=request.POST.get('publication_date'),
                author_id=request.POST.get('author')
            )
            return redirect('home')
        
        elif action == 'edit_book':
            book_id = request.POST.get('book_id')
            book = Book.objects.get(id=book_id)
            book.title = request.POST.get('title')
            book.isbn = request.POST.get('isbn')
            book.genre = request.POST.get('genre')
            book.publication_date = request.POST.get('publication_date')
            book.author_id = request.POST.get('author')
            book.save()
            return redirect('home')
        
        elif action == 'delete_book':
            book_id = request.POST.get('book_id')
            Book.objects.filter(id=book_id).delete()
            return redirect('home')
        
        # MEMBER ACTIONS
        elif action == 'add_member':
            Member.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                membership_date=request.POST.get('membership_date')
            )
            return redirect('home')
        
        elif action == 'edit_member':
            member_id = request.POST.get('member_id')
            member = Member.objects.get(id=member_id)
            member.name = request.POST.get('name')
            member.email = request.POST.get('email')
            member.phone = request.POST.get('phone')
            member.membership_date = request.POST.get('membership_date')
            member.save()
            return redirect('home')
        
        elif action == 'delete_member':
            member_id = request.POST.get('member_id')
            Member.objects.filter(id=member_id).delete()
            return redirect('home')
        
        # LOAN ACTIONS
        elif action == 'add_loan':
            Loan.objects.create(
                member_id=request.POST.get('member'),
                book_id=request.POST.get('book'),
                loan_date=request.POST.get('loan_date'),
                due_date=request.POST.get('due_date'),
                return_date=request.POST.get('return_date') if request.POST.get('return_date') else None
            )
            return redirect('home')
        
        elif action == 'edit_loan':
            loan_id = request.POST.get('loan_id')
            loan = Loan.objects.get(id=loan_id)
            loan.member_id = request.POST.get('member')
            loan.book_id = request.POST.get('book')
            loan.loan_date = request.POST.get('loan_date')
            loan.due_date = request.POST.get('due_date')
            loan.return_date = request.POST.get('return_date') if request.POST.get('return_date') else None
            loan.save()
            return redirect('home')
        
        elif action == 'delete_loan':
            loan_id = request.POST.get('loan_id')
            Loan.objects.filter(id=loan_id).delete()
            return redirect('home')
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Library System Dashboard</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                    min-height: 100vh;
                    padding: 20px;
                    color: #e0e0e0;
                }}
                
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: rgba(20, 20, 30, 0.95);
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }}
                
                h1 {{
                    color: #00d4ff;
                    text-align: center;
                    margin-bottom: 10px;
                    font-size: 2.5em;
                    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
                }}
                
                .subtitle {{
                    text-align: center;
                    color: #8b8b8b;
                    margin-bottom: 40px;
                    font-size: 1.1em;
                }}
                
                .quick-links {{
                    display: flex;
                    gap: 15px;
                    margin-bottom: 40px;
                    justify-content: center;
                    flex-wrap: wrap;
                }}
                
                .quick-link {{
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    transition: all 0.3s;
                    border: 1px solid rgba(0, 212, 255, 0.3);
                }}
                
                .quick-link:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 5px 20px rgba(0, 212, 255, 0.4);
                    border-color: #00d4ff;
                }}
                
                .admin-link {{
                    background: linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%);
                }}
                
                .admin-link:hover {{
                    box-shadow: 0 5px 20px rgba(142, 45, 226, 0.4);
                }}
                
                .section {{
                    margin-bottom: 50px;
                }}
                
                .section-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #00d4ff;
                }}
                
                .section-title {{
                    color: #00d4ff;
                    font-size: 1.8em;
                    text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
                }}
                
                .add-btn {{
                    padding: 10px 20px;
                    background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 100%);
                    color: #0a0a0a;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1em;
                    font-weight: bold;
                    transition: all 0.3s;
                }}
                
                .add-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 20px rgba(0, 201, 255, 0.4);
                }}
                
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    background: rgba(30, 30, 40, 0.6);
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                    border-radius: 8px;
                    overflow: hidden;
                    border: 1px solid rgba(0, 212, 255, 0.2);
                }}
                
                thead {{
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    color: white;
                }}
                
                th, td {{
                    padding: 15px;
                    text-align: left;
                    color: #e0e0e0;
                }}
                
                tbody tr {{
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    transition: all 0.3s;
                }}
                
                tbody tr:hover {{
                    background: rgba(0, 212, 255, 0.1);
                }}
                
                .action-btn {{
                    padding: 6px 12px;
                    margin: 0 3px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 0.9em;
                    transition: all 0.2s;
                    font-weight: 500;
                }}
                
                .action-btn:hover {{
                    transform: scale(1.05);
                }}
                
                .edit-btn {{
                    background: #00d4ff;
                    color: #0a0a0a;
                }}
                
                .edit-btn:hover {{
                    box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
                }}
                
                .delete-btn {{
                    background: #ff006e;
                    color: white;
                }}
                
                .delete-btn:hover {{
                    box-shadow: 0 0 15px rgba(255, 0, 110, 0.5);
                }}
                
                .modal {{
                    display: none;
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0,0,0,0.8);
                    z-index: 1000;
                    justify-content: center;
                    align-items: center;
                    backdrop-filter: blur(5px);
                }}
                
                .modal.active {{
                    display: flex;
                }}
                
                .modal-content {{
                    background: linear-gradient(135deg, rgba(20, 20, 30, 0.98), rgba(30, 30, 50, 0.98));
                    padding: 30px;
                    border-radius: 15px;
                    max-width: 500px;
                    width: 90%;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                    max-height: 90vh;
                    overflow-y: auto;
                    border: 1px solid rgba(0, 212, 255, 0.3);
                }}
                
                .modal-header {{
                    font-size: 1.5em;
                    margin-bottom: 20px;
                    color: #00d4ff;
                    text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
                }}
                
                .form-group {{
                    margin-bottom: 15px;
                }}
                
                .form-group label {{
                    display: block;
                    margin-bottom: 5px;
                    color: #b0b0b0;
                    font-weight: 500;
                }}
                
                .form-group input,
                .form-group select {{
                    width: 100%;
                    padding: 10px;
                    border: 2px solid rgba(0, 212, 255, 0.3);
                    border-radius: 5px;
                    font-size: 1em;
                    background: rgba(10, 10, 20, 0.8);
                    color: #e0e0e0;
                }}
                
                .form-group input:focus,
                .form-group select:focus {{
                    outline: none;
                    border-color: #00d4ff;
                    box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
                }}
                
                .form-actions {{
                    display: flex;
                    gap: 10px;
                    margin-top: 20px;
                }}
                
                .submit-btn {{
                    flex: 1;
                    padding: 12px;
                    background: linear-gradient(135deg, #00c9ff 0%, #92fe9d 100%);
                    color: #0a0a0a;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1em;
                    font-weight: bold;
                }}
                
                .submit-btn:hover {{
                    box-shadow: 0 0 20px rgba(0, 201, 255, 0.4);
                }}
                
                .cancel-btn {{
                    flex: 1;
                    padding: 12px;
                    background: rgba(100, 100, 100, 0.6);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 1em;
                }}
                
                .cancel-btn:hover {{
                    background: rgba(120, 120, 120, 0.8);
                }}
                
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin-bottom: 40px;
                }}
                
                .stat-card {{
                    background: linear-gradient(135deg, rgba(30, 60, 114, 0.6) 0%, rgba(42, 82, 152, 0.6) 100%);
                    color: white;
                    padding: 25px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
                    border: 1px solid rgba(0, 212, 255, 0.3);
                    transition: all 0.3s;
                }}
                
                .stat-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 10px 30px rgba(0, 212, 255, 0.3);
                }}
                
                .stat-number {{
                    font-size: 2.5em;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color: #00d4ff;
                    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
                }}
                
                .stat-label {{
                    font-size: 1.1em;
                    opacity: 0.9;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐺 Library Management System</h1>
                <p class="subtitle">Full CRUD Operations - Create, Read, Update, Delete</p>
                
                <div class="quick-links">
                    <a href="/admin/" class="quick-link admin-link">🔐 Django Admin</a>
                    <a href="/api/authors/" class="quick-link">📝 Authors API</a>
                    <a href="/api/books/" class="quick-link">📖 Books API</a>
                    <a href="/api/members/" class="quick-link">👥 Members API</a>
                    <a href="/api/loans/" class="quick-link">📋 Loans API</a>
                </div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-number">{authors.count()}</div>
                        <div class="stat-label">Authors</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{books.count()}</div>
                        <div class="stat-label">Books</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{members.count()}</div>
                        <div class="stat-label">Members</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{loans.count()}</div>
                        <div class="stat-label">Active Loans</div>
                    </div>
                </div>
                
                <!-- AUTHORS SECTION -->
                <div class="section">
                    <div class="section-header">
                        <h2 class="section-title">✍️ Authors</h2>
                        <button class="add-btn" onclick="openAddAuthorModal()">+ Add Author</button>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Nationality</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join([f'''
                            <tr>
                                <td>{author.id}</td>
                                <td>{author.name}</td>
                                <td>{author.nationality}</td>
                                <td>
                                    <button class="action-btn edit-btn" onclick='openEditAuthorModal({json.dumps({"id": author.id, "name": author.name, "nationality": author.nationality})})'>Edit</button>
                                    <button class="action-btn delete-btn" onclick='confirmDelete("author", {author.id}, {json.dumps(author.name)})'>Delete</button>
                                </td>
                            </tr>
                            ''' for author in authors]) if authors.exists() else '<tr><td colspan="4" style="text-align:center; padding:20px; color:#8b8b8b;">No authors yet. Click "Add Author" to get started!</td></tr>'}
                        </tbody>
                    </table>
                </div>
                
                <!-- BOOKS SECTION -->
                <div class="section">
                    <div class="section-header">
                        <h2 class="section-title">📖 Books</h2>
                        <button class="add-btn" onclick="openAddBookModal()">+ Add Book</button>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Title</th>
                                <th>ISBN</th>
                                <th>Genre</th>
                                <th>Publication Date</th>
                                <th>Author</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join([f'''
                            <tr>
                                <td>{book.id}</td>
                                <td>{book.title}</td>
                                <td>{book.isbn}</td>
                                <td>{book.genre}</td>
                                <td>{book.publication_date}</td>
                                <td>{book.author.name}</td>
                                <td>
                                    <button class="action-btn edit-btn" onclick='openEditBookModal({json.dumps({"id": book.id, "title": book.title, "isbn": book.isbn, "genre": book.genre, "publication_date": str(book.publication_date), "author_id": book.author.id})})'>Edit</button>
                                    <button class="action-btn delete-btn" onclick='confirmDelete("book", {book.id}, {json.dumps(book.title)})'>Delete</button>
                                </td>
                            </tr>
                            ''' for book in books]) if books.exists() else '<tr><td colspan="7" style="text-align:center; padding:20px; color:#8b8b8b;">No books yet. Click "Add Book" to get started!</td></tr>'}
                        </tbody>
                    </table>
                </div>
                
                <!-- MEMBERS SECTION -->
                <div class="section">
                    <div class="section-header">
                        <h2 class="section-title">👥 Members</h2>
                        <button class="add-btn" onclick="openAddMemberModal()">+ Add Member</button>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Member Since</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join([f'''
                            <tr>
                                <td>{member.id}</td>
                                <td>{member.name}</td>
                                <td>{member.email}</td>
                                <td>{member.phone}</td>
                                <td>{member.membership_date}</td>
                                <td>
                                    <button class="action-btn edit-btn" onclick='openEditMemberModal({json.dumps({"id": member.id, "name": member.name, "email": member.email, "phone": member.phone, "membership_date": str(member.membership_date)})})'>Edit</button>
                                    <button class="action-btn delete-btn" onclick='confirmDelete("member", {member.id}, {json.dumps(member.name)})'>Delete</button>
                                </td>
                            </tr>
                            ''' for member in members]) if members.exists() else '<tr><td colspan="6" style="text-align:center; padding:20px; color:#8b8b8b;">No members yet. Click "Add Member" to get started!</td></tr>'}
                        </tbody>
                    </table>
                </div>
                
                <!-- LOANS SECTION -->
                <div class="section">
                    <div class="section-header">
                        <h2 class="section-title">📋 Loans</h2>
                        <button class="add-btn" onclick="openAddLoanModal()">+ Add Loan</button>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Member</th>
                                <th>Book</th>
                                <th>Loan Date</th>
                                <th>Due Date</th>
                                <th>Return Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join([f'''
                            <tr>
                                <td>{loan.id}</td>
                                <td>{loan.member.name}</td>
                                <td>{loan.book.title}</td>
                                <td>{loan.loan_date}</td>
                                <td>{loan.due_date}</td>
                                <td>{loan.return_date if loan.return_date else "Not returned"}</td>
                                <td>
                                    <button class="action-btn edit-btn" onclick='openEditLoanModal({json.dumps({"id": loan.id, "member_id": loan.member.id, "book_id": loan.book.id, "loan_date": str(loan.loan_date), "due_date": str(loan.due_date), "return_date": str(loan.return_date) if loan.return_date else ""})})'>Edit</button>
                                    <button class="action-btn delete-btn" onclick='confirmDelete("loan", {loan.id}, "loan record for {loan.book.title}")'>Delete</button>
                                </td>
                            </tr>
                            ''' for loan in loans]) if loans.exists() else '<tr><td colspan="7" style="text-align:center; padding:20px; color:#8b8b8b;">No loans yet. Click "Add Loan" to get started!</td></tr>'}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- DELETE CONFIRMATION MODAL -->
            <div id="deleteModal" class="modal">
                <div class="modal-content">
                    <h3 class="modal-header">⚠️ Confirm Delete</h3>
                    <p id="deleteMessage" style="margin-bottom: 20px; color: #b0b0b0;"></p>
                    <form method="POST" id="deleteForm">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                        <input type="hidden" name="action" id="deleteAction" value="">
                        <input type="hidden" name="author_id" id="deleteAuthorId" value="">
                        <input type="hidden" name="book_id" id="deleteBookId" value="">
                        <input type="hidden" name="member_id" id="deleteMemberId" value="">
                        <input type="hidden" name="loan_id" id="deleteLoanId" value="">
                        <div class="form-actions">
                            <button type="submit" class="delete-btn" style="flex: 1; padding: 12px; font-size: 1em;">Yes, Delete</button>
                            <button type="button" class="cancel-btn" onclick="closeModal('deleteModal')">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- ADD/EDIT AUTHOR MODAL -->
            <div id="authorModal" class="modal">
                <div class="modal-content">
                    <h3 class="modal-header" id="authorModalTitle">Add New Author</h3>
                    <form method="POST" id="authorForm">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                        <input type="hidden" name="action" id="authorAction" value="add_author">
                        <input type="hidden" name="author_id" id="authorId" value="">
                        <div class="form-group">
                            <label>Name:</label>
                            <input type="text" name="name" id="authorName" required>
                        </div>
                        <div class="form-group">
                            <label>Nationality:</label>
                            <input type="text" name="nationality" id="authorNationality" required>
                        </div>
                        <div class="form-actions">
                            <button type="submit" class="submit-btn" id="authorSubmitBtn">Add Author</button>
                            <button type="button" class="cancel-btn" onclick="closeModal('authorModal')">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- ADD/EDIT BOOK MODAL -->
            <div id="bookModal" class="modal">
                <div class="modal-content">
                    <h3 class="modal-header" id="bookModalTitle">Add New Book</h3>
                    <form method="POST" id="bookForm">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                        <input type="hidden" name="action" id="bookAction" value="add_book">
                        <input type="hidden" name="book_id" id="bookId" value="">
                        <div class="form-group">
                            <label>Title:</label>
                            <input type="text" name="title" id="bookTitle" required>
                        </div>
                        <div class="form-group">
                            <label>ISBN:</label>
                            <input type="text" name="isbn" id="bookIsbn" required>
                        </div>
                        <div class="form-group">
                            <label>Genre:</label>
                            <input type="text" name="genre" id="bookGenre" required>
                        </div>
                        <div class="form-group">
                            <label>Publication Date:</label>
                            <input type="date" name="publication_date" id="bookPubDate" required>
                        </div>
                        <div class="form-group">
                            <label>Author:</label>
                            <select name="author" id="bookAuthor" required>
                                <option value="">Select an author</option>
                                {''.join([f'<option value="{author.id}">{author.name}</option>' for author in authors])}
                            </select>
                        </div>
                        <div class="form-actions">
                            <button type="submit" class="submit-btn" id="bookSubmitBtn">Add Book</button>
                            <button type="button" class="cancel-btn" onclick="closeModal('bookModal')">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- ADD/EDIT MEMBER MODAL -->
            <div id="memberModal" class="modal">
                <div class="modal-content">
                    <h3 class="modal-header" id="memberModalTitle">Add New Member</h3>
                    <form method="POST" id="memberForm">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                        <input type="hidden" name="action" id="memberAction" value="add_member">
                        <input type="hidden" name="member_id" id="memberId" value="">
                        <div class="form-group">
                            <label>Name:</label>
                            <input type="text" name="name" id="memberName" required>
                        </div>
                        <div class="form-group">
                            <label>Email:</label>
                            <input type="email" name="email" id="memberEmail" required>
                        </div>
                        <div class="form-group">
                            <label>Phone:</label>
                            <input type="tel" name="phone" id="memberPhone" required>
                        </div>
                        <div class="form-group">
                            <label>Membership Date:</label>
                            <input type="date" name="membership_date" id="membershipDate" required>
                        </div>
                        <div class="form-actions">
                            <button type="submit" class="submit-btn" id="memberSubmitBtn">Add Member</button>
                            <button type="button" class="cancel-btn" onclick="closeModal('memberModal')">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- ADD/EDIT LOAN MODAL -->
            <div id="loanModal" class="modal">
                <div class="modal-content">
                    <h3 class="modal-header" id="loanModalTitle">Add New Loan</h3>
                    <form method="POST" id="loanForm">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', '')}">
                        <input type="hidden" name="action" id="loanAction" value="add_loan">
                        <input type="hidden" name="loan_id" id="loanId" value="">
                        <div class="form-group">
                            <label>Member:</label>
                            <select name="member" id="loanMember" required>
                                <option value="">Select a member</option>
                                {''.join([f'<option value="{member.id}">{member.name}</option>' for member in members])}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Book:</label>
                            <select name="book" id="loanBook" required>
                                <option value="">Select a book</option>
                                {''.join([f'<option value="{book.id}">{book.title}</option>' for book in books])}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Loan Date:</label>
                            <input type="date" name="loan_date" id="loanDate" required>
                        </div>
                        <div class="form-group">
                            <label>Due Date:</label>
                            <input type="date" name="due_date" id="dueDate" required>
                        </div>
                        <div class="form-group">
                            <label>Return Date (optional):</label>
                            <input type="date" name="return_date" id="returnDate">
                        </div>
                        <div class="form-actions">
                            <button type="submit" class="submit-btn" id="loanSubmitBtn">Add Loan</button>
                            <button type="button" class="cancel-btn" onclick="closeModal('loanModal')">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <script>
                // DELETE CONFIRMATION
                function confirmDelete(type, id, name) {{
                    document.getElementById('deleteMessage').textContent = `Are you sure you want to delete "${{name}}"? This action cannot be undone.`;
                    document.getElementById('deleteAction').value = `delete_${{type}}`;
                    
                    // Reset all delete IDs
                    document.getElementById('deleteAuthorId').value = '';
                    document.getElementById('deleteBookId').value = '';
                    document.getElementById('deleteMemberId').value = '';
                    document.getElementById('deleteLoanId').value = '';
                    
                    // Set the appropriate ID
                    document.getElementById(`delete${{type.charAt(0).toUpperCase() + type.slice(1)}}Id`).value = id;
                    
                    document.getElementById('deleteModal').classList.add('active');
                }}
                
                // AUTHOR MODALS
                function openAddAuthorModal() {{
                    document.getElementById('authorModalTitle').textContent = 'Add New Author';
                    document.getElementById('authorAction').value = 'add_author';
                    document.getElementById('authorSubmitBtn').textContent = 'Add Author';
                    document.getElementById('authorId').value = '';
                    document.getElementById('authorName').value = '';
                    document.getElementById('authorNationality').value = '';
                    document.getElementById('authorModal').classList.add('active');
                }}
                
                function openEditAuthorModal(data) {{
                    document.getElementById('authorModalTitle').textContent = 'Edit Author';
                    document.getElementById('authorAction').value = 'edit_author';
                    document.getElementById('authorSubmitBtn').textContent = 'Update Author';
                    document.getElementById('authorId').value = data.id;
                    document.getElementById('authorName').value = data.name;
                    document.getElementById('authorNationality').value = data.nationality;
                    document.getElementById('authorModal').classList.add('active');
                }}
                
                // BOOK MODALS
                function openAddBookModal() {{
                    document.getElementById('bookModalTitle').textContent = 'Add New Book';
                    document.getElementById('bookAction').value = 'add_book';
                    document.getElementById('bookSubmitBtn').textContent = 'Add Book';
                    document.getElementById('bookId').value = '';
                    document.getElementById('bookTitle').value = '';
                    document.getElementById('bookIsbn').value = '';
                    document.getElementById('bookGenre').value = '';
                    document.getElementById('bookPubDate').value = '';
                    document.getElementById('bookAuthor').value = '';
                    document.getElementById('bookModal').classList.add('active');
                }}
                
                function openEditBookModal(data) {{
                    document.getElementById('bookModalTitle').textContent = 'Edit Book';
                    document.getElementById('bookAction').value = 'edit_book';
                    document.getElementById('bookSubmitBtn').textContent = 'Update Book';
                    document.getElementById('bookId').value = data.id;
                    document.getElementById('bookTitle').value = data.title;
                    document.getElementById('bookIsbn').value = data.isbn;
                    document.getElementById('bookGenre').value = data.genre;
                    document.getElementById('bookPubDate').value = data.publication_date;
                    document.getElementById('bookAuthor').value = data.author_id;
                    document.getElementById('bookModal').classList.add('active');
                }}
                
                // MEMBER MODALS
                function openAddMemberModal() {{
                    document.getElementById('memberModalTitle').textContent = 'Add New Member';
                    document.getElementById('memberAction').value = 'add_member';
                    document.getElementById('memberSubmitBtn').textContent = 'Add Member';
                    document.getElementById('memberId').value = '';
                    document.getElementById('memberName').value = '';
                    document.getElementById('memberEmail').value = '';
                    document.getElementById('memberPhone').value = '';
                    document.getElementById('membershipDate').value = '';
                    document.getElementById('memberModal').classList.add('active');
                }}
                
                function openEditMemberModal(data) {{
                    document.getElementById('memberModalTitle').textContent = 'Edit Member';
                    document.getElementById('memberAction').value = 'edit_member';
                    document.getElementById('memberSubmitBtn').textContent = 'Update Member';
                    document.getElementById('memberId').value = data.id;
                    document.getElementById('memberName').value = data.name;
                    document.getElementById('memberEmail').value = data.email;
                    document.getElementById('memberPhone').value = data.phone;
                    document.getElementById('membershipDate').value = data.membership_date;
                    document.getElementById('memberModal').classList.add('active');
                }}
                
                // LOAN MODALS
                function openAddLoanModal() {{
                    document.getElementById('loanModalTitle').textContent = 'Add New Loan';
                    document.getElementById('loanAction').value = 'add_loan';
                    document.getElementById('loanSubmitBtn').textContent = 'Add Loan';
                    document.getElementById('loanId').value = '';
                    document.getElementById('loanMember').value = '';
                    document.getElementById('loanBook').value = '';
                    document.getElementById('loanDate').value = '';
                    document.getElementById('dueDate').value = '';
                    document.getElementById('returnDate').value = '';
                    document.getElementById('loanModal').classList.add('active');
                }}
                
                function openEditLoanModal(data) {{
                    document.getElementById('loanModalTitle').textContent = 'Edit Loan';
                    document.getElementById('loanAction').value = 'edit_loan';
                    document.getElementById('loanSubmitBtn').textContent = 'Update Loan';
                    document.getElementById('loanId').value = data.id;
                    document.getElementById('loanMember').value = data.member_id;
                    document.getElementById('loanBook').value = data.book_id;
                    document.getElementById('loanDate').value = data.loan_date;
                    document.getElementById('dueDate').value = data.due_date;
                    document.getElementById('returnDate').value = data.return_date;
                    document.getElementById('loanModal').classList.add('active');
                }}
                
                function closeModal(modalId) {{
                    document.getElementById(modalId).classList.remove('active');
                }}
                
                // Close modal when clicking outside
                window.onclick = function(event) {{
                    if (event.target.classList.contains('modal')) {{
                        event.target.classList.remove('active');
                    }}
                }}
            </script>
        </body>
    </html>
    """
    return HttpResponse(html)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer