"""
References : https://www.dataquest.io/blog/documenting-in-python-with-docstrings/#:~:text=Docstrings%20explain%20what%20a%20function,want%20to%20use%20the%20code.
Author  : Joel Wembo

This is a pure Python implementation of Dynamic Programming solution to the longest
increasing subsequence of a given sequence.

The problem is  :
Given an array, to find the longest and increasing sub-array in that given array and
return it.
Example: [10, 22, 9, 33, 21, 50, 41, 60, 80] as input will return
         [10, 22, 33, 41, 60, 80] as output
"""

from datetime import datetime
import uuid
from django.db import models


TYPES = [
    ("expense", "Expense"),
    ("income", "Income"),
    ("transfer", "Transfer"),
]

# Coding Documentation standards
# def add_binary(a, b):
#     '''
#     Returns the sum of two decimal numbers in binary digits.

#             Parameters:
#                     a (int): A decimal integer
#                     b (int): Another decimal integer

#             Returns:
#                     binary_sum (str): Binary string of the sum of a and b
#     '''
#     binary_sum = bin(a+b)[2:]
#     return binary_sum

# print(add_binary.__doc__)

class Transaction(models.Model):
    
    """
    some explaination of the function
    >>> LongestIncreasingSubsequenceLength([2, 5, 3, 7, 11, 8, 10, 13, 6])
    6
    >>> LongestIncreasingSubsequenceLength([])
    0

    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(default=datetime.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPES, default="expense")
    category = models.ForeignKey(
        "Category", on_delete=models.DO_NOTHING, related_name="transactions"
    )
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, related_name="transactions"
    )
    
    """
      Get Timestamps from the user
      Return date & time
    """
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
     
    # transaction meta
    # meta class
    
    class Meta:
        db_table = "Transactions"
        ordering = ['-createdAt']

        def __str__(self):
            return f"{self.date} - {self.amount} - {self.description}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="subcategories",
        null=True,
        blank=True,
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Categories"
        ordering = ['-createdAt']

        def __str__(self):
            return self.name


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "Accounts"
        ordering = ['-createdAt']
        def __str__(self):
            return self.name
        
