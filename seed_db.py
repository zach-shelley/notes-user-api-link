from app import app, db, User, Note

with app.app_context():
    # Clear and recreate
    db.drop_all()
    db.create_all()

    # Create users
    zach = User(username='zach', email='zach@example.com')
    alice = User(username='alice', email='alice@example.com')
    bob = User(username='bob', email='bob@example.com')

    db.session.add_all([zach, alice, bob])
    db.session.commit()  # Commit users first to get their IDs

    # Create notes (user_id is now available)
    notes = [
        Note(title='Flask Relationships', content='Learning foreign keys', user_id=zach.id),
        Note(title='Grocery List', content='Milk, eggs, bread', user_id=zach.id),
        Note(title='Project Ideas', content='Build a blog', user_id=zach.id),
        Note(title='Meeting Notes', content='Q4 planning session', user_id=alice.id),
        Note(title='Code Review', content='Check PR #42', user_id=alice.id),
        Note(title='Todo', content='Fix bug in login', user_id=bob.id),
    ]

    db.session.add_all(notes)
    db.session.commit()

    print("✓ Created 3 users")
    print("✓ Created 6 notes")
    print(f"  - Zach has {len(zach.notes)} notes")
    print(f"  - Alice has {len(alice.notes)} notes")
    print(f"  - Bob has {len(bob.notes)} notes")