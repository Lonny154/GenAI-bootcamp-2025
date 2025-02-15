from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func, case

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///language_portal.db'
db = SQLAlchemy(app)

# Models
class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    meaning = db.Column(db.String(500), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    difficulty_level = db.Column(db.Integer, default=1)

class LearningRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabulary.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class LearningApp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    url = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(200))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vocabulary', methods=['GET'])
def get_vocabulary():
    vocabulary = Vocabulary.query.all()
    return jsonify([{
        'id': v.id,
        'word': v.word,
        'meaning': v.meaning,
        'language': v.language,
        'difficulty_level': v.difficulty_level
    } for v in vocabulary])

@app.route('/record', methods=['POST'])
def record_attempt():
    data = request.json
    record = LearningRecord(
        user_id=data['user_id'],
        vocabulary_id=data['vocabulary_id'],
        is_correct=data['is_correct']
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/apps', methods=['GET'])
def get_apps():
    apps = LearningApp.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'description': a.description,
        'url': a.url,
        'icon': a.icon
    } for a in apps])

@app.route('/api/items')
def get_items():
    vocabulary = Vocabulary.query.all()
    return jsonify([{
        'id': item.id,
        'word': item.word,
        'meaning': item.meaning,
        'language': item.language,
        'difficulty_level': item.difficulty_level
    } for item in vocabulary])

# Learning app routes
@app.route('/apps/hiragana')
def hiragana_practice():
    hiragana = [
        {'char': 'あ', 'romaji': 'a'},
        {'char': 'い', 'romaji': 'i'},
        {'char': 'う', 'romaji': 'u'},
        {'char': 'え', 'romaji': 'e'},
        {'char': 'お', 'romaji': 'o'}
    ]
    return render_template('learning_app.html', 
                         title='Hiragana Practice',
                         content=hiragana,
                         app_type='hiragana')

@app.route('/apps/kanji')
def kanji_quiz():
    kanji = [
        {'char': '水', 'meaning': 'water', 'reading': 'みず (mizu)'},
        {'char': '火', 'meaning': 'fire', 'reading': 'ひ (hi)'},
        {'char': '木', 'meaning': 'tree', 'reading': 'き (ki)'}
    ]
    return render_template('learning_app.html', 
                         title='Kanji Quiz',
                         content=kanji,
                         app_type='kanji')

@app.route('/apps/writing')
def writing_practice():
    words = [word for word in Vocabulary.query.all()]
    return render_template('learning_app.html', 
                         title='Writing Practice',
                         content=words,
                         app_type='writing')

# Dashboard routes
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats', methods=['GET'])
def get_user_stats():
    user_id = request.args.get('user_id', 'default_user')  # In future, get from auth
    
    # Get total attempts
    total_attempts = LearningRecord.query.filter_by(user_id=user_id).count()
    
    # Get correct attempts
    correct_attempts = LearningRecord.query.filter_by(
        user_id=user_id,
        is_correct=True
    ).count()
    
    # Calculate accuracy
    accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
    
    # Get daily progress for the last 7 days
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    daily_progress = db.session.query(
        func.date(LearningRecord.timestamp).label('date'),
        func.count(LearningRecord.id).label('attempts'),
        func.sum(case((LearningRecord.is_correct == True, 1), else_=0)).label('correct')
    ).filter(
        LearningRecord.user_id == user_id,
        LearningRecord.timestamp >= seven_days_ago
    ).group_by(
        func.date(LearningRecord.timestamp)
    ).all()
    
    # Get progress by language
    language_progress = db.session.query(
        Vocabulary.language,
        func.count(LearningRecord.id).label('attempts'),
        func.sum(case((LearningRecord.is_correct == True, 1), else_=0)).label('correct')
    ).join(
        Vocabulary,
        LearningRecord.vocabulary_id == Vocabulary.id
    ).filter(
        LearningRecord.user_id == user_id
    ).group_by(
        Vocabulary.language
    ).all()
    
    return jsonify({
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'accuracy': round(accuracy, 1),
        'daily_progress': [{
            'date': str(record.date),
            'attempts': record.attempts,
            'correct': record.correct
        } for record in daily_progress],
        'language_progress': [{
            'language': record.language,
            'attempts': record.attempts,
            'correct': record.correct
        } for record in language_progress]
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
