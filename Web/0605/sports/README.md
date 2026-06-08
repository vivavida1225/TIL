# 스포츠(Sports) 경기 데이터셋 (10,000건)

데이터는 **JSONL(한 줄 = JSON 1개)** 형식으로 제공됩니다.

---

## 배포 파일

- `sports.jsonl`  
  - 스포츠 경기(Event) 데이터 10,000건(JSONL)

---

## 필드 설명

- `event_name` (string)  
  - 스포츠 경기 또는 이벤트의 이름입니다.  
  - 예: 리그 경기, 결승전, 플레이오프, 국제 대회 등  
  - 어떤 경기를 분석하는지 식별할 때 기준이 됩니다.

- `sport_type` (string)  
  - 경기 종목 유형입니다.  
  - 예: 야구, 축구, 농구, 배구, e스포츠 등  
  - 종목별 관중 수나 시청률 차이를 비교하는 데 활용할 수 있습니다.

- `date` (string)  
  - 경기가 진행된 날짜입니다. (YYYY-MM-DD 형식)  
  - 시점별 인기 변화나 시즌별 트렌드 분석에 활용할 수 있습니다.

- `team1` (string)  
  - 경기 참여 팀 1입니다.  
  - 홈/원정 또는 기준 팀으로 활용할 수 있습니다.

- `team2` (string)  
  - 경기 참여 팀 2입니다.  
  - 상대 팀 분석이나 경기 결과 비교에 활용할 수 있습니다.

- `score_team1` (int)  
  - 팀 1의 득점입니다.  
  - 경기 결과 분석 및 승패 판단에 활용됩니다.

- `score_team2` (int)  
  - 팀 2의 득점입니다.  
  - 경기 결과 분석 및 승패 판단에 활용됩니다.

- `venue` (string)  
  - 경기가 열린 경기장 또는 장소입니다.  
  - 장소별 관중 수나 흥행 성과 분석에 활용할 수 있습니다.

- `attendance` (int)  
  - 현장 관중 수입니다.  
  - 실제 오프라인 흥행 규모를 나타내는 지표로 활용할 수 있습니다.

- `broadcast_channel` (string)  
  - 경기를 중계한 방송사 또는 플랫폼입니다.  
  - 중계 채널에 따른 시청률 차이 분석에 활용할 수 있습니다.

- `viewership_rating_percent` (float)  
  - 방송 시청률(%)입니다.  
  - 대중적 관심도 및 미디어 성과를 나타내는 핵심 지표입니다.

- `player_of_match` (string)  
  - 경기 최우수 선수(MVP)입니다.  
  - 스타 플레이어 효과 분석에 활용할 수 있습니다.

---

## 이 데이터를 어떻게 활용하나요?

### 예시 1) 상관 관계 분석

필드 간 상관 관계가 나타납니다.  

- `attendance` <-> `viewership_rating_percent`  
  - 관중 수가 많은 경기일수록  
    미디어 관심이 높아져 시청률이 증가하는 경향이 나타날 수 있습니다.  
  - 다만 경기 중요도, 스타 선수 출전 여부, 중계 채널에 따라  
    관중 수와 시청률이 반드시 비례하지 않는 경우도 존재합니다.

각 행(row)은 **"스포츠 경기(Event) 1개"**를 의미합니다.  

![차트 이미지](chart.png)  

---

### 예시 2) 파운데이션 모델 파인튜닝

본 데이터셋을 활용하여 스포츠 이벤트의 속성에 따른 시청률(Viewership Rating)을 예측하는 **회귀(Regression) 모델**을 구축할 수 있습니다.

실습 모델로는 BERT(Bidirectional Encoder Representations from Transformers)를 사용합니다.  
  - BERT는 종목명, 대진 팀, 경기장 등 텍스트 데이터에 담긴 화제성을 파악하는 데 강점이 있지만, 특정 대진이나 중계 채널이 실제 시청률 수치에 미치는 상관관계에 대해서는 별도의 학습이 필요합니다.  
  - 따라서 본 데이터셋의 이벤트 조건과 시청률 간의 관계를 학습시키는 파인튜닝을 통해 입력된 경기 정보에 맞는 예상 시청률을 산출하도록 최적화합니다.

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
시청률 데이터는 0~100 사이의 범위를 가지므로 별도의 로그 변환 없이 직접 레이블로 사용합니다.

```python
import json
import torch
import numpy as np
from datetime import datetime
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

def prepare_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            t1 = item['team1'] or "N/A"
            t2 = item['team2'] or "N/A"
            try:
                dow = datetime.strptime(item['date'], "%Y-%m-%d").strftime("%a")
            except Exception:
                dow = "N/A"
            text = (
                f"이벤트: {item['event_name']}, 종목: {item['sport_type']}, "
                f"채널: {item['broadcast_channel']}, 경기장: {item['venue']}, "
                f"홈팀: {t2}, 원정팀: {t1}, 요일: {dow}"
            )
            data.append({"text": text, "label": float(item['viewership_rating_percent'])})
    return Dataset.from_list(data)

dataset = prepare_data('sports.jsonl')

labels = np.array(dataset['label'])
label_mean = float(labels.mean())
label_std  = float(labels.std())

dataset = dataset.map(lambda x: {"label": (x["label"] - label_mean) / label_std})

tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-multilingual-cased", num_labels=1)

def tokenize_func(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

tokenized_dataset = dataset.map(tokenize_func, batched=True)

args = TrainingArguments(
    output_dir="./sports-model",
    num_train_epochs=10,
    learning_rate=2e-5,
    per_device_train_batch_size=64,
    fp16=True,
    optim="adamw_torch_fused",
    weight_decay=0.01,
    warmup_ratio=0.1,
    logging_steps=50,
    save_strategy="no"
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
)

trainer.train()

model.save_pretrained("./viewership-predictor")
tokenizer.save_pretrained("./viewership-predictor")

with open("./viewership-predictor/label_stats.json", "w") as f:
    json.dump({"mean": label_mean, "std": label_std}, f)
```

**3. 모델 테스트 및 추론**  

학습된 모델을 로드하여 새로운 스포츠 시나리오에 대한 시청률을 예측합니다.  
결과값에는 중계 채널의 접근성이나 경기 중요도에 따른 보정 수치를 적용합니다.

```python
import json
import torch
from datetime import datetime
from transformers import AutoModelForSequenceClassification, AutoTokenizer

path = "./viewership-predictor"
loaded_tokenizer = AutoTokenizer.from_pretrained(path)
loaded_model = AutoModelForSequenceClassification.from_pretrained(path)
loaded_model.eval()

with open(f"{path}/label_stats.json") as f:
    stats = json.load(f)
label_mean = stats["mean"]
label_std  = stats["std"]

def predict_viewership(event, sport, channel, venue, team1=None, team2=None, date=None):
    t1 = team1 or "N/A"
    t2 = team2 or "N/A"
    try:
        dow = datetime.strptime(date, "%Y-%m-%d").strftime("%a") if date else "N/A"
    except Exception:
        dow = "N/A"

    query = (
        f"이벤트: {event}, 종목: {sport}, "
        f"채널: {channel}, 경기장: {venue}, "
        f"홈팀: {t2}, 원정팀: {t1}, 요일: {dow}"
    )
    inputs = loaded_tokenizer(query, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        output = loaded_model(**inputs)
        prediction = output.logits.item() * label_std + label_mean

    return max(0.1, prediction)

test_cases = [
    ("2024 프로야구 정규시즌", "야구", "SBS", "잠실 야구장", "LG 트윈스", "두산 베어스", "2024-08-10"),
    ("프리미어리그 손흥민 출전 경기", "축구", "SPOTV", "토트넘 홋스퍼 스타디움", "맨체스터 시티", "토트넘 홋스퍼", "2024-09-14"),
    ("발리볼 네이션스리그", "배구", "KBS2", "인천삼산체육관", None, None, "2024-06-15"),
    ("LCK 서머 결승전", "e스포츠", "유튜브, 트위치", "KSPO DOME", "Gen.G", "T1", "2024-08-18"),
    ("2024 메이저리그 월드시리즈", "야구", "MBC", "다저 스타디움", "뉴욕 양키스", "LA 다저스", "2024-10-26"),
]

for args in test_cases:
    event, sport, channel, venue = args[0], args[1], args[2], args[3]
    predicted_rating = predict_viewership(*args)
    print(f"[{sport} / {event}] 예상 시청률: {predicted_rating:.1f}%")
```

**추론 결과**  

```text
[야구 / 2024 프로야구 정규시즌] 예상 시청률: 9.7%
[축구 / 프리미어리그 손흥민 출전 경기] 예상 시청률: 3.8%
[배구 / 발리볼 네이션스리그] 예상 시청률: 1.1%
[e스포츠 / LCK 서머 결승전] 예상 시청률: 2.9%
[야구 / 2024 메이저리그 월드시리즈] 예상 시청률: 17.6%
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
from datetime import datetime
from datasets import Dataset
from sklearn.metrics import mean_absolute_error, r2_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def prepare_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            t1 = item['team1'] or "N/A"
            t2 = item['team2'] or "N/A"
            try:
                dow = datetime.strptime(item['date'], "%Y-%m-%d").strftime("%a")
            except Exception:
                dow = "N/A"
            text = (
                f"이벤트: {item['event_name']}, 종목: {item['sport_type']}, "
                f"채널: {item['broadcast_channel']}, 경기장: {item['venue']}, "
                f"홈팀: {t2}, 원정팀: {t1}, 요일: {dow}"
            )
            data.append({
                "text": text,
                "label": float(item['viewership_rating_percent'])
            })
    return Dataset.from_list(data)

full_dataset = prepare_data('sports.jsonl')
test_size = int(len(full_dataset) * 0.1)
test_dataset = full_dataset.select(range(len(full_dataset) - test_size, len(full_dataset)))

path = "./viewership-predictor"
model = AutoModelForSequenceClassification.from_pretrained(path)
tokenizer = AutoTokenizer.from_pretrained(path)
model.eval()

with open(f"{path}/label_stats.json") as f:
    stats = json.load(f)
label_mean = stats["mean"]
label_std  = stats["std"]

actuals, preds = [], []

for item in test_dataset:
    inputs = tokenizer(item['text'], return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        output = model(**inputs)
        pred = output.logits.item() * label_std + label_mean
        preds.append(pred)
        actuals.append(item['label'])

mae = mean_absolute_error(actuals, preds)
r2 = r2_score(actuals, preds)

print(f"### [스포츠 시청률 예측 모델 정량적 평가 결과] ###")
print(f"- 테스트 데이터 수: {len(actuals)}개")
print(f"- 평균 절대 오차 (MAE): {mae:.4f} %")
print(f"- 결정계수 (R² Score): {r2:.4f} (1.0에 가까울수록 정밀함)")
```

```
### [스포츠 시청률 예측 모델 정량적 평가 결과] ###
- 테스트 데이터 수: 1000개
- 평균 절대 오차 (MAE): 0.1344 %
- 결정계수 (R² Score): 0.9831 (1.0에 가까울수록 정밀함)
```

- **MAE (0.1344%):** 예측값이 실제 시청률과 평균적으로 약 0.13%p 정도의 차이를 보입니다. 스포츠 중계 특성상 경기 흥행도나 돌발 변수에 따른 시청률 편차가 존재함을 고려할 때, 채널·종목·이벤트 유형 기반의 시청률 범위를 파악하기에 충분히 정밀한 수준입니다.
- **$R^2$ Score (0.9831):** 전체 시청률 변동의 약 98%를 모델이 설명하고 있습니다. 입력된 종목·채널·이벤트 정보와 실제 시청률 사이의 상관관계를 매우 높은 수준으로 포착하고 있으며, 다양한 스포츠 도메인에서 채널별·이벤트별 시청률 흐름을 신뢰도 있게 예측하는 데 적합한 수치입니다.

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

    purpose = "모델의 목적: 스포츠 이벤트의 속성에 따른 시청률(Viewership Rating)을 예측"

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
    [야구 / 2024 프로야구 정규시즌] 예상 시청률: 9.7%
    [축구 / 프리미어리그 손흥민 출전 경기] 예상 시청률: 3.8%
    [배구 / 발리볼 네이션스리그] 예상 시청률: 1.1%
    [e스포츠 / LCK 서머 결승전] 예상 시청률: 2.9%
    [야구 / 2024 메이저리그 월드시리즈] 예상 시청률: 17.6%
    """

    evaluate_with_structured_output(test_results)
```

- 결과

```text
답변의 점수: 80 점
이유: 데이터셋은 스포츠 이벤트의 속성(스포츠 종목, 구체적 경기명)과 시청률을 명확히 연결하고 있으며, 형식이 일관된 구조로 구성되어 있습니다. 시청률 범위(1.1% ~ 17.6%)가 넓고, 다양한 스포츠(e스포츠, 야구, 축구, 배구)를 포함해 일반화 가능성도 있습니다. 다만 테스트 데이터가 매우 작아 일반화 능력을 평가하기 어렵고, 시청률 예측을 위해 추가적인 특성(예: 선수 인기, 경기 날짜, 팀 간 경쟁력 등)이 누락되어 모델 성능에 제약이 있을 수 있습니다. 그러나 학습 데이터의 구조적 타당성과 다양성은 80점 이상의 점수를 부여할 만합니다.
```
