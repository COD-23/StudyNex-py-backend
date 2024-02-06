import inspect

if not hasattr(inspect, "signature"):
    inspect.signature = inspect.signature


import nltk
import random
import json
import PyPDF2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

nltk.download("punkt")


class QuizGenerator:
    def __init__(self, text):
        self.sentences = nltk.sent_tokenize(text)
        self.questions = []
        self.common_words = set(
            [
                "i",
                "you",
                "we",
                "they",
                "me",
                "him",
                "her",
                "us",
                "them",
                "your",
                "my",
                "his",
                "its",
                "our",
                "their",
                "mine",
                "hers",
                "ours",
                "theirs",
                "am",
                "is",
                "are",
                "was",
                "were",
                "be",
                "been",
                "being",
                "have",
                "has",
                "had",
                "do",
                "does",
                "did",
                "doing",
                "a",
                "an",
                "the",
                "and",
                "but",
                "or",
                "if",
                "because",
                "as",
                "since",
                "while",
                "when",
                "where",
                "before",
                "after",
                "with",
                "at",
                "by",
                "on",
                "in",
                "to",
                "from",
                "through",
                "over",
                "under",
                "above",
                "below",
                "up",
                "down",
                "out",
                "off",
                "on",
                "between",
                "among",
                "throughout",
                "into",
                "onto",
                "of",
                "for",
                "with",
                "within",
                "about",
                "against",
                "between",
                "into",
                "during",
                "before",
                "after",
                "above",
                "below",
                "to",
                "from",
                "up",
                "down",
                "through",
                "over",
                "under",
                "again",
                "further",
                "then",
                "once",
                "here",
                "there",
                "when",
                "where",
                "why",
                "how",
                "all",
                "any",
                "both",
                "each",
                "few",
                "more",
                "most",
                "other",
                "some",
                "such",
                "no",
                "nor",
                "not",
                "only",
                "own",
                "same",
                "so",
                "than",
                "too",
                "very",
                "s",
                "t",
                "can",
                "will",
                "just",
                "don",
                "should",
                "now",
                "d",
                "ll",
                "m",
                "o",
                "re",
                "ve",
                "y",
                "ain",
                "aren",
                "couldn",
                "didn",
                "doesn",
                "hadn",
                "hasn",
                "haven",
                "isn",
                "ma",
                "mightn",
                "mustn",
                "needn",
                "shan",
                "shouldn",
                "wasn",
                "weren",
                "won",
                "wouldn",
                ",",
                ".",
                "-",
                ":",
                ";",
                "?",
                "/",
                "(",
                ")",
                "()",
                "{",
                "}",
                "[",
                "]",
            ]
        )

    def generate_quiz(self, num_questions=5, num_choices=4):
        for sentence in random.sample(self.sentences, num_questions):
            words = nltk.word_tokenize(sentence)

            eligible_words = [
                word for word in words if word.lower() not in self.common_words
            ]

            if not eligible_words:
                continue

            blank_index = random.randint(0, len(eligible_words) - 1)
            answer = eligible_words[blank_index]

            choices = random.sample(
                set(eligible_words) - {answer},
                min(num_choices - 1, len(eligible_words) - 1),
            )
            choices.append(answer)
            random.shuffle(choices)

            blanked_sentence = " ".join(
                ["_" if word == answer else word for word in words]
            )
            question = {
                "question": blanked_sentence,
                "options": choices,
                "answer": answer,
            }

            self.questions.append(question)

        return self.questions


@app.route("/generate_quiz", methods=["POST"])
def generate_quiz_from_pdf():
    pdf_file = request.files.get("file")

    if pdf_file and pdf_file.filename.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

        quiz_generator = QuizGenerator(text)
        quiz = quiz_generator.generate_quiz(num_questions=10, num_choices=4)

        return jsonify({"quiz": quiz})
    else:
        return jsonify({"error": "Invalid or no PDF file provided"}), 400


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
    # app.run(debug=True)
