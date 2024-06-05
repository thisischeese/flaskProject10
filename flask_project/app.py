from flask import Flask, render_template, jsonify,request
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
from model import Base, Info, Worksheet, History, Note
from datetime import datetime
from sqlalchemy.sql import func
import config

app = Flask(__name__)

# Connecting Database
engine = create_engine(config.DB_URL)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mypage')
def mypage():
    return 'This is My Page!'

@app.route('/mynote/<string:my_id>/')
# mypage에서 mynote 접속 시 my_id 문자열과 일치하는 모든 notes 조회
def readNoteList(my_id):
    user_info = session.query(Info).filter_by(id=my_id).first()
    if not user_info:
        return jsonify({"error": "id not found"}), 404
    else:
        user_notes = session.query(Note).filter_by(email=user_info.email).all()
        user_notes_data = []
        for note in user_notes:
            user_notes_data.append({
                "seq": note.seq,
                "date": note.date.isoformat(),
                "memo": note.memo,
                "email": note.email,
                "word": note.word
            })
        return jsonify(user_notes_data)

@app.route('/mynote/<string:my_id>/<int:mynote_seq>/delete/', methods=['DELETE'])
# memoList 화면에서 Note 삭제
def deleteNote(my_id, mynote_seq):
    user_info = session.query(Info).filter_by(id=my_id).first()
    if not user_info:
        return jsonify({"error": "id not found"}), 404
    else:
        user_note = session.query(Note).filter_by(email=user_info.email, seq=mynote_seq).first()
        if not user_note:
            return jsonify({"error": "note not found"}), 404
        else:
            session.delete(user_note)
            session.commit()
            return jsonify({"success": "Note deleted successfully"}), 200

@app.route('/mynote/<string:my_id>/<int:mynote_seq>')
# memoView 화면에서 노트 정보 조회해옴
def readNote(my_id, mynote_seq):
    user_info = session.query(Info).filter_by(id=my_id).first()
    if not user_info:
        return jsonify({"error": "id not found"}), 404
    else:
        user_note = session.query(Note).filter_by(email=user_info.email, seq=mynote_seq).first()
        if not user_note:
            return jsonify({"error": "note not found"}), 404
        else:
            user_note_data = {
                "seq": user_note.seq,
                "date": user_note.date.isoformat(),
                "memo": user_note.memo,
                "email": user_note.email,
                "word": user_note.word
            }
            return jsonify(user_note_data)


@app.route('/mynote/<string:my_id>/new', methods=['POST'])
def newNoteRoute(my_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    my_word = data.get('word')
    my_memo = data.get('memo')
    return newNote(my_id, my_word, my_memo)

def newNote(my_id, my_word, my_memo):
    user_info = session.query(Info).filter_by(id=my_id).first()
    if not user_info:
        return jsonify({"error": "id not found"}), 404

    max_seq = session.query(Note).filter_by(email=user_info.email).order_by(Note.seq.desc()).first()
    new_seq = 1 if max_seq is None else max_seq.seq + 1
    new_note = Note(
        seq=new_seq,
        date=func.current_date(),
        memo=my_memo,
        word=my_word,
        email=user_info.email
    )
    session.add(new_note)
    session.commit()
    return jsonify({"success": "successfully created new memo"})


@app.route('/mynote/check_word/<string:my_id>', methods=['POST'])
def checkWordRoute(my_id):
    data = request.json
    if not data or 'word' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    my_word = data['word']
    exists = checkWord(my_word)  # Check if the word exists

    return jsonify({"exists": exists}), 200

def checkWord(my_word):
    # Logic to check if the word exists in the worksheet
    worksheet_word = session.query(Worksheet).filter_by(word=my_word).first()
    return worksheet_word is not None

@app.route('/mynote/<string:my_id>/<int:mynote_seq>/update', methods=['POST','GET'])
# memoView 화면에서 기존에 존재하는 노트의 메모 내용을 업데이트
def updateMemo(my_id, mynote_seq):
    data = request.json
    new_memo = data.get('memo')
    user_info = session.query(Info).filter_by(id=my_id).first()
    if not user_info:
        return jsonify({"error": "id not found"}), 404
    user_note = session.query(Note).filter_by(email=user_info.email, seq=mynote_seq).first()
    if not user_note:
        return jsonify({"error": "note not found"}), 404
    user_note.memo = new_memo
    session.commit()
    return jsonify({"success": "Memo updated successfully"}), 200


@app.route('/mynote/<string:my_id>/list')
# 메모 리스트 화면 접속
def memoListPage(my_id):
    return render_template('memoList.html', my_id=my_id)

@app.route('/mynote/<string:my_id>/<int:mynote_seq>/view')
# 메모 조회 화면 접속
def memoViewPage(my_id, mynote_seq):
    return render_template('memoView.html', my_id=my_id, mynote_seq=mynote_seq)

@app.route('/mynote/<string:my_id>/newpage')
# 새로운 메모 생성 화면 접속
def memoNewPage(my_id):
    return render_template('memoNew.html', my_id=my_id)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)