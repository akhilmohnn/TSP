from app import app, db

with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(db.text("DROP TABLE IF EXISTS add_auditor"))
        conn.execute(db.text("DROP TABLE IF EXISTS auditor"))
        conn.commit()

    print("✅ Old tables dropped successfully!")
