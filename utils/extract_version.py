import sys ,os
from PyQt5.QtWidgets import *
import requests
import webbrowser
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import main
# github에 올릴때 버전을 확인하기 위한 코드 + 버전 체크
def update_cheak(self):
    try:
        response = requests.get('https://api.github.com/repos/wlans01/LaserMicroscopeController/releases/latest')
        data = response.json()
        latest_version = data['tag_name']
        current_version = main.CURRENT_VERSION
        print(latest_version, current_version)

        if latest_version > current_version:
            reply = QMessageBox.question(self, '업데이트 확인', 
                                        f'새로운 버전 {latest_version}이(가) 있습니다. 지금 업데이트하시겠습니까?(현재 버전 {current_version})',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                # 윈도우에서 다운로드 url 열기
                ''''''
                download_url = data['html_url']
                webbrowser.open(download_url)
                sys.exit()
                
            else:
                pass

    except:
        pass
        


if __name__ == "__main__":
    CURRENT_VERSION = main.CURRENT_VERSION
    print(CURRENT_VERSION)