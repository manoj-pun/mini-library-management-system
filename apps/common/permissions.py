from rest_framework.permissions import BasePermission

class IsLibrarian(BasePermission):
    message = "You're not allowed to perform this action."

    def has_permission(self,request):
        return request.user.is_authenticated and request.user.role == "LIBRARIAN"