from flask import Flask, request, send_file
import edge_tts, os

app = Flask(__name__)

@app.route('/process_file', methods=['POST'])
def process_file():
    try:
        # 检查请求中是否包含文件
        if 'file' not in request.files:
            return "file not found", 400

        file = request.files['file']
        wav_filename = 'summary_any.wav'
        # 读取文件内容
        file_content = file.read()

        communicate = edge_tts.Communicate(text=file_content.decode('utf-8'),
                voice="zh-CN-XiaoxiaoNeural",
                rate='+100%',
                volume= '+0%',
                pitch= '+0Hz')
        communicate.save_sync(wav_filename)
        # 检查文件是否存在
        if os.path.exists(wav_filename):
            # 使用 send_file 函数发送文件给客户端
            return send_file(wav_filename, as_attachment=True)
        else:
            return "file not exist", 404
        # return file_content
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
