import os
from flask import Flask, render_template, request, jsonify
from matcher import ProposalMatcher

app = Flask(__name__)
matcher = ProposalMatcher()

@app.route('/')
def index():
    meta = matcher.get_proposal_meta()
    questions = matcher.get_suggested_questions()
    return render_template('index.html', proposal=meta, questions=questions)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'No question provided'}), 400
    result = matcher.get_answer(query)
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
