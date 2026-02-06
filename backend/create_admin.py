#!/usr/bin/env python3
"""
Admin User Creation/Update Script for Home Assistant Addon

This script creates or updates the admin user based on environment variables
set by the addon configuration. It should be run after database initialization.
"""

import os
import sys

# Add backend to path
sys.path.insert(0, '/app')

def create_or_update_admin():
    """Create or update admin user from environment variables"""
    
    from backend.extensions import db
    from backend.models.user import User
    from backend.utills.security import hash_password
    from flask import Flask
    
    # Get admin credentials from environment
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    
    if not admin_email or not admin_password:
        print("ERROR: ADMIN_EMAIL and ADMIN_PASSWORD environment variables must be set")
        sys.exit(1)
    
    # Create minimal Flask app for database context
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or \
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST', 'mysql')}/{os.getenv('MYSQL_DATABASE')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    with app.app_context():
        try:
            # Ensure tables exist
            db.create_all()
            
            # Check if admin user exists
            admin = User.query.filter_by(email=admin_email).first()
            
            if admin:
                print(f"Updating existing admin user: {admin_email}")
                admin.password = hash_password(admin_password)
                admin.role = '1'  # Ensure admin role
                print("  - Password updated")
                print("  - Role set to admin (1)")
            else:
                print(f"Creating new admin user: {admin_email}")
                admin = User(
                    email=admin_email,
                    password=hash_password(admin_password),
                    role='1'
                )
                db.session.add(admin)
                print("  - Admin user created with role 1")
            
            db.session.commit()
            print("✓ Admin user initialized successfully")
            return 0
            
        except Exception as e:
            print(f"ERROR: Failed to create/update admin user: {e}")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == "__main__":
    sys.exit(create_or_update_admin())
