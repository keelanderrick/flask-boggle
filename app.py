from msilib.schema import Billboard
from pydoc import render_doc
from boggle import Boggle
from flask import Flask, render_template, session, request, jsonify

boggle_game = Boggle()
app = Flask(__name__)
app.config["SECRET_KEY"] = "jkasdnfsaoifnasdfwern"


@app.route("/")
def home():
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    return render_template("index.html", board=board, highscore=highscore, plays=plays)


@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    plays = session.get("plays", 0)

    session['plays'] = plays + 1
    session['highscore'] = max(score, highscore)

    if (score > highscore):
        return jsonify(newRecord=True)
    return jsonify(newRecord=False)
