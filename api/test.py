import pymysql

try:
    connection = pymysql.connect(
        host='your-host',
        user='your-user',
        password='your-password',
        database='your-db',
        port=3306
    )
    print("DB 연결 성공!")
    connection.close()
except Exception as e:
    print(f"연결 실패: {e}")
    print(f"에러 타입: {type(e)}")
