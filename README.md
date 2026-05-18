# Voice Swap Project - 양방향 음성 변환 시스템

## 프로젝트 개요

두 명의 화자가 각각 음성을 녹음하면, 내용은 유지하면서 목소리만 서로 바꾸는 시스템입니다. **FreeVC(Free Voice Conversion)** 모델을 기반으로 하며, Speaker Embedding을 활용한 메타러닝 방식의 음성 변환을 구현합니다.

### 핵심 개념

```
A 음성 입력 ── 내용 추출 ──┐
                          ├─ FreeVC ── A 내용 + B 목소리 출력
B 음성 입력 ── 화자 특징 ──┘

B 음성 입력 ── 내용 추출 ──┐
                          ├─ FreeVC ── B 내용 + A 목소리 출력
A 음성 입력 ── 화자 특징 ──┘
```

### 메타러닝 특징

| 일반 음성 변환 | 이 프로젝트 |
|---|---|
| 특정 화자 데이터를 많이 학습해야 함 | 새로운 화자가 들어와도 짧은 reference 음성으로 speaker embedding 생성 |
| 학습에 오래 걸림 | Unseen speaker에 빠르게 적응하는 few-shot/meta-adaptation 구조 |
| 화자별 모델 필요 | 동일한 모델로 모든 화자 처리 |

**관련 기술:**
- **ECAPA-TDNN** (SpeechBrain): Speaker embedding 추출
- **VoxCeleb**: Pretrained speaker embedding 모델
- **WavLM-Large**: Content 특징 추출

---

## 프로젝트 구조

```
voice_swap_project/
│
├─ FreeVC/                      # GitHub에서 clone한 FreeVC 저장소
│  ├─ checkpoints/
│  │  └─ freevc.pth             # 사전학습된 FreeVC 모델
│  ├─ wavlm/
│  │  └─ WavLM-Large.pt         # WavLM 대형 모델
│  ├─ logs/
│  │  └─ freevc.json            # 하이퍼파라미터 설정
│  ├─ convert.py                # FreeVC 변환 스크립트
│  └─ requirements.txt
│
├─ input/
│  ├─ speaker_A.wav             # 화자 A 음성 파일
│  └─ speaker_B.wav             # 화자 B 음성 파일
│
├─ output/
│  ├─ A_to_B.wav                # A의 내용 + B의 목소리
│  └─ B_to_A.wav                # B의 내용 + A의 목소리
│
├─ temp_realtime/               # 청크 단위 임시 저장소
│  ├─ A_chunk.wav
│  └─ B_chunk.wav
│
├─ output_realtime/             # 청크 변환 결과 저장소
│  ├─ A_to_B_chunk.wav
│  └─ B_to_A_chunk.wav
│
├─ swap_two_voices.py           # 핵심 실행 코드: 두 파일 일괄 변환
├─ realtime_like_demo.py        # 청크 단위 준실시간 데모
└─ README.md
```

---

## 설치 가이드

### 1. 환경 설정

**Windows (Anaconda)**

```bash
# 새로운 conda 환경 생성
conda create -n voice_swap python=3.9 -y
conda activate voice_swap
```

### 2. 필수 패키지 설치

```bash
# PyTorch (CUDA 12.1 버전)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 오디오 처리
pip install librosa soundfile numpy scipy tqdm

# 실시간 녹음 (준실시간 데모 필요)
pip install sounddevice
```

### 3. FreeVC 저장소 Clone

```bash
git clone https://github.com/OlaWod/FreeVC.git
cd FreeVC
pip install -r requirements.txt
cd ..
```

### 4. 사전학습 모델 다운로드

FreeVC는 두 가지 사전학습 모델이 필요합니다:

**a) FreeVC 체크포인트**
- [FreeVC 공식 GitHub](https://github.com/OlaWod/FreeVC)에서 `freevc.pth` 다운로드
- 저장 위치: `FreeVC/checkpoints/freevc.pth`

**b) WavLM-Large 모델**
- [Microsoft WavLM 리포지토리](https://github.com/microsoft/unilm/tree/master/wavlm)에서 다운로드
- 저장 위치: `FreeVC/wavlm/WavLM-Large.pt`

**c) 하이퍼파라미터 설정 파일**
- FreeVC 공식 저장소에서 `freevc.json` 다운로드
- 저장 위치: `FreeVC/logs/freevc.json`

최종 파일 배치:

```
FreeVC/
├─ checkpoints/
│  └─ freevc.pth
├─ wavlm/
│  └─ WavLM-Large.pt
├─ logs/
│  └─ freevc.json
├─ convert.py
└─ requirements.txt
```

### 5. 입력 음성 파일 준비

`input/` 디렉토리에 다음 파일들을 배치합니다:

- **speaker_A.wav**: 화자 A의 음성 (권장: 3~10초)
- **speaker_B.wav**: 화자 B의 음성 (권장: 3~10초)

**음성 파일 요구사항:**
- 포맷: WAV (16kHz 권장, 자동 변환됨)
- 채널: Mono 또는 Stereo
- 길이: 최소 1초 이상

---

## 사용 방법

### 방법 1: 두 음성 파일 일괄 변환

가장 기본적인 사용 방식입니다.

```bash
python swap_two_voices.py
```

**실행 과정:**
1. 필수 파일 확인 (FreeVC, 모델, 입력 음성)
2. `convert_project.txt` 생성 (변환 작업 명세)
3. FreeVC 실행
4. 결과 생성

**출력 파일:**
- `output/A_to_B.wav` - A의 내용 + B의 목소리
- `output/B_to_A.wav` - B의 내용 + A의 목소리

### 방법 2: 청크 단위 준실시간 데모

수업 프레젠테이션에 적합한 양방향 실시간 시뮬레이션입니다.

```bash
python realtime_like_demo.py
```

**동작 방식:**
1. **A 화자 녹음**: 3초 녹음 대기
2. **B 화자 녹음**: 3초 녹음 대기
3. **변환 실행**: FreeVC로 양방향 변환
4. **결과 재생**: 
   - A 내용 + B 목소리 재생
   - B 내용 + A 목소리 재생
5. **반복**: Ctrl+C로 종료할 때까지 반복

**중요:**
- 마이크가 있어야 실행 가능
- `Ctrl+C` 입력으로 종료

---

## 코드 상세 설명

### swap_two_voices.py

```python
FREEVC_DIR = Path("FreeVC")              # FreeVC 저장소 경로
INPUT_DIR = Path("input")                # 입력 음성 파일 경로
OUTPUT_DIR = Path("output")              # 결과 저장 경로

A_WAV = INPUT_DIR / "speaker_A.wav"      # 화자 A 음성
B_WAV = INPUT_DIR / "speaker_B.wav"      # 화자 B 음성

CONVERT_TXT = FREEVC_DIR / "convert_project.txt"  # 변환 작업 명세 파일
```

**주요 함수:**

| 함수 | 역할 |
|---|---|
| `check_files()` | 필수 파일 존재 여부 확인 |
| `make_convert_txt()` | FreeVC 입력 파일 `convert_project.txt` 생성 |
| `run_freevc()` | FreeVC 변환 프로세스 실행 |

**convert_project.txt 형식:**

```
A_to_B|../input/speaker_A.wav|../input/speaker_B.wav
B_to_A|../input/speaker_B.wav|../input/speaker_A.wav
```

형식: `[작업ID]|[입력음성]|[화자참조음성]`

### realtime_like_demo.py

**주요 함수:**

| 함수 | 역할 |
|---|---|
| `record_wav(filename, seconds, device)` | Sounddevice로 음성 녹음 |
| `make_convert_txt(a_wav, b_wav)` | 청크용 변환 작업 명세 생성 |
| `run_freevc()` | FreeVC 변환 실행 |
| `play_wav(path)` | 변환된 음성 재생 |

**변수:**

```python
SAMPLE_RATE = 16000   # 샘플링 레이트 (16kHz)
SECONDS = 3           # 각 청크 녹음 시간 (초)
```

---

## 동작 원리

### FreeVC 모델 구조

```
음성 입력
   ↓
┌─ WavLM-Large ────→ Content 특징 추출
│
├─ Speaker Encoder ─→ Reference 음성에서 Speaker 특징 추출
│
└─ HiFi-GAN Decoder → 새로운 음성 생성 (내용 유지 + 화자 변경)
   ↓
음성 출력
```

### 메타러닝 메커니즘

1. **Content 특징**: WavLM-Large에서 추출한 음성 내용
   - Speaker-invariant representation
   - 화자에 무관한 순수 음성 내용만 추출

2. **Speaker 특징**: Reference 음성에서 추출한 화자 특성
   - Speaker embedding (ECAPA-TDNN 등)
   - VoxCeleb 데이터로 사전학습

3. **빠른 적응**:
   - 새로운 화자가 들어와도 reference 음성 하나로 embedding 생성
   - 추가 학습 없이 즉시 변환 가능
   - Few-shot meta-learning의 특성

---

## 문제 해결

### 문제 1: `FileNotFoundError: 파일이 없습니다`

**원인:** 필수 파일 누락

**해결:**
```bash
# 1. FreeVC 저장소 확인
ls FreeVC/checkpoints/freevc.pth
ls FreeVC/wavlm/WavLM-Large.pt
ls FreeVC/logs/freevc.json

# 2. 입력 파일 확인
ls input/speaker_A.wav
ls input/speaker_B.wav

# 3. 디렉토리 생성
mkdir -p input output temp_realtime output_realtime
```

### 문제 2: CUDA/GPU 오류

**원인:** PyTorch CUDA 버전 불일치

**해결:**
```bash
# CPU로 강제 실행 (느림)
# swap_two_voices.py 수정
import torch
torch.device('cpu')
```

### 문제 3: 음성 품질 저하

**원인:** 입력 음성 품질 저하 또는 너무 짧음

**해결:**
- 입력 음성 길이: 최소 3초 이상
- 조용한 환경에서 녹음
- 명확한 발음 권장

### 문제 4: `sounddevice` 오류 (실시간 데모)

**원인:** 마이크 연결 안 됨 또는 호환성 문제

**해결:**
```bash
# 재설치
pip uninstall sounddevice -y
pip install sounddevice

# 또는 manual device 지정
python realtime_like_demo.py
# 녹음 시 마이크 선택 프롬프트 확인
```

---

## 성능 최적화

### 1. 청크 길이 조정

`realtime_like_demo.py`에서:

```python
SECONDS = 3  # 3초 → 빠름 but 낮은 품질
SECONDS = 5  # 5초 → 중간
SECONDS = 10 # 10초 → 느림 but 높은 품질
```

### 2. 배치 처리

여러 음성을 한 번에 변환:

```python
# convert_project.txt에 여러 줄 추가
pair1|input/A.wav|input/B.wav
pair2|input/C.wav|input/D.wav
pair3|input/E.wav|input/F.wav
```

### 3. GPU 메모리 최적화

```bash
# 메모리 사용량 확인
nvidia-smi

# 배치 크기 조정 (FreeVC convert.py 수정 필요)
```

---

## 확장 기능 아이디어

### 1. 다중 화자 지원

```python
# 3명 이상의 화자 음성 변환
# 모든 쌍(pair)에 대해 변환

speakers = ['A', 'B', 'C', 'D']
for src in speakers:
    for tgt in speakers:
        if src != tgt:
            # src 내용 + tgt 목소리
```

### 2. GUI 인터페이스

```python
import tkinter as tk
from tkinter import filedialog

# 파일 선택 및 실시간 프리뷰
# 변환 진행률 표시
```

### 3. 실시간 스트리밍

```python
# 청크 단위가 아닌 연속 스트리밍
# 오디오 버퍼 활용
```

### 4. 감정 전이

```python
# 음성 감정 분석 → 감정도 함께 변환
# Emotion-aware speaker embedding
```

---

## 참고 자료

### 주요 논문
- **FreeVC**: FreeVC: Zero-shot Voice Style Conversion with Only Autoencoder Loss
  - GitHub: https://github.com/OlaWod/FreeVC
  
- **WavLM**: WavLM: Large-Scale Self-Supervised Pre-training for Speech
  - GitHub: https://github.com/microsoft/unilm/tree/master/wavlm

- **Speaker Embedding**: ECAPA-TDNN (SpeechBrain)
  - GitHub: https://github.com/speechbrain/speechbrain

### 관련 프로젝트
- **SpeechBrain**: Speech Processing Toolkit (https://speechbrain.github.io/)
- **Librosa**: Audio Analysis Library (https://librosa.org/)

---

## 라이선스 및 기여

이 프로젝트는 FreeVC(오픈소스)를 기반으로 합니다.

**주요 의존성:**
- FreeVC: MIT License
- PyTorch: BSD License
- Librosa: ISC License

---

## 저자

**프로젝트**: Voice Swap Project - 양방향 음성 변환  
**작성**: Meiblue2  
**저장소**: https://github.com/Meiblue2/ai

---

## 수정 이력

| 날짜 | 내용 |
|---|---|
| 2026-05-18 | 초기 문서 작성 |

