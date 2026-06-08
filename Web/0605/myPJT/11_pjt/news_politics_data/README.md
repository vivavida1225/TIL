# 뉴스/정치 관련 데이터셋 (10,000건)

데이터는 **JSONL(한 줄 = JSON 1개)** 형식으로 제공됩니다.

---

## 배포 파일

- `news_politics.jsonl`  
  - 뉴스 및 정치 관련 기사 데이터 10,000건(JSONL)

---

## 필드 설명

- `article_topic` (string)
    - 보도된 뉴스 기사의 핵심 주제 또는 헤드라인입니다.
    - 정치, 경제, 스포츠 등 사회 전반의 주요 사건사고를 식별하는 기준이 됩니다.
- `category` (string)
    - 뉴스 기사가 속한 보도 분야입니다.
    - 예: 정치, 경제/부동산, 경제/금융, 스포츠, 국방/외교 등
- `view_count` (int)
    - 해당 기사가 대중에게 노출되어 발생한 총 조회수입니다.
    - 기사의 화제성과 대중적 관심을 측정하는 직접적인 지표입니다.
- `shares` (int)
    - SNS나 커뮤니티 등으로 기사가 공유된 횟수입니다.
    - 정보의 확산 속도와 독자의 능동적인 반응 정도를 나타냅니다.
- `comments_count` (int)
    - 기사에 달린 댓글의 총 개수입니다.
    - 해당 주제에 대해 독자들이 얼마나 활발하게 의견을 교환했는지 보여주는 참여도 지표입니다.
- `sentiment_score` (float)
    - 기사의 내용 및 댓글 반응을 분석하여 산출한 감성 점수입니다.
    - -1.0(매우 부정)에서 1.0(매우 긍정) 사이의 값을 가지며, 해당 이슈에 대한 여론의 향방을 수치로 나타냅니다.

---

## 이 데이터를 어떻게 활용하나요?

### 예시 1) 상관 관계 분석
기사 데이터의 `sentiment_score`와 `view_count` 필드 간의 관계를 분석한 결과입니다. 각 행(row)은 **뉴스 또는 정치 기사 1건**을 나타냅니다.

---

#### 1. 시각화 개요 (Matplotlib)
* **X축**: `sentiment_score` (기사 감성 점수)
* **Y축**: `view_count` (조회 수, 로그 스케일 적용)

---

#### 2. 사분면별 결과 해석

| 영역 | 특징 | 주요 사례 및 해석 |
| :--- | :--- | :--- |
| **우상단** (오른쪽-위) | **긍정 감성 & 높은 조회 수** | 희망적 메시지, 성과 보도, 공감 유도형 스토리. 긍정적 감성이 독자의 호응을 얻어 높은 조회 수로 이어진 사례. |
| **좌상단** (왼쪽-위) | **부정 감성 & 높은 조회 수** | 사회적 논란, 정치적 갈등, 비판적 이슈. 자극적인 내용이 감정적 반응을 유발하여 클릭과 공유가 활발히 발생한 사례. |
| **우하단** (오른쪽-아래) | **긍정 감성 & 낮은 조회 수** | 소규모 뉴스, 특정 집단 타겟 기사. 감성은 긍정적이나 이슈의 파급력이 낮아 조회 수가 제한된 사례. |
| **좌하단** (왼쪽-아래) | **부정 감성 & 낮은 조회 수** | 저관심 비판 기사, 반복된 이슈의 후속 보도. 부정적 내용임에도 사회적 주목을 받지 못한 사례. |

---

#### 3. 종합 결론
조회 수를 로그 스케일로 변환하여 분석한 결과, 감성 점수의 높고 낮음과 관계없이 조회 수가 다양하게 분포되어 있습니다.

* **감성 점수 단독**으로는 조회 수를 완전히 설명하기 어렵습니다.
* 중립적인 기사라도 **사회적 이슈나 선거 시기**에는 높은 조회 수를 기록할 수 있습니다.
* 실제 조회 수는 기사 주제, **시의성, 사회적 맥락** 등 복합적인 요소에 의해 결정됩니다.

![chart.png](./chart.png)  

---

### 예시 2) 파운데이션 모델 파인튜닝

본 데이터셋을 활용하여 뉴스 기사의 주제와 카테고리에 따른 예상 **조회수(View Count)**를 예측하는 **회귀(Regression) 모델**을 구축할 수 있습니다.

실습 모델로는 **BERT(Bidirectional Encoder Representations from Transformers)**를 사용합니다.  
* BERT는 사전 학습 과정에서 언어의 문맥적 구조를 파악하고 있지만, 특정 기사 주제나 카테고리가 대중의 반응(조회수)에 미치는 수치적 영향은 학습되지 않은 상태입니다.  
* 따라서 본 데이터셋의 기사 정보와 실제 조회수 간의 상관관계를 학습시키는 파인튜닝을 통해, 입력된 텍스트 조건에 맞는 예상 조회수를 산출하도록 모델을 최적화합니다.

---

**1. 가상환경 생성 및 패키지 설치**  
```bash
python3.11 -m venv ./venv
. ./venv/bin/activate

# PyTorch 및 관련 라이브러리 설치
pip install torch==2.9.1 torchvision==0.24.1 torchaudio==2.9.1 --index-url https://download.pytorch.org/whl/cu128

# 데이터 처리 및 학습 가속화 도구 설치
pip install datasets==4.8.4 accelerate==1.13.0 transformers==5.4.0
```

**2. 데이터 전처리 및 학습**  
JSONL 데이터를 모델 학습에 적합한 형태로 변환합니다.  
조회수는 값의 편차가 크고 항상 양수이므로, 학습의 안정성을 위해 **로그 변환(Log Transformation)**을 적용하여 레이블로 사용합니다.

```py
import json
import torch
import numpy as np
from datasets import Dataset
from transformers import (
    DataCollatorWithPadding, 
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    TrainingArguments, 
    Trainer,
    EarlyStoppingCallback
)

# 1) 데이터 전처리 및 분리
def prepare_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            # [SEP] 토큰을 사용하여 카테고리와 주제 간의 관계를 BERT가 더 잘 파악하게 함
            text = f"카테고리: {item['category']} [SEP] 주제: {item['article_topic']}"
            label = np.log1p(float(item['view_count']))
            data.append({"text": text, "label": label})
    
    full_dataset = Dataset.from_list(data)
    # 80/20 비율로 학습/검증 데이터 분리
    return full_dataset.train_test_split(test_size=0.2, seed=42)

split_dataset = prepare_data('news_politics.jsonl')

# 2) 토크나이저 및 모델 로드
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=1)

def tokenize_func(examples):
    return tokenizer(examples["text"], truncation=True, max_length=128)

tokenized_dataset = split_dataset.map(tokenize_func, batched=True, remove_columns=["text"])
data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

# 3) 학습 파라미터 최적화
args = TrainingArguments(
    output_dir="./news-view-model",
    eval_strategy="steps",
    save_strategy="steps",
    eval_steps=100,
    save_steps=100,
    num_train_epochs=10,              # 모델이 충분히 수렴할 수 있도록 에포크 상향
    learning_rate=3e-5,               # 회귀 문제를 위해 소폭 상향
    per_device_train_batch_size=16,   # 더 세밀한 업데이트를 위해 배치 사이즈 하향
    per_device_eval_batch_size=16,
    fp16=True,
    optim="adamw_torch_fused",
    weight_decay=0.01,
    logging_steps=20,
    load_best_model_at_end=True,
    metric_for_best_model="loss",
    save_total_limit=2,
)

# 4) Trainer 실행 (Early Stopping 적용)
trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    data_collator=data_collator,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=5)] # 인내심 상향
)

trainer.train()

# 모델 저장
model.save_pretrained("./news-view-predictor")
tokenizer.save_pretrained("./news-view-predictor")
```

**3. 모델 테스트 및 추론**  
학습된 모델을 로드하여 새로운 뉴스 시나리오에 대한 예상 조회수를 예측합니다.  
로그 변환된 결과값을 다시 **지수 함수(`exp`)**를 통해 실제 조회수 단위로 복원합니다.

```py
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def predict():
    model_path = "./news-view-predictor"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()

    # 현실적인 변별력을 확인하기 위한 5개 테스트 케이스
    test_cases = [
        {"article_topic": "K-POP 그룹, 빌보드 차트 1위 석권", "category": "연예/음악"},
        {"article_topic": "정부, 차세대 AI 반도체 육성 전략 발표", "category": "IT/과학"},
        {"article_topic": "북한, 동해상으로 미확인 발사체 발사", "category": "국방/외교"},
        {"article_topic": "내일 전국 맑고 일교차 큰 완연한 가을", "category": "사회/날씨"},
        {"article_topic": "코스피, 기관 매수세에 강보합 마감", "category": "경제/금융"}
    ]

    print(f"{'입력 주제':<35} | {'예상 조회수'}")
    print("-" * 60)

    for case in test_cases:
        # 학습 시와 동일한 포맷 사용
        text = f"카테고리: {case['category']} [SEP] 주제: {case['article_topic']}"
        
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
        
        with torch.no_grad():
            outputs = model(**inputs)
            # 로그 스케일 복원: exp(x) - 1
            prediction = outputs.logits.item()
            actual_view_estimate = int(np.expm1(prediction))
            
            print(f"{case['article_topic'][:33]:<35} | {actual_view_estimate:,} 회")

if __name__ == "__main__":
    predict()
```

**추론 결과**
```text
입력 주제                               | 예상 조회수
------------------------------------------------------------
K-POP 그룹, 빌보드 차트 1위 석권              | 5,455,242 회
정부, 차세대 AI 반도체 육성 전략 발표             | 2,000,044 회
북한, 동해상으로 미확인 발사체 발사                | 5,407,506 회
내일 전국 맑고 일교차 큰 완연한 가을               | 3,112,616 회
코스피, 기관 매수세에 강보합 마감                 | 918,391 회
```

#### 모델 추론 결과 평가

학습된 모델의 신뢰성을 확보하기 위해 미학습 데이터(Test Set)를 활용한 정량적 평가와 대형 언어 모델(LLM)을 활용한 정성적 평가를 병행합니다.

##### 1. 정량적 성능 지표 분석 (Quantitative Evaluation)

전체 데이터의 10%(1,000건)를 검증용으로 분리하여 모델이 얼마나 정확하게 예측하는지 수치로 산출합니다. 회귀 모델의 특성을 고려하여 **MAE(평균 절대 오차)**와 **R² Score(결정계수)**를 주요 지표로 활용합니다.  

```bash
pip install scikit-learn==1.8.0
```

```python
import json
import numpy as np
import torch
from datasets import Dataset
from sklearn.metrics import mean_absolute_error, r2_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# 1) 데이터 전처리 함수 정의 (훈련 시 사용한 포맷 및 분리 방식 동일 적용)
def prepare_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip(): continue
            item = json.loads(line)
            text = f"카테고리: {item['category']} [SEP] 주제: {item['article_topic']}"
            data.append({"text": text, "label": np.log1p(float(item['view_count']))})

    full_dataset = Dataset.from_list(data)
    return full_dataset.train_test_split(test_size=0.2, seed=42)

# 2) 테스트 데이터 준비 (훈련과 동일한 seed=42 기준 20% 분리)
split_dataset = prepare_data('news_politics.jsonl')
test_dataset = split_dataset["test"]

# 3) 모델 로드 및 추론
path = "./news-view-predictor"
model = AutoModelForSequenceClassification.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained(path)
model.eval()

actuals, preds = [], []

for item in test_dataset:
    inputs = tokenizer(item['text'], return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        output = model(**inputs)
        preds.append(np.expm1(output.logits.item()))
        actuals.append(np.expm1(item['label']))

# 4) 지표 산출
mae = mean_absolute_error(actuals, preds)
r2 = r2_score(actuals, preds)

print(f"### [뉴스 기사 조회수 예측 모델 정량적 평가 결과] ###")
print(f"- 테스트 데이터 수: {len(actuals)}개")
print(f"- 평균 절대 오차 (MAE): {mae:,.0f} 회")
print(f"- 결정계수 (R² Score): {r2:.4f} (1.0에 가까울수록 정밀함)")
```

```
### [뉴스 기사 조회수 예측 모델 정량적 평가 결과] ###
- 테스트 데이터 수: 2000개
- 평균 절대 오차 (MAE): 590,429 회
- 결정계수 (R² Score): 0.7768 (1.0에 가까울수록 정밀함)
```

- **MAE (590,429회):** 예측값이 실제 기사 조회수와 평균적으로 약 59만 회 정도의 차이를 보입니다. 뉴스 기사의 특성상 속보성 이슈, 포털 메인 노출 여부, 공유 확산 등 예측 불가한 외부 변수에 따라 조회수가 폭발적으로 증가하는 경우가 빈번함을 고려할 때 전반적인 기사 파급력을 가늠하기에 참고 가능한 수준입니다.
- **$R^2$ Score (0.7768):** 전체 조회수 변동의 약 78%를 모델이 설명하고 있습니다. 카테고리와 기사 주제만을 입력으로 활용했음에도 실제 조회수와 유의미한 상관관계를 포착하고 있으며, 조회수 분포가 극단적으로 편향된 뉴스 도메인의 특성을 감안할 때 양호한 예측력을 나타내는 수치입니다.

##### 2. LLM-as-a-Judge를 활용한 정성적 평가 (Qualitative Evaluation)

수치적 지표 외에, 대형 언어 모델인 **Qwen3 (14B)**를 평가자로 활용하여 모델의 추론 결과가 도메인의 상식에 부합하는지 검토합니다. LangChain의 structured_output을 사용하여 평가의 객관성을 유지합니다.  

- Ollama 설치

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

- 모델 다운로드

```bash
ollama pull qwen3:14b
```

- 가상환경 생성 및 패키지 설치

```bash
python -m venv ./venv
. ./venv/bin/activate
pip install langchain==1.2.15 langchain-ollama==1.1.0
```

- 평가 코드 실행

Pydantic을 사용하여 평가 점수(score)와 상세 사유(reason)를 객체 형태로 반환하도록 설계했습니다.  

```python
from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama


class EvaluationResult(BaseModel):
    score: int = Field(description="0에서 100 사이의 평가 점수")
    reason: str = Field(description="해당 점수가 도출된 상세한 이유")


def evaluate_with_structured_output(data_list):
    llm = ChatOllama(
        model="qwen3:14b",
        temperature=0.7,
    )

    structured_llm = llm.with_structured_output(EvaluationResult)

    base_system_message = (
        "당신은 AI 모델의 학습 데이터셋을 검토하는 전문가입니다. "
        "제공된 데이터셋은 교육 목적의 가상 데이터이며, 현실과는 차이가 있을 수 있습니다. "
        "언어 모델 파인튜닝이라는 학습의 목적에 맞다면, 엄격함을 낮추고 점수를 중간 이상(70점 이상)으로 주십시오. "
        "특히, 여러 개 결과가 한 구간에 수렴하지 않는지 경향성을 분석해서 점수를 주십시오. "
        "1만개 데이터셋을 학습했으며, 테스트는 그 중 5번 이하의 결과입니다. "
    )

    purpose = "모델의 목적: 뉴스 기사의 주제와 카테고리에 따른 예상 **조회수(View Count)**를 예측"

    system_message = base_system_message + purpose

    result = structured_llm.invoke(
        [
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": f"데이터:\n{data_list}",
            },
        ]
    )

    print(f"답변의 점수: {result.score} 점")
    print(f"이유: {result.reason}")


if __name__ == "__main__":
    test_results = """
    입력 주제                               | 예상 조회수
    ------------------------------------------------------------
    K-POP 그룹, 빌보드 차트 1위 석권              | 5,455,242 회
    정부, 차세대 AI 반도체 육성 전략 발표             | 2,000,044 회
    북한, 동해상으로 미확인 발사체 발사                | 5,407,506 회
    내일 전국 맑고 일교차 큰 완연한 가을               | 3,112,616 회
    코스피, 기관 매수세에 강보합 마감                 | 918,391 회
    """

    evaluate_with_structured_output(test_results)
```

- 결과

```text
답변의 점수: 75 점
이유: 데이터셋은 뉴스 주제와 조회수 예측을 위한 학습에 적합한 구조를 보입니다. K-POP, 정책, 국제사건, 날씨, 금융 등 다양한 주제가 포함되어 있어 카테고리별 조회수 패턴을 학습할 수 있는 기반이 됩니다. 조회수 범위(918,391 ~ 5,455,242)도 현실적인 분포를 반영하고 있으며, 특정 주제에 대한 조회수 예측 모델의 학습에 유리합니다. 다만, 1만개 데이터셋 중 5개만 테스트로 사용하는 설정은 일반적인 교차검증의 범위를 벗어나며, 데이터 분포의 경향성 분석에 제약이 있을 수 있습니다. 70점 이상의 중간 수준 점수를 부여합니다.
```
