from app import app, db, Vocabulary, LearningApp

# Sample vocabulary data
vocabulary_data = [
    {
        'word': 'こんにちは',
        'meaning': 'hello, good afternoon (konnichiwa)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': 'ありがとう',
        'meaning': 'thank you (arigatou)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': 'おはよう',
        'meaning': 'good morning (ohayou)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': 'さようなら',
        'meaning': 'goodbye (sayounara)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': 'はい',
        'meaning': 'yes (hai)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': 'いいえ',
        'meaning': 'no (iie)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': '水',
        'meaning': 'water (mizu)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': '食べる',
        'meaning': 'to eat (taberu)',
        'language': 'Japanese',
        'difficulty_level': 2
    },
    {
        'word': '飲む',
        'meaning': 'to drink (nomu)',
        'language': 'Japanese',
        'difficulty_level': 2
    },
    {
        'word': '行く',
        'meaning': 'to go (iku)',
        'language': 'Japanese',
        'difficulty_level': 2
    },
    {
        'word': '来る',
        'meaning': 'to come (kuru)',
        'language': 'Japanese',
        'difficulty_level': 2
    },
    {
        'word': '見る',
        'meaning': 'to see/watch (miru)',
        'language': 'Japanese',
        'difficulty_level': 2
    },
    {
        'word': '私',
        'meaning': 'I/me (watashi)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': 'あなた',
        'meaning': 'you (anata)',
        'language': 'Japanese',
        'difficulty_level': 1
    },
    {
        'word': '今日',
        'meaning': 'today (kyou)',
        'language': 'Japanese',
        'difficulty_level': 1
    }
]

# Sample learning apps
learning_apps_data = [
    {
        'name': 'Hiragana Practice',
        'description': 'Learn and practice Japanese Hiragana characters',
        'url': '/apps/hiragana',
        'icon': 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/icons/card-text.svg'
    },
    {
        'name': 'Kanji Quiz',
        'description': 'Test your knowledge of basic Kanji characters',
        'url': '/apps/kanji',
        'icon': 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/icons/question-circle.svg'
    },
    {
        'name': 'Japanese Writing',
        'description': 'Practice writing Japanese characters',
        'url': '/apps/writing',
        'icon': 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/icons/pencil.svg'
    }
]

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Add vocabulary
        for vocab_item in vocabulary_data:
            vocabulary = Vocabulary(**vocab_item)
            db.session.add(vocabulary)

        # Add learning apps
        for app_item in learning_apps_data:
            learning_app = LearningApp(**app_item)
            db.session.add(learning_app)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
