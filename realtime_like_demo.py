import os
import time
import subprocess
from pathlib import Path

import sounddevice as sd
import soundfile as sf


FREEVC_DIR = Path("FreeVC")
TEMP_DIR = Path("temp_realtime")
OUTPUT_DIR = Path("output_realtime")

SAMPLE_RATE = 16000
SECONDS = 3

HP_FILE = "logs/freevc.json"
PT_FILE = "checkpoints/freevc.pth"


def record_wav(filename, seconds=3, device=None):
    """Sounddevice를 사용하여 음성 녹음"""
    print(f"\n🎤 녹음 시작: {filename}")
    print(f"   ({seconds}초 동안 말씀해주세요...)")
    
    try:
        audio = sd.rec(
            int(seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=device,
        )
        sd.wait()
        sf.write(filename, audio, SAMPLE_RATE)
        print(f"✓ 녹음 완료: {filename}")
    except Exception as e:
        print(f"❌ 녹음 오류: {e}")
        raise


def make_convert_txt(a_wav, b_wav):
    """청크용 변환 작업 명세 생성"""
    txt_path = FREEVC_DIR / "convert_realtime.txt"

    a_path = "../" + str(a_wav).replace("\\", "/")
    b_path = "../" + str(b_wav).replace("\\", "/")

    lines = [
        f"A_to_B_chunk|{a_path}|{b_path}",
        f"B_to_A_chunk|{b_path}|{a_path}",
    ]

    txt_path.write_text("\n".join(lines), encoding="utf-8")


def run_freevc():
    """FreeVC 변환 실행"""
    cmd = [
        "python",
        "convert.py",
        "--hpfile", HP_FILE,
        "--ptfile", PT_FILE,
        "--txtpath", "convert_realtime.txt",
        "--outdir", "../output_realtime",
    ]

    try:
        subprocess.run(cmd, cwd=FREEVC_DIR, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ FreeVC 변환 오류: {e}")
        raise


def play_wav(path, label=""):
    """변환된 음성 재생"""
    try:
        audio, sr = sf.read(path, dtype="float32")
        print(f"\n🔊 {label} 재생 중...")
        sd.play(audio, sr)
        sd.wait()
        print(f"✓ 재생 완료")
    except Exception as e:
        print(f"❌ 재생 오류: {e}")
        raise


def main():
    """준실시간 양방향 음성 변환 데모"""
    
    # 디렉토리 생성
    TEMP_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("\n" + "=" * 60)
    print("      준실시간 양방향 음성 변환 데모")
    print("=" * 60)
    print(f"📊 설정:")
    print(f"   - 샘플링 레이트: {SAMPLE_RATE} Hz")
    print(f"   - 청크 길이: {SECONDS}초")
    print(f"\n💡 종료하려면 Ctrl+C를 누르세요")
    print("=" * 60)

    iteration = 0
    
    try:
        while True:
            iteration += 1
            print(f"\n\n{'='*60}")
            print(f"[라운드 {iteration}]")
            print(f"{'='*60}")
            
            a_wav = TEMP_DIR / "A_chunk.wav"
            b_wav = TEMP_DIR / "B_chunk.wav"

            # A 화자 녹음
            print("\n[1/4] A 화자 음성 입력")
            record_wav(a_wav, SECONDS)

            # B 화자 녹음
            print("\n[2/4] B 화자 음성 입력")
            record_wav(b_wav, SECONDS)

            # FreeVC 변환 실행
            print("\n[3/4] 음성 변환 중...")
            make_convert_txt(a_wav, b_wav)
            run_freevc()
            print("✓ 변환 완료")

            # 결과 재생
            print("\n[4/4] 변환 결과 재생")
            a_to_b = OUTPUT_DIR / "A_to_B_chunk.wav"
            b_to_a = OUTPUT_DIR / "B_to_A_chunk.wav"

            play_wav(a_to_b, "A 내용 + B 목소리")
            time.sleep(0.5)
            play_wav(b_to_a, "B 내용 + A 목소리")
            
            print("\n✓ 한 라운드 완료!")

    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("프로그램 종료")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        print("\n다음을 확인하세요:")
        print("  1. FreeVC 설치 완료")
        print("  2. 모델 파일 다운로드 완료")
        print("  3. 마이크 연결 확인")


if __name__ == "__main__":
    main()
