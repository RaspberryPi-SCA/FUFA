import os
import sys
import site
import zipfile

# 1. Python 패키지 경로 가져오기
site_packages_dirs = site.getsitepackages()

# 기본적으로 첫 번째 경로를 사용
target_dir = site_packages_dirs[0]

# 2. 압축된 cusignal 패키지 찾기
zip_filename = "cusignal_package.zip"  # 공유 받은 ZIP 파일명
if not os.path.exists(zip_filename):
    print(f"Error: '{zip_filename}' 파일을 찾을 수 없습니다. ZIP 파일을 동일한 폴더에 두고 실행하세요.")
    sys.exit(1)

# 3. ZIP 압축 해제
print(f"📦 Extracting '{zip_filename}' to {target_dir} ...")
with zipfile.ZipFile(zip_filename, "r") as zip_ref:
    zip_ref.extractall(target_dir)

print("✅ cusignal 설치 완료!")

# 4. 설치 확인 테스트
try:
    import cusignal
    print("🎉 cusignal 설치 확인 성공! 정상적으로 사용 가능합니다.")
except ImportError as e:
    print("❌ Error: cusignal을 import할 수 없습니다.")
    print(f"🔍 Debug Info: {e}")
