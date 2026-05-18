import os
import subprocess
from pathlib import Path

FREEVC_DIR = Path("FreeVC")
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

A_WAV = INPUT_DIR / "speaker_A.wav"
B_WAV = INPUT_DIR / "speaker_B.wav"

CONVERT_TXT = FREEVC_DIR / "convert_project.txt"

HP_FILE = "logs/freevc.json"
PT_FILE = "checkpoints/freevc.pth"
OUT_DIR = "../output"


def check_files():
    """필수 파일 존재 여부 확인"""
    required = [
        FREEVC_DIR / "convert.py",
        FREEVC_DIR / HP_FILE,
        FREEVC_DIR / PT_FILE,
        A_WAV,
        B_WAV,
    ]

    for path in required:
        if not path.exists():
            raise FileNotFoundError(f"파일이 없습니다: {path}")


def make_convert_txt():
    """FreeVC 입력 파일 convert_project.txt 생성"""
    a_path = "../" + str(A_WAV).replace("\\", "/")
    b_path = "../" + str(B_WAV).replace("\\", "/")

    lines = [
        f"A_to_B|{a_path}|{b_path}",
        f"B_to_A|{b_path}|{a_path}",
    ]

    CONVERT_TXT.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ convert_project.txt 생성")


def run_freevc():
    """FreeVC 변환 프로세스 실행"""
    cmd = [
        "python",
        "convert.py",
        "--hpfile", HP_FILE,
        "--ptfile", PT_FILE,
        "--txtpath", "convert_project.txt",
        "--outdir", OUT_DIR,
    ]

    print("FreeVC 실행 중...")
    subprocess.run(cmd, cwd=FREEVC_DIR, check=True)


if __name__ == "__main__":
    try:
        print("=" * 50)
        print("   양방향 음성 변환 시스템")
        print("=" * 50)
        
        # 출력 디렉토리 생성
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"✓ 출력 디렉토리 생성: {OUTPUT_DIR}")
        
        # 필수 파일 확인
        print("\n1. 필수 파일 확인 중...")
        check_files()
        print("✓ 모든 필수 파일 확인 완료")
        
        # convert_project.txt 생성
        print("\n2. 변환 작업 명세 생성 중...")
        make_convert_txt()
        
        # FreeVC 실행
        print("\n3. FreeVC 모델 실행 중...")
        run_freevc()
        
        # 완료
        print("\n" + "=" * 50)
        print("✓ 변환 완료!")
        print("=" * 50)
        print(f"✓ output/A_to_B.wav 생성 (A 내용 + B 목소리)")
        print(f"✓ output/B_to_A.wav 생성 (B 내용 + A 목소리)")
        print("=" * 50)
        
    except FileNotFoundError as e:
        print(f"\n❌ 오류: {e}")
        print("\n필요한 파일을 확인하세요:")
        print(f"  - FreeVC/convert.py")
        print(f"  - FreeVC/logs/freevc.json")
        print(f"  - FreeVC/checkpoints/freevc.pth")
        print(f"  - input/speaker_A.wav")
        print(f"  - input/speaker_B.wav")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ FreeVC 실행 오류: {e}")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
