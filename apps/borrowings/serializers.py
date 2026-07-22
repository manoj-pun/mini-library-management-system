from rest_framework import serializers
from .models import Borrowing

class BorrowCreateSerializer(serializers.ModelSerializer):

    """
    Serializer for borrowing book.
    """

    class Meta:
        model = Borrowing
        fields = ["book"]


class BorrowListSerializer(serializers.ModelSerializer):

    """
    Serializer for listing the borrowings.
    """

    membership_number = serializers.CharField(source="member.membership_number")

    class Meta:
        model = Borrowing
        fields = ["id", "membership_number", "book", "status", "due_date"]


class BorrowDetailSerializer(serializers.ModelSerializer):

    """
    Serializer for retrieving borrowings.
    """

    membership_number = serializers.CharField(source="member.membership_number")

    class Meta:
        model = Borrowing
        fields = ["id", "membership_number", "book", "borrowed_date", "due_date", "returned_date", "status", "is_overdue", 
                  "days_overdue", "fine_amount", "fine_paid"]