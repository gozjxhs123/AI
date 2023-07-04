# 도커 베이스 이미지 선택
FROM python:3.9.16-alpine

# 필요한 파일들을 컨테이너 내부로 복사
COPY requirements.txt requirements.txt
COPY server server
COPY main.py main.py

# pip 업데이트
RUN pip install --upgrade pip

# 필요한 패키지 설치
RUN pip install -r requirements.txt

# 컨테이너 실행시 실행할 명령어
CMD ["python", "main.py"]