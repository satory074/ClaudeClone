from flask import Flask, request, jsonify, render_template
import anthropic
import json

app = Flask(__name__)

# env.json から API キーを読み込む
with open('env.json') as f:
    env = json.load(f)

API_KEY = env.get('CLAUDE_API_KEY')
if not API_KEY:
    raise ValueError("CLAUDE_API_KEY is not set in env.json.")

# Claude APIクライアントの初期化
client = anthropic.Anthropic(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        user_message = request.json.get('message', '')

        if not user_message:
            return jsonify({'error': 'Message content is empty.'}), 400

        # Claude APIへのリクエスト
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=512
        )

        # 応答の検証
        if 'completion' in response:
            return jsonify({'response': response['completion']})
        else:
            return jsonify({'error': 'Invalid response from Claude API.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
