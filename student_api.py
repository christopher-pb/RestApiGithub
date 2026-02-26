from flask import Flask, jsonify

app = Flask(__name__)

students = [
    {"id": 1, "name": "Akshay", "grade": "A"},
    {"id": 2, "name": "John", "grade": "B"},
]

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
