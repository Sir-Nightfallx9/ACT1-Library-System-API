from rest_framework import serializers
from .models import Author, Book, Member, Loan

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'name', 'nationality']

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'isbn', 'genre', 'publication_date', 'author']

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ['url', 'id', 'name', 'email', 'phone', 'membership_date']

class LoanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Loan
        fields = ['url', 'id', 'member', 'book', 'loan_date', 'due_date', 'return_date']
