# 라이브러리 불러오기
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, MaxPooling1D, GlobalMaxPooling1D, Dense
import numpy as np
from konlpy.tag import Okt
import re

# 예시 레시피 데이터 준비
recipes = [
    "고구마를 깨끗이 씻고 쪄서 으깬다. 버터를 넣고 섞어 반죽을 만든다.",
    "닭고기를 소금과 후추로 간을 하고 구워준다.",
    "양파와 당근을 잘게 썰어 볶다가 토마토소스를 넣고 끓인다.",
    "소고기를 다져서 소금, 후추로 간하고, 팬에 구워낸다.",
    "밥에 참기름과 김가루를 넣고 섞는다. 계란을 올린다.",
    "오이 토막은 밑부분 1.5cm 정도만 남기고 열십(+)자로 칼집을 넣어주세요",
    "핏물 뺀 돼지고기를 넣어주세요",
    "버섯을 얇게 썰어 소금과 후추로 간을 하고 팬에 볶아준다.",
    "고기를 재워둔 후 기름에 튀긴다.",
    "양파와 마늘을 다져서 기름에 볶다가 소스를 붓고 졸인다.",
    "채소를 씻어서 깨끗하게 다듬어 채를 썬다.",
    "감자를 삶아서 으깨고, 버터와 섞는다.",
    "생선을 손질한 후 간장에 재워둔다.",
    "마늘을 다지고, 고추를 썰어 팬에 볶는다.",
    "계란을 풀어 팬에 부쳐서 지단을 만든다.",
    "파를 송송 썰어 국에 넣고 끓인다.",
    "불고기를 양념에 재워서 하루 동안 냉장고에 둔다.",
    "소고기를 얇게 썰어, 팬에 구워서 접시에 담는다.",
    "양파를 볶아 카레 가루를 넣고 함께 끓인다.",
    "생선을 손질하고 소금으로 간을 한 후 구워준다.",
]

labels = [
    "고구마", "닭고기", "토마토소스", "소고기", "밥", "오이", "돼지고기",
    "버섯", "고기", "양파", "채소", "감자", "생선", "마늘", "계란", "파", 
    "불고기", "소고기", "카레", "생선"
]

# 형태소 분석기
okt = Okt()

# 불용어 목록 확장
custom_stop_words = ['맛있', '좋', '완성']

def preprocess_text(text):
    # 한글과 공백을 제외한 모든 문자 제거
    text = re.sub("[^가-힣\s]", "", text)
    # 형태소 분석 후 동사와 형용사 추출 및 어간 추출
    tokens = okt.pos(text, stem=True)
    verbs_adjectives = [word for word, pos in tokens if pos in ['Verb', 'Adjective']]
    return ' '.join(verbs_adjectives)

# 레시피 전처리
processed_recipes = [preprocess_text(recipe) for recipe in recipes]

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(stop_words=['을', '를', '이', '가', '은', '는', '에', '와', '과'] + custom_stop_words)
X_tfidf = vectorizer.fit_transform(processed_recipes)

# 단어의 중요도 출력
important_words = vectorizer.get_feature_names_out()
print("TF-IDF 중요 단어:", important_words)

# 중요 단어 기반 텍스트 필터링
filtered_recipes = []
for i, recipe in enumerate(processed_recipes):
    filtered_words = [word for word in recipe.split() if word in important_words]
    filtered_recipes.append(' '.join(filtered_words))

# 텍스트 전처리
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(filtered_recipes)
sequences = tokenizer.texts_to_sequences(filtered_recipes)
word_index = tokenizer.word_index
X = pad_sequences(sequences, maxlen=100)

# 레이블 인코딩
encoder = LabelEncoder()
y = encoder.fit_transform(labels)

# 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# CNN 모델 정의
model = Sequential()
model.add(Embedding(len(word_index) + 1, 128, input_length=100))
model.add(Conv1D(128, 5, activation='relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(Conv1D(128, 5, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# 모델 컴파일 및 훈련
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# 모델 훈련
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_data=(X_test, y_test))

# 모델 평가
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# 새로운 텍스트
new_text = "모든 양념은 냄비에 한번에 넣어 팔팔 끓여주세요 ~"

# 텍스트 전처리
processed_text = preprocess_text(new_text)

# 불용어 포함 여부 확인
contains_stop_word = any(word in processed_text for word in custom_stop_words)

if contains_stop_word:
    print("중요하지 않음 : 불용어 포함")
else:
    # 새로운 텍스트에 대해 TF-IDF 적용
    new_tfidf_vector = vectorizer.transform([processed_text])

    # 단어와 해당 TF-IDF 점수를 매칭 및 중요도 평가
    word_tfidf = dict(zip(vectorizer.get_feature_names_out(), new_tfidf_vector.toarray().flatten()))

    # TF-IDF 점수가 높은 단어들을 출력
    sorted_word_tfidf = sorted(word_tfidf.items(), key=lambda item: item[1], reverse=True)
    print("단어별 TF-IDF 중요도:")
    for word, score in sorted_word_tfidf:
        print(f"{word}: {score:.4f}")

    # 중요한 단어가 있는지 확인하고 출력
    important_found = any(score > 0 for word, score in word_tfidf.items())

    if important_found:
        print("중요")
    else:
        print("중요하지 않음: 중요한 단어 없음")
