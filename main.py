from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import threading

app = Flask(__name__)
CORS(app) # Quan trọng: Cho phép Web từ InfinityFree gọi tới

def execute_logic(api_url, data):
    try:
        # Tải code Python từ Mockbin
        response = requests.get(api_url, timeout=10)
        code = response.text
        
        # Môi trường chạy code, code trên Mockbin dùng target_data để lấy info
        exec_globals = {
            "target_data": data,
            "requests": requests,
            "threading": threading,
            "time": __import__('time'),
            "re": __import__('re')
        }
        exec(code, exec_globals)
    except Exception as e:
        print(f"Lỗi: {e}")

@app.route('/')
def home():
    return "Backend DuyKhang đang chạy!"

@app.route('/run', methods=['POST'])
def run():
    params = request.json
    url_map = {
        "1": "https://89641e6231be4f32b9260c1d4cd60879.api.mockbin.io/",
        "2": "https://219b5601f63b4eae9b4a24817b011a19.api.mockbin.io/",
        "3": "https://7d483a5ecdbc4ba284ae04460e1e0b3b.api.mockbin.io/",
        "4": "https://17ffd9b550fb4626aab442e49509dd2c.api.mockbin.io/"
    }
    
    target_api = url_map.get(str(params.get('id')))
    if target_api:
        threading.Thread(target=execute_logic, args=(target_api, params)).start()
        return jsonify({"status": "success", "message": "Đã kích hoạt module!"})
    return jsonify({"status": "error", "message": "ID không hợp lệ"}), 400

if __name__ == "__main__":
    app.run()
    
