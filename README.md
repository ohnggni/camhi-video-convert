이 파일은 Aliexpress에서 판매하는 IP Camera의 CamHi앱에서 ftp로 Alram recording을 실시하는 경우 파일이 확장자265로 저장되어 재생호환성이 떨어지므로 이를 보완하기 위해 mkv로 변환하는 스크립트이다.

#### 0. ftp 서버설치 및 설정
'''Ubuntu 서버에서 FTP 서버를 설치하고 설정하는 방법입니다.
sudo apt update
sudo apt install vsftpd -y
'''
'''vsftpd 설정 파일 열기:
sudo nano /etc/vsftpd.conf
'''
'''다음 내용을 수정 또는 추가:
anonymous_enable=NO              # 익명 접속 금지
local_enable=YES                 # 로컬 사용자 접속 허용
write_enable=YES                 # 파일 업로드 허용
local_umask=022                  # 파일 권한 설정
chroot_local_user=YES            # 사용자 홈 디렉토리를 루트로 고정
allow_writeable_chroot=YES       # chroot 환경에서 쓰기 허용
pasv_enable=YES                  # Passive 모드 활성화
pasv_min_port=40000              # Passive 포트 범위
pasv_max_port=50000
'''
'''설정 저장 후 vsftpd 서비스 재시작:
sudo systemctl restart vsftpd
'''
![IMG_1BC7A6EC3087-1](https://github.com/user-attachments/assets/813d0332-724f-4c75-a533-6ed1e92f155f)

해당 스크립트를 상시 작동하게 하기 위해 다음과 같이 설정한다. (재부팅 후에도 자동실행)

#### 1. 서비스 파일을 생성한다.
'''
nano /etc/systemd/system/convert_script.service
'''
'''
[Unit]
Description=265 to MKV Conversion Script
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/convert_265_to_mkv.py
WorkingDirectory=/home/ohnggni
Restart=always
User=ohnggni

[Install]
WantedBy=multi-user.target
'''
#### 2. 서비스 활성화 및 실행
'''
sudo systemctl daemon-reload
sudo systemctl enable convert_script.service
sudo systemctl start convert_script.service
'''
#### 3. 상태 확인
'''
sudo systemctl status convert_script.service
'''
#### 4. 서비스 재시작 (필요시, 파일 수정 이후 등)
'''
sudo systemctl daemon-reload
sudo systemctl restart convert_script.service
'''
