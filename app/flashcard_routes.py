# flashcard_routes.py
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import FlashcardSet, Flashcard
from app import db

flashcard_bp = Blueprint('flashcard', __name__)

@flashcard_bp.route('/flashcards')
@login_required
def flashcards():
    return render_template('flashcards.html')

@flashcard_bp.route('/flashcard-sets')
@login_required
def get_flashcard_sets():
    flashcard_sets = current_user.flashcard_sets.all()
    sets_data = []
    for flashcard_set in flashcard_sets:
        flashcards_data = []
        for flashcard in flashcard_set.flashcards:
            flashcards_data.append({
                'id': flashcard.id,
                'question': flashcard.question,
                'answer': flashcard.answer
            })
        sets_data.append({
            'id': flashcard_set.id,
            'name': flashcard_set.name,
            'flashcards': flashcards_data
        })
    return jsonify({'flashcard_sets': sets_data})

@flashcard_bp.route('/flashcard-sets', methods=['POST'])
@login_required
def create_flashcard_set():
    set_name = request.json['name']
    flashcard_set = FlashcardSet(name=set_name, user=current_user)
    db.session.add(flashcard_set)
    db.session.commit()
    return jsonify({'id': flashcard_set.id, 'name': flashcard_set.name})

@flashcard_bp.route('/flashcards', methods=['POST'])
@login_required
def create_flashcard():
    set_id = request.json['setId']
    question = request.json['question']
    answer = request.json['answer']
    flashcard_set = FlashcardSet.query.get(set_id)
    if flashcard_set and flashcard_set.user == current_user:
        flashcard = Flashcard(question=question, answer=answer, flashcard_set=flashcard_set)
        db.session.add(flashcard)
        db.session.commit()
        return jsonify({'id': flashcard.id, 'question': flashcard.question, 'answer': flashcard.answer})
    return jsonify({'error': 'Invalid flashcard set'}), 400
