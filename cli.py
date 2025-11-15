#!/usr/bin/env python3

import typer
from faker import Faker
from lorem_text import lorem
import random
import sqlite3
import os
from flask import Flask
from app import app, db, User, Post
from datetime import datetime, timedelta
import csv
import secrets
import string

cli = typer.Typer()
fake = Faker()

def get_db_connection():
    """
    Get a connection to the SQLite database.
    """

    return sqlite3.connect('./instance/blog.db')

@cli.command()
def seed_users():
    """
    Seed the database with 10 test users.
    """

    def generate_strong_password(length=16):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    with app.app_context():
        print("Seeding database with 10 test users...")
        users = []
        for i in range(1, 11):
            username = f"testuser{i}"
            password = generate_strong_password()

            existing = User.query.filter_by(username=username).first()
            if existing:
                print(f"User {username} already exists, skipping.")
                continue

            user = User(username=username)
            user.set_password(password)
            users.append(user)

            db.session.add(user)

            print(f"Created {username} with password: {password}")
        db.session.commit()
        print(f"Created {len(users)} test users.")

@cli.command()
def seed_posts(
    posts_per_user: int = typer.Option(3, help="Number of posts per user"),
    min_words: int = typer.Option(50, help="Minimum words per post"),
    max_words: int = typer.Option(200, help="Maximum words per post")
):
    """
    Seed the database with random posts for the 10 test users.
    """

    with app.app_context():
        users = User.query.filter(User.username.like("testuser%")).order_by(User.username).all()

        if len(users) < 10:
            print("Not all test users found. Please run the seed_users command first.", err=True)
            raise typer.Exit(code=0)

        print(f"Seeding posts for {len(users)} test users...")

        total_posts = 0
        for user in users:
            for _ in range(posts_per_user):
                title = fake.sentence(nb_words=random.randint(3, 8))
                word_count = random.randint(min_words, max_words)
                content = lorem.paragraphs(random.randint(1, 5))
                created_at = datetime.utcnow() - timedelta(days=random.randint(0, 365))
                post = Post(
                    title=title,
                    content=content,
                    user_id=user.id,
                    created_at=created_at
                )
                db.session.add(post)
                total_posts += 1

        db.session.commit()

        print(f"Created {total_posts} posts for test users.")

@cli.command()
def cleanup_seed():
    """
    Remove all test users and their posts from the database.
    """

    with app.app_context():
        print("Cleaning up test users and their posts...")

        test_users = User.query.filter(User.username.like("testuser%")).all()
        if not test_users:
            print("No test users found. Nothing to clean up.")
            raise typer.Exit(code=0)

        test_user_ids = [user.id for user in test_users]
        deleted_posts = Post.query.filter(Post.user_id.in_(test_user_ids)).delete(synchronize_session=False)
        deleted_users = User.query.filter(User.id.in_(test_user_ids)).delete(synchronize_session=False)

        db.session.commit()

        print(f"Deleted {deleted_posts} posts and {deleted_users} test users.")
    
@cli.command()
def check_db():
    """
    Check if the database is available and accessible.
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # check if any tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("Database exists but no tables found!")
            raise typer.Exit(code=0)
        
        # check if any table has any records
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Table '{table_name}' has {count} records")
        
        conn.close()
        print("Database check completed successfully!")
        
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise typer.Exit(code=1)

@cli.command()
def list_routes():
    """
    List all available routes in the Flask application.
    """

    print("Available routes:")
    
    with app.app_context():
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            print(f"{rule.endpoint:20} {rule.rule:30} {methods}")

if __name__ == "__main__":
    cli()