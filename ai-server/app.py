import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import torch
from yolov5 import detect

# NotImplementedError: cannot instantiate 'PosixPath' on your system 해결
from pathlib import Path
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

app = Flask(__name__)

FoodList = [
    "Kochujang", "Apple", "Avocado", "Bacon", "Banana", "Beef", "Bread", "Burdock", "Butter",
    "Cabbage", "Canned Corn", "Canned Tuna", "Carrot", "Cheese", "Chicken", "Chili Powder",
    "Chocolate Bread", "Cinnamon", "Cooking Oil", "Corn", "Cornflake", "Crab Meat", "Cucumber",
    "Curry Powder", "Dumpling", "Egg", "Fish Cake", "French Fries", "Garlic", "Ginger",
    "Green Onion", "Ham", "Hash Brown", "Hotdog", "Ice", "Ketchup", "Kimchi", "Lemon",
    "Lemon Juice", "Mandarin", "Marshmallow", "Mayonnaise", "Milk", "Mozzarella Cheese",
    "Mushroom", "Mustard", "Nacho Chips", "Noodle", "Nutella", "Olive Oil", "Onion", "Oreo",
    "Parmesan Cheese", "Parsley", "Pasta", "Peanut Butter", "Pear", "Pepper", "Pepper Powder",
    "Pickle", "Pickled Radish", "Pimento", "Pineapple", "Pork", "Potato", "Ramen", "Red Wine",
    "Rice", "Salt", "Sausage", "Seaweed", "Sesame", "Sesame Oil", "Shrimp Paste", "Soy Sauce",
    "Spam", "Squid", "Strawberry", "Sugar", "Sweet Potato", "Tofu", "Tomato", "Wasabi",
    "Watermelon", "Whipping Cream"
]

def transform_labels(translated_labels):
    transformed_labels = [label.lower().replace(' ', '_') for label in translated_labels]
    return transformed_labels

@app.route('/detection', methods=['GET', 'POST'])
def predict():
    output_labels = []
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)

        os.makedirs('./input_dir', exist_ok=True)
        file.save(os.path.join('./input_dir', filename))
        train_img = './input_dir/' + file.filename

        weights = '.\\yolov5\\runs\\train\\exp6\\weights\\best.pt'  # YOLOv5 모델 가중치 경로
        img_size = 640  # 이미지 사이즈

        # YOLOv5 모델 로드
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights)
        model.eval()

        # 이미지 예측
        results = model(train_img, size=img_size)

        # 예측된 결과 처리
        if results and results.pred[0] is not None:
            for *box, conf, cls in results.pred[0]:
                output_labels.append(model.names[int(cls)])

            translated_labels = [FoodList[label] if label in FoodList else label for label in output_labels]

            transformed_labels = transform_labels(translated_labels)

            return jsonify(transformed_labels), 200
        else:
            return jsonify({"error": "No detections made"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0')