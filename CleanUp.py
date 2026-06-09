# 하위 폴더 용량 관리용 코드(/venv, /node_modules 삭제)

import os
import shutil

def delete_target_folders(root_dir, targets=["node_modules", "venv"]):
    print(f"🔍 [{root_dir}] 하위에서 삭제 대상을 탐색합니다...")
    
    found_folders = []
    
    # 1. 삭제할 대상 폴더 탐색
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # 복사본을 만들어 루프를 돌면서 실제 dirnames를 수정 (하위 탐색 최적화)
        for dirname in list(dirnames):
            if dirname in targets:
                full_path = os.path.join(dirpath, dirname)
                found_folders.append(full_path)
                # 삭제할 폴더 안쪽은 더 이상 탐색하지 않도록 제외
                dirnames.remove(dirname)

    if not found_folders:
        print("✨ 삭제할 대상(node_modules, venv)이 없습니다.")
        return

    # 2. 발견된 대상 출력 및 사용자 확인
    print(f"\n⚠️ 총 {len(found_folders)}개의 대상 폴더가 발견되었습니다:")
    for path in found_folders:
        print(f"  - {path}")
        
    confirm = input("\n❗ 위 폴더들을 '실제로' 삭제하시겠습니까? (y/N): ")
    
    if confirm.lower() != 'y':
        print("❌ 삭제가 취소되었습니다.")
        return

    # 3. 실제 삭제 진행
    print("\n🚀 삭제를 시작합니다...")
    success_count = 0
    
    for path in found_folders:
        try:
            print(f"🗑️ 삭제 중: {path} ...", end="", flush=True)
            shutil.rmtree(path)
            print(" 완료!")
            success_count += 1
        except Exception as e:
            print(f" ❌ 실패 (원인: {e})")
            
    print(f"\n✨ 작업 완료! 총 {success_count}개의 폴더를 삭제하여 용량을 확보했습니다.")

if __name__ == "__main__":
    # 스크립트가 실행되는 현재 폴더를 기준으로 탐색합니다.
    current_directory = os.getcwd()
    delete_target_folders(current_directory)