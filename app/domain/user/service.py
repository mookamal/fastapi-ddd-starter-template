from app.domain.user.entity import User
from app.infrastructure.security.password import PasswordManager


class AuthService:
    def __init__(self, password_manager: PasswordManager):
        self.password_manager = password_manager
    
    def create_user(self, name: str, email: str, password: str) -> User:
        if not email or not password or not name:
            raise ValueError("Name, email and password are required")
        
        user = User(name=name, email=email)
        
        if not user.is_valid_email():
            raise ValueError("Invalid email format")
        
        user.password_hash = self.password_manager.hash_password(password)
        return user
    
    def verify_password(self, user: User, password: str) -> bool:
        return self.password_manager.verify_password(password, user.password_hash)