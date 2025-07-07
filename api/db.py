from sqlalchemy import create_engine, MetaData
from databases import Database

# 연결 정보는 config 파일에서 가져오는 게 깔끔하지만, 테스트용으로 직접 입력도 가능
DATABASE_URL = "mysql+pymysql://cybershock:tjtj!!0714@cybershock.mycafe24.com:3306/cybershock"

# 비동기 데이터베이스 연결 객체
database = Database(DATABASE_URL)

# SQLAlchemy용 메타데이터 (테이블 정의 등 관리용)
metadata = MetaData()

# SQLAlchemy용 동기 엔진 (마이그레이션이나 DB 작업용)
engine = create_engine("mysql+pymysql://cybershock:tjtj!!0714@cybershock.mycafe24.com:3306/cybershock")