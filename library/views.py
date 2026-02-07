from django.shortcuts import render
from rest_framework import viewsets
from .models import Author, Book, Member, Loan
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    MemberSerializer,
    LoanSerializer
)
from django.http import HttpResponse

def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Library System API</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                
                .container {
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    max-width: 600px;
                    width: 100%;
                    padding: 50px;
                }
                
                h1 {
                    color: #2c3e50;
                    font-size: 2.5em;
                    margin-bottom: 10px;
                    text-align: center;
                }
                
                .subtitle {
                    text-align: center;
                    color: #7f8c8d;
                    margin-bottom: 40px;
                    font-size: 1.1em;
                }
                
                .admin-section {
                    margin-bottom: 30px;
                }
                
                .admin-link {
                    display: flex;
                    align-items: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 12px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
                }
                
                .admin-link:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 8px 25px rgba(245, 87, 108, 0.5);
                }
                
                .section-title {
                    color: #2c3e50;
                    font-size: 1.2em;
                    margin-bottom: 15px;
                    font-weight: 600;
                }
                
                .api-links {
                    display: grid;
                    gap: 15px;
                }
                
                .api-link {
                    display: flex;
                    align-items: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 12px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                }
                
                .api-link:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
                }
                
                .icon {
                    font-size: 2em;
                    margin-right: 20px;
                }
                
                .link-content h3 {
                    font-size: 1.3em;
                    margin-bottom: 5px;
                }
                
                .link-content p {
                    font-size: 0.9em;
                    opacity: 0.9;
                }
                
                .footer {
                    margin-top: 40px;
                    text-align: center;
                    color: #95a5a6;
                    font-size: 0.9em;
                }
                
                @media (max-width: 600px) {
                    .container {
                        padding: 30px;
                    }
                    
                    h1 {
                        font-size: 2em;
                    }
                    
                    .icon {
                        font-size: 1.5em;
                        margin-right: 15px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📚 Library System</h1>
                <p class="subtitle">RESTful API Management Portal</p>
                
                <div class="admin-section">
                    <h2 class="section-title">⚙️ Administration</h2>
                    <a href="/admin/" class="admin-link">
                        <div class="icon">🔐</div>
                        <div class="link-content">
                            <h3>Django Admin Panel</h3>
                            <p>Manage all database models</p>
                        </div>
                    </a>
                </div>
                
                <h2 class="section-title">🔌 API Endpoints</h2>
                <div class="api-links">
                    <a href="/api/authors/" class="api-link">
                        <div class="icon">✍️</div>
                        <div class="link-content">
                            <h3>Authors</h3>
                            <p>Manage author records and profiles</p>
                        </div>
                    </a>
                    
                    <a href="/api/books/" class="api-link">
                        <div class="icon">📖</div>
                        <div class="link-content">
                            <h3>Books</h3>
                            <p>Browse and manage book inventory</p>
                        </div>
                    </a>
                    
                    <a href="/api/members/" class="api-link">
                        <div class="icon">👥</div>
                        <div class="link-content">
                            <h3>Members</h3>
                            <p>View and manage library members</p>
                        </div>
                    </a>
                    
                    <a href="/api/loans/" class="api-link">
                        <div class="icon">📋</div>
                        <div class="link-content">
                            <h3>Loans</h3>
                            <p>Track book lending and returns</p>
                        </div>
                    </a>
                </div>
                
                <div class="footer">
                    <p>Powered by Django REST Framework</p>
                </div>
            </div>
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