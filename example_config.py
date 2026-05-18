"""
설정 및 커스터마이징 가이드

이 파일에서 프로젝트의 설정을 커스터마이징할 수 있습니다.
"""

# ========================================
# 1. 경로 설정 (Path Configuration)
# ========================================

from pathlib import Path

# 입출력 경로
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
FREEVC_DIR = Path("FreeVC")

# 음성 파일 경로
SPEAKER_A = INPUT_DIR / "speaker_A.wav"
SPEAKER_B = INPUT_DIR / "speaker_B.wav"

# FreeVC 설정 파일
HP_FILE = "logs/freevc.json"
PT_FILE = "checkpoints/freevc.pth"
WAVLM_FILE = "wavlm/WavLM-Large.pt"


# ========================================
# 2. 오디오 설정 (Audio Configuration)
# ========================================

# 청크 단위 데모 설정
SAMPLE_RATE = 16000  # 샘플링 레이트 (Hz)
CHUNK_SECONDS = 3    # 청크 길이 (초)

# 청크 길이 선택지:
# - 3초: 빠름 (권장 - 실시간 데모용)
# - 5초: 중간
# - 10초: 느리지만 높은 품질


# ========================================
# 3. FreeVC 설정 (FreeVC Configuration)
# ========================================

FREEVC_CONFIG = {
    "convert_script": "convert.py",
    "hpfile": HP_FILE,
    "ptfile": PT_FILE,
    "output_dir": "../output",
    "convert_txt": "convert_project.txt",
}


# ========================================
# 4. 배치 처리 설정 (Batch Processing)
# ========================================

# 한 번에 여러 음성 쌍 변환
# convert_project.txt 파일에 다음과 같이 작성:
"""
# 형식: 작업ID|입력음성|화자참조음성

# 예시:
A_to_B|input/speaker_A.wav|input/speaker_B.wav
B_to_A|input/speaker_B.wav|input/speaker_A.wav

# 추가 예시 (3명 이상):
A_to_C|input/speaker_A.wav|input/speaker_C.wav
A_to_D|input/speaker_A.wav|input/speaker_D.wav
B_to_C|input/speaker_B.wav|input/speaker_C.wav
B_to_D|input/speaker_B.wav|input/speaker_D.wav
C_to_A|input/speaker_C.wav|input/speaker_A.wav
C_to_B|input/speaker_C.wav|input/speaker_B.wav
D_to_A|input/speaker_D.wav|input/speaker_A.wav
D_to_B|input/speaker_D.wav|input/speaker_B.wav
"""


# ========================================
# 5. GPU 설정 (GPU Configuration)
# ========================================

USE_GPU = True  # GPU 사용 여부
GPU_DEVICE = 0  # GPU 장치 번호 (0 = 첫 번째 GPU)

# GPU 메모리 제한 (GB, None = 제한 없음)
GPU_MEMORY_FRACTION = None

# CPU만 사용하려면:
# import torch
# torch.device('cpu')


# ========================================
# 6. 로깅 설정 (Logging Configuration)
# ========================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

LOG_CONFIG = {
    "verbose": True,           # 상세 출력
    "show_progress": True,     # 진행률 표시
    "save_logs": False,        # 로그 파일 저장
    "log_file": "voice_swap.log",
}


# ========================================
# 7. 품질 설정 (Quality Configuration)
# ========================================

QUALITY_PRESETS = {
    "fast": {
        "chunk_seconds": 3,
        "description": "빠른 처리 (권장 - 실시간 데모)",
    },
    "medium": {
        "chunk_seconds": 5,
        "description": "중간 품질",
    },
    "high": {
        "chunk_seconds": 10,
        "description": "높은 품질 (느림)",
    },
}

# 현재 품질 선택
CURRENT_QUALITY = "fast"


# ========================================
# 8. 오류 처리 설정 (Error Handling)
# ========================================

ERROR_HANDLING = {
    "on_missing_file": "raise",    # raise, skip, or create
    "on_gpu_error": "fallback_cpu",  # fallback_cpu or raise
    "on_audio_error": "raise",     # raise or skip
}


# ========================================
# 9. 실험용 설정 (Experimental)
# ========================================

# 음성 감정 전이 (향후 구현)
EMOTION_TRANSFER = False

# 다중 화자 처리 (향후 구현)
MULTI_SPEAKER = False

# 스트리밍 모드 (향후 구현)
STREAMING_MODE = False


# ========================================
# 10. 고급 설정 (Advanced Settings)
# ========================================

ADVANCED_CONFIG = {
    # WavLM 모델 설정
    "wavlm": {
        "model_size": "large",  # large or base
        "use_cache": True,
    },
    
    # HiFi-GAN 디코더 설정
    "decoder": {
        "use_amp": True,  # Automatic Mixed Precision
    },
    
    # 전처리 설정
    "preprocessing": {
        "normalize": True,
        "remove_silence": False,
    },
}


# ========================================
# 사용 예시 (Usage Examples)
# ========================================

if __name__ == "__main__":
    # 예시 1: 기본 설정 확인
    print("=== 기본 설정 ===")
    print(f"입력 폴더: {INPUT_DIR}")
    print(f"출력 폴더: {OUTPUT_DIR}")
    print(f"샘플링 레이트: {SAMPLE_RATE} Hz")
    print(f"청크 길이: {CHUNK_SECONDS}초")
    print(f"GPU 사용: {USE_GPU}")
    
    # 예시 2: 품질 선택
    print(f"\n=== 현재 품질 설정 ===")
    quality_info = QUALITY_PRESETS[CURRENT_QUALITY]
    print(f"설정: {CURRENT_QUALITY}")
    print(f"설명: {quality_info['description']}")
    print(f"청크 길이: {quality_info['chunk_seconds']}초")
    
    # 예시 3: 커스텀 설정
    print("\n=== 커스텀 설정 예시 ===")
    print("""
    # 높은 품질로 변경하려면:
    CHUNK_SECONDS = 10
    
    # GPU 비활성화하려면:
    USE_GPU = False
    
    # 배치 처리를 위해 다음 파일 생성:
    # convert_project.txt에 여러 줄 추가
    """)
