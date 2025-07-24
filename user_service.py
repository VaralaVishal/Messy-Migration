import sqlite3
import bcrypt

def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect('users.db', check_same_thread=False)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def validate_user_data(data):
    """Validate user input data"""
    if not data.get('name') or not data.get('email'):
        return False, "Name and email are required"
    
    if '@' not in data.get('email', ''):
        return False, "Invalid email format"
    
    if len(data.get('name', '').strip()) < 2:
        return False, "Name must be at least 2 characters"
    
    return True, None

class UserService:
    """Service class for user CRUD operations"""
    
    @staticmethod
    def get_all_users():
        """Fetch all users from database"""
        conn = get_db_connection()
        if not conn:
            return None, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            users = cursor.fetchall()
            user_list = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
            return user_list, None
        except Exception as e:
            return None, "Failed to fetch users"
        finally:
            conn.close()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Fetch user by ID"""
        conn = get_db_connection()
        if not conn:
            return None, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if user:
                return {"id": user[0], "name": user[1], "email": user[2]}, None
            else:
                return None, "User not found"
        except Exception as e:
            return None, "Failed to fetch user"
        finally:
            conn.close()
    
    @staticmethod
    def create_user(data):
        """Create new user"""
        # Validate input
        is_valid, error_message = validate_user_data(data)
        if not is_valid:
            return None, error_message
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data.get('password', '')
        
        if len(password) < 6:
            return None, "Password must be at least 6 characters"
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        conn = get_db_connection()
        if not conn:
            return None, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                          (name, email, password_hash))
            conn.commit()
            return {"message": "User created successfully"}, None
        except Exception as e:
            return None, "Failed to create user"
        finally:
            conn.close()
    
    @staticmethod
    def update_user(user_id, data):
        """Update existing user"""
        # Validate input
        is_valid, error_message = validate_user_data(data)
        if not is_valid:
            return None, error_message
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        
        conn = get_db_connection()
        if not conn:
            return None, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", 
                          (name, email, user_id))
            
            if cursor.rowcount == 0:
                return None, "User not found"
            
            conn.commit()
            return {"message": "User updated successfully"}, None
        except Exception as e:
            return None, "Failed to update user"
        finally:
            conn.close()
    
    @staticmethod
    def delete_user(user_id):
        """Delete user by ID"""
        conn = get_db_connection()
        if not conn:
            return None, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            if cursor.rowcount == 0:
                return None, "User not found"
            
            conn.commit()
            return {"message": "User deleted successfully"}, None
        except Exception as e:
            return None, "Failed to delete user"
        finally:
            conn.close()
    
    @staticmethod
    def search_users(name):
        """Search users by name"""
        if not name:
            return None, "Please provide a name to search"
        
        conn = get_db_connection()
        if not conn:
            return None, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f'%{name}%',))
            users = cursor.fetchall()
            user_list = [{"id": user[0], "name": user[1], "email": user[2]} for user in users]
            return user_list, None
        except Exception as e:
            return None, "Search failed"
        finally:
            conn.close()
    
    @staticmethod
    def authenticate_user(email, password):
        """Authenticate user login"""
        if not email or not password:
            return None, "Email and password required"
        
        conn = get_db_connection()
        if not conn:
            return None, "Database connection failed"
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE email = ?", (email.strip().lower(),))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user[1]):
                return {"user_id": user[0]}, None
            else:
                return None, "Invalid credentials"
        except Exception as e:
            return None, "Login failed"
        finally:
            conn.close()
