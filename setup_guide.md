# Windows 상세 설치 가이드 🖥️

> 이 가이드는 Windows 환경에서의 설치를 단계별로 설명합니다.

---

## 📋 전체 과정

```
1️⃣  Python/Anaconda 설치
2️⃣  프로젝트 받기
3️⃣  가상 환경 생성
4️⃣  패키지 설치
5️⃣  FreeVC 설치
6️⃣  모델 파일 다운로드
7️⃣  음성 파일 준비
8️⃣  실행 테스트
```

---

## 1️⃣ Python & Anaconda 설치

### Python 설치 (이미 설치되어 있다면 건너뛰기)

1. **Python 공식 사이트** 방문: https://www.python.org/downloads/
2. **Python 3.11** 또는 **3.12** 다운로드
3. 설치 시 **"Add Python to PATH"** 체크 ✓

### Anaconda 설치

1. **Anaconda 공식 사이트** 방문: https://www.anaconda.com/download
2. **Windows 64-bit** 버전 다운로드
3. 설치 진행 (기본 설정 OK)

### 확인

```bash
# Anaconda Prompt 또는 PowerShell 실행

python --version
# Python 3.9 이상 확인

conda --version
# Anaconda 버전 확인
```

---

## 2️⃣ 프로젝트 받기

### 방법 1: Git Clone (권장)

```bash
# 원하는 폴더에서 실행
git clone https://github.com/Meiblue2/ai.git
cd ai
```

### 방법 2: ZIP 다운로드

1. https://github.com/Meiblue2/ai 방문
2. **Code** > **Download ZIP** 클릭
3. 압축 해제

---

## 3️⃣ 가상 환경 생성

```bash
# 프로젝트 폴더에서 실행

# Anaconda Prompt 또는 PowerShell에서
conda create -n voice_swap python=3.9 -y

# 환경 활성화
conda activate voice_swap
```

**확인:**
```bash
(voice_swap) C:\path\to\project>  # 왼쪽에 (voice_swap) 표시됨
```

---

## 4️⃣ 패키지 설치

### PyTorch 설치 (GPU 버전)

```bash
# CUDA 12.1 버전 (NVIDIA GPU가 있는 경우)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**또는 CPU 버전 (GPU가 없는 경우)**

```bash
pip install torch torchvision torchaudio
```

### 기타 패키지 설치

```bash
pip install librosa soundfile numpy scipy tqdm sounddevice
```

**또는 requirements.txt 사용:**

```bash
pip install -r requirements.txt
```

---

## 5️⃣ FreeVC 설치

### FreeVC 저장소 Clone

```bash
# 프로젝트 폴더에서 실행
git clone https://github.com/OlaWod/FreeVC.git
cd FreeVC
```

### FreeVC 의존성 설치

```bash
# FreeVC 폴더에서 실행
pip install -r requirements.txt
```

### 폴더 구조 확인

```
프로젝트/
├─ FreeVC/
│  ├─ checkpoints/
│  ├─ wavlm/
│  ├─ logs/
│  ├─ convert.py
│  └─ requirements.txt
```

---

## 6️⃣ 모델 파일 다운로드

### 필요한 파일 3개

| 파일 | 저장 위치 | 크기 | 출처 |
|---|---|---|---|
| **freevc.pth** | `FreeVC/checkpoints/` | ~300MB | [FreeVC GitHub](https://github.com/OlaWod/FreeVC) |
| **WavLM-Large.pt** | `FreeVC/wavlm/` | ~800MB | [WavLM GitHub](https://github.com/microsoft/unilm/tree/master/wavlm) |
| **freevc.json** | `FreeVC/logs/` | ~1KB | FreeVC 저장소 |

### 다운로드 단계별

#### A) FreeVC 체크포인트

1. [FreeVC 공식 GitHub](https://github.com/OlaWod/FreeVC) 방문
2. **README.md** 에서 모델 다운로드 링크 찾기
3. **freevc.pth** 다운로드
4. `FreeVC/checkpoints/` 폴더에 저장

```
FreeVC/
├─ checkpoints/
│  └─ freevc.pth  ← 여기 저장
```

#### B) WavLM-Large 모델

1. [Microsoft WavLM GitHub](https://github.com/microsoft/unilm/tree/master/wavlm) 방문
2. **README** 의 "Pre-trained Models" 찾기
3. **WavLM-Large** 다운로드
4. `FreeVC/wavlm/` 폴더에 저장

```
FreeVC/
├─ wavlm/
│  └─ WavLM-Large.pt  ← 여기 저장
```

#### C) freevc.json

1. FreeVC 저장소에서 찾기 (보통 `configs/` 또는 `logs/` 폴더)
2. 또는 FreeVC README 참고
3. `FreeVC/logs/` 폴더에 저장

```
FreeVC/
├─ logs/
│  └─ freevc.json  ← 여기 저장
```

### 확인 스크립트

```bash
# 프로젝트 폴더에서 실행
python -c "
import os
from pathlib import Path

paths = [
    'FreeVC/checkpoints/freevc.pth',
    'FreeVC/wavlm/WavLM-Large.pt',
    'FreeVC/logs/freevc.json',
]

for p in paths:
    if os.path.exists(p):
        size = os.path.getsize(p) / (1024**2)
        print(f'✓ {p} ({size:.1f}MB)')
    else:
        print(f'✗ {p} (없음)')
"
```

---

## 7️⃣ 음성 파일 준비

### 입력 폴더 구조

```
프로젝트/
├─ input/
│  ├─ speaker_A.wav   ← 화자 A 음성
│  └─ speaker_B.wav   ← 화자 B 음성
```

### 음성 파일 요구사항

| 항목 | 요구사항 |
|---|---|
| 포맷 | WAV, MP3, OGG 등 (자동 변환) |
| 길이 | 최소 1초, 권장 3~10초 |
| 샘플링 레이트 | 16kHz 권장 (자동 변환) |
| 채널 | Mono 또는 Stereo |
| 품질 | 조용한 환경에서 명확한 발음 |

### 음성 파일 얻기

#### 방법 1: 마이크로 녹음 (Windows)

```bash
# 내장 녹음 앱 실행
# 시작 > "음성 녹음" 또는 "Voice Recorder"

# 3~10초 정도 녹음
# 저장 위치: input/ 폴더
```

#### 방법 2: YouTube/Podcast에서 다운로드

```bash
# 예: yt-dlp 사용
pip install yt-dlp

# 동영상 다운로드
yt-dlp -x --audio-format wav "URL" -o "input/speaker_A.wav"
```

#### 방법 3: 온라인 음성 변환

- Google Speech to Text → WAV 변환
- 또는 다른 TTS 서비스 사용

---

## 8️⃣ 실행 테스트

### 테스트 1: 기본 변환

```bash
# 프로젝트 폴더에서 (voice_swap 환경 활성화)
python swap_two_voices.py
```

**예상 출력:**
```
==================================================
   양방향 음성 변환 시스템
==================================================
✓ 출력 디렉토리 생성: output

1. 필수 파일 확인 중...
✓ 모든 필수 파일 확인 완료

2. 변환 작업 명세 생성 중...
✓ convert_project.txt 생성

3. FreeVC 모델 실행 중...
[진행 중...]

==================================================
✓ 변환 완료!
==================================================
✓ output/A_to_B.wav 생성 (A 내용 + B 목소리)
✓ output/B_to_A.wav 생성 (B 내용 + A 목소리)
==================================================
```

**결과 확인:**
```bash
ls output/
# A_to_B.wav
# B_to_A.wav
```

### 테스트 2: 실시간 데모 (선택)

```bash
# 마이크가 있는 경우
python realtime_like_demo.py

# 3초씩 녹음 → 변환 → 재생 반복
# Ctrl+C로 종료
```

---

## 🚨 일반 오류 및 해결

### 1. "FileNotFoundError: 파일을 찾을 수 없습니다"

**원인:** 필수 파일 누락

**해결:**
```bash
# 1. 파일 위치 다시 확인
ls FreeVC/checkpoints/freevc.pth
ls FreeVC/wavlm/WavLM-Large.pt
ls FreeVC/logs/freevc.json
ls input/speaker_A.wav
ls input/speaker_B.wav

# 2. 폴더 생성
mkdir input output temp_realtime output_realtime

# 3. 다시 시도
python swap_two_voices.py
```

### 2. "No module named 'librosa'"

**원인:** 패키지 설치 안 됨

**해결:**
```bash
# 환경 활성화 확인
conda activate voice_swap

# 패키지 재설치
pip install librosa soundfile numpy scipy tqdm
```

### 3. CUDA/GPU 오류

**오류 메시지:** "CUDA out of memory" 또는 "CUDA not available"

**해결:**
```bash
# CPU 강제 사용 (느리지만 항상 작동)
# swap_two_voices.py 상단에 추가:
import torch
torch.device('cpu')
```

### 4. "sounddevice" 오류 (실시간 데모)

**원인:** 마이크 연결 안 됨 또는 드라이버 문제

**해결:**
```bash
# 1. 마이크 확인
# Windows 설정 > 사운드 > 입력 장치

# 2. sounddevice 재설치
pip uninstall sounddevice -y
pip install sounddevice

# 3. 다시 시도
python realtime_like_demo.py
```

### 5. "permission denied" 또는 "access denied"

**원인:** 관리자 권한 필요

**해결:**
```bash
# PowerShell을 관리자로 실행한 후 다시 시도
```

---

## 📊 성능 최적화

### GPU 확인

```bash
python -c "import torch; print(torch.cuda.is_available())"
# True 출력 = GPU 사용 가능
# False 출력 = CPU만 사용
```

### GPU 사용 메모리 확인

```bash
# NVIDIA GPU의 경우
nvidia-smi

# 메모리 사용량 확인
```

### 속도 개선 팁

| 조건 | 추천 |
|---|---|
| GPU 있음 | PyTorch GPU 버전 사용 ✓ |
| 메모리 부족 | `CHUNK_SECONDS = 3` 사용 |
| 높은 품질 필요 | `CHUNK_SECONDS = 10` 사용 |

---

## 📚 다음 단계

1. **README.md** 읽기 - 프로젝트 전체 이해
2. **QUICKSTART.md** 확인 - 빠른 시작
3. **example_config.py** 수정 - 설정 커스터마이징
4. **코드 분석** - Python 코드 이해

---

## 💬 추가 도움

- **FreeVC 문제**: https://github.com/OlaWod/FreeVC/issues
- **PyTorch 문제**: https://pytorch.org/get-started/locally/
- **GitHub Issues**: https://github.com/Meiblue2/ai/issues

---

✅ **설치 완료! 이제 사용을 시작할 수 있습니다!**
