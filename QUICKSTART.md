# Quick Start - 5분 안에 시작하기 ⚡

> 이 가이드를 따라하면 **5분 안에** 음성 변환을 시작할 수 있습니다!

---

## 📋 요구사항

- **Python 3.9+** (설치 여부 확인: `python --version`)
- **Anaconda** (또는 pip)
- **GPU 권장** (CPU로도 가능, 느림)

---

## 🚀 5분 설치

### 1️⃣ 프로젝트 받기 (30초)

```bash
git clone https://github.com/Meiblue2/ai.git
cd ai
```

### 2️⃣ 환경 설정 (1분)

```bash
# Anaconda 환경 생성
conda create -n voice_swap python=3.9 -y
conda activate voice_swap
```

### 3️⃣ 패키지 설치 (2분)

```bash
# PyTorch 설치 (GPU 버전)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 기타 패키지
pip install -r requirements.txt
```

### 4️⃣ FreeVC 설치 (1분)

```bash
git clone https://github.com/OlaWod/FreeVC.git
cd FreeVC
pip install -r requirements.txt
cd ..
```

### 5️⃣ 모델 다운로드 (⏰ 중요!)

다음 3개 파일을 다운로드하세요:

| 파일 | 저장 위치 | 크기 |
|---|---|---|
| `freevc.pth` | `FreeVC/checkpoints/` | ~300MB |
| `WavLM-Large.pt` | `FreeVC/wavlm/` | ~800MB |
| `freevc.json` | `FreeVC/logs/` | ~1KB |

**다운로드 링크:**
- [FreeVC 공식 저장소](https://github.com/OlaWod/FreeVC) → README 참고
- [WavLM 공식 저장소](https://github.com/microsoft/unilm/tree/master/wavlm) → README 참고

---

## 📁 폴더 구조 확인

```
ai/
├─ FreeVC/
│  ├─ checkpoints/
│  │  └─ freevc.pth          ← 다운로드한 모델
│  ├─ wavlm/
│  │  └─ WavLM-Large.pt      ← 다운로드한 모델
│  ├─ logs/
│  │  └─ freevc.json         ← 다운로드한 설정
│  └─ convert.py
│
├─ input/
│  ├─ speaker_A.wav          ← 음성 파일 1
│  └─ speaker_B.wav          ← 음성 파일 2
│
└─ output/
   ├─ A_to_B.wav             ← 결과 (생성됨)
   └─ B_to_A.wav             ← 결과 (생성됨)
```

---

## 🎤 음성 파일 준비

`input/` 폴더에 음성 파일 2개를 넣으세요:

- **speaker_A.wav** - 화자 A의 음성 (3~10초)
- **speaker_B.wav** - 화자 B의 음성 (3~10초)

**팁:** 마이크로 녹음하거나 YouTube에서 다운로드 가능

---

## ▶️ 실행!

### 방법 1: 파일 변환 (가장 간단)

```bash
python swap_two_voices.py
```

**출력:**
```
✓ output/A_to_B.wav 생성 (A 내용 + B 목소리)
✓ output/B_to_A.wav 생성 (B 내용 + A 목소리)
```

### 방법 2: 실시간 데모 (선택)

```bash
python realtime_like_demo.py

# 3초씩 녹음 → 변환 → 재생 반복
# Ctrl+C로 종료
```

---

## 🎉 완료!

**축하합니다!** 이제 음성 변환이 작동합니다!

### 다음 단계

- 📖 **README.md** - 프로젝트 전체 설명
- 🖥️ **setup_guide.md** - 문제 해결
- 🔧 **example_config.py** - 설정 커스터마이징

---

## 🚨 문제 해결

### ❌ "FileNotFoundError"

```bash
# 1. 필수 파일 확인
ls FreeVC/checkpoints/freevc.pth
ls FreeVC/wavlm/WavLM-Large.pt
ls FreeVC/logs/freevc.json
ls input/speaker_A.wav
ls input/speaker_B.wav

# 2. 없으면 다운로드 (setup_guide.md 참고)
```

### ❌ "No module named"

```bash
# 환경 활성화 확인
conda activate voice_swap

# 패키지 재설치
pip install -r requirements.txt
```

### ❌ CUDA 오류

```bash
# CPU로 실행 (느리지만 항상 작동)
# swap_two_voices.py에 추가:
import torch
torch.device('cpu')
```

**더 많은 문제?** → **setup_guide.md** 참고

---

**행운을 빕니다! 🚀**

