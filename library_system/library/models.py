from django.db import models

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=150)
    isbn = models.CharField(max_length=20)
    genre = models.CharField(max_length=50)
    publication_date = models.DateField()

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    membership_date = models.DateField()

    def __str__(self):
        return self.name


class Loan(models.Model):
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    loan_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member} borrowed {self.book}"

