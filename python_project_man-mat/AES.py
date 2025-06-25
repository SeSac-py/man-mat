import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sentence_transformers import SentenceTransformer
import warnings

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)

warnings.filterwarnings("ignore")

# 전처리 함수 수정 (문자열 반환)
def preprocess_text(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return ' '.join(lemmatized_tokens)  # 문자열로 반환

# 채점/평가
# 1. 정확 일치
def exact_match(expected_answer, student_answer):
    return int(expected_answer == student_answer)

# 2. 부분 일치
def partial_match(expected_answer, student_answer):
    expected_tokens = preprocess_text(expected_answer)
    student_tokens = preprocess_text(student_answer)
    common_tokens = set(expected_tokens) & set(student_tokens)
    match_percentage = len(common_tokens) / max(len(expected_tokens), len(student_tokens))
    return match_percentage

# 3. 코사인 유사도 (TF-IDF) - 벡터라이저 호환성 개선
def cosine_similarity_score(expected_answer, student_answer):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([preprocess_text(expected_answer), 
                                            preprocess_text(student_answer)])
    if tfidf_matrix.shape[0] < 2:
        return 0.0
    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

# 4. 감정 분석 점수
def sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    return (sentiment_score + 1) / 2  # [0, 1]로 정규화

# 5 & 7. Sentence-BERT - 모델 캐싱 추가
sbert_model = None
def get_sbert_model():
    global sbert_model
    if sbert_model is None:
        sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    return sbert_model

def enhanced_sentence_match(expected_answer, student_answer):
    model = get_sbert_model()
    embeddings = model.encode([expected_answer, student_answer])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

def semantic_similarity_score(expected_answer, student_answer):
    return enhanced_sentence_match(expected_answer, student_answer)  # 중복 제거

# 6. Multinomial Naive Bayes - 안정성 개선
def multinomial_naive_bayes_score(expected_answer, student_answer):
    try:
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform([expected_answer, student_answer])
        if X.shape[1] == 0:  # 빈 어휘 사전 방지
            return 0.5
        clf = MultinomialNB()
        clf.fit(X, [0, 1])
        return clf.predict_proba(X)[1][1]
    except:
        return 0.5

# 8. Coherence - 빈 문자열 처리
def coherence_score(expected_answer, student_answer):
    len_expected = len(word_tokenize(expected_answer))
    len_student = len(word_tokenize(student_answer))
    if len_expected == 0 or len_student == 0:
        return 0.0
    return min(len_expected, len_student) / max(len_expected, len_student)

# 9. Relevance - 빈 문자열 처리
def relevance_score(expected_answer, student_answer):
    expected_tokens = set(word_tokenize(expected_answer.lower()))
    if not expected_tokens:
        return 0.0
    student_tokens = set(word_tokenize(student_answer.lower()))
    return len(expected_tokens & student_tokens) / len(expected_tokens)

# 최종 evaluate()
def evaluate(expected, response):
    if expected == response:
        return 10
    elif not response.strip():
        return 0
    
    # 각 지표 점수 계산 (+ 예외 처리)
    metrics = {
        'exact_match': exact_match,
        'partial_match': partial_match,
        'cosine_similarity': cosine_similarity_score,
        'sentiment': lambda e, r: sentiment_analysis(r),
        'sentence_match': enhanced_sentence_match,
        'naive_bayes': multinomial_naive_bayes_score,
        'semantic_similarity': semantic_similarity_score,
        'coherence': coherence_score,
        'relevance': relevance_score
    }
    
    scores = []
    weights = [0.15, 0.1, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1]
    
    for metric_name, metric_func in metrics.items():
        try:
            score = metric_func(expected, response)
            scores.append(max(0, min(1, score)))  # 0~1 범위 보장
        except Exception as e:
            print(f"Error in {metric_name}: {str(e)}")
            scores.append(0.0)
    
    # 가중 평균 계산
    weighted_sum = sum(s * w for s, w in zip(scores, weights))
    total_weight = sum(weights)
    final_score = (weighted_sum / total_weight) * 10  # 0~10점 변환
    return round(final_score)
