# MySQL : TCL(Transaction Control Language)

## 1. 트랜잭션 제어 (Transaction Control)

### 실습 환경 준비

```sql
-- 데이터베이스 및 테이블 생성
CREATE DATABASE comstudy_db;
USE comstudy_db;

-- 테스트 테이블 생성
CREATE TABLE account (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    balance DECIMAL(10,2)
);

-- 데이터 삽입
INSERT INTO account VALUES
(1, 'Alice', 100000),
(2, 'Bob', 50000),
(3, 'Eve', 55000),
(4, 'Grace', 78000);
```

### 트랜잭션:

여러 SQL 작업을 하나의 논리적 단위로 묶어 데이터 일관성을 유지하는 기술입니다.

- `COMMIT`: 변경 사항을 데이터베이스에 영구 저장합니다.
- `ROLLBACK`: 작업을 취소하고 이전 상태로 되돌립니다

```sql
-- 트랜잭션 시작 (MySQL은 DML 실행 시 자동 시작)
UPDATE account SET balance = balance - 10000 WHERE id = 1;
UPDATE account SET balance = balance + 10000 WHERE id = 2;

-- 성공 시 커밋
COMMIT;

-- 실패 시 롤백
-- ROLLBACK;
```

### 자동 커밋 확인

```sql
-- 현재 자동 커밋 상태 확인
SELECT @@autocommit;

-- 자동 커밋 비활성화
SET autocommit = 0;

-- DML 실행 후 자동 커밋 테스트
UPDATE account SET balance = 90000 WHERE id = 1;

-- MySQL은 정상 종료 시 자동 커밋 발생
EXIT;
```

---

## 2. 사용자 관리

### 2.1 새 계정 생성

```sql
-- 계정 생성 및 권한 부여
CREATE USER 'comstudy'@'localhost' IDENTIFIED BY 'comstudy';
GRANT ALL PRIVILEGES ON comstudy_db.* TO 'comstudy'@'localhost';
FLUSH PRIVILEGES;
```

### 2.2 계정 접속 테스트

```bash
# 터미널에서 실행
mysql -ucomstudy -pcomstudy
```

### 2.3 사용자 테이블 수정 (MySQL 8.0+)

```sql
USE mysql;
INSERT INTO user (
    host, user, authentication_string
) VALUES (
    'localhost', 'comstudy', '1111'
);
FLUSH PRIVILEGES;
```

---

## 3. 비밀번호 변경 방법

### 1️⃣ ALTER USER (MySQL 8.0+ 권장)

```sql
ALTER USER 'comstudy'@'localhost'
IDENTIFIED WITH mysql_native_password
BY '1234';
FLUSH PRIVILEGES;
```

### 2️⃣ mysqladmin (터미널)

```bash
mysqladmin -ucomstudy -pcomstudy password '1234'
```

---

## 4. 백업 및 복구

### 4.1 테이블 단위 백업/복구

```sql
-- 테이블 백업
SELECT * INTO OUTFILE '/tmp/account_backup.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
FROM account;

-- 테이블 초기화
TRUNCATE TABLE account;

-- 백업 복구
LOAD DATA INFILE '/tmp/account_backup.csv'
INTO TABLE account
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;
```

### 4.2 데이터베이스 전체 백업/복구

```bash
# 백업
mysqldump -u root -p comstudy > /tmp/comstudy_db_backup.sql

# 복구
mysql -u root -p comstudy < /tmp/comstudy_db_backup.sql
```

---

## 5. 데이터베이스 생성 및 사용자 연결

### 5.1 데이터베이스 생성

```sql
CREATE DATABASE javadb;
```

### 5.2 사용자 권한 부여 (MySQL 8.0+ 권장)

```sql
CREATE USER 'park'@'localhost' IDENTIFIED BY 'park';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP
ON javadb.* TO 'park'@'localhost';
FLUSH PRIVILEGES;
```

### 5.3 사용자 테이블 직접 수정 (레거시 방식)

```sql
USE mysql;
INSERT INTO db (
    host, db, user, select_priv, insert_priv,
    update_priv, delete_priv, create_priv, drop_priv
) VALUES (
    '%', 'javadb', 'park', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'
);
FLUSH PRIVILEGES;
```

---

## 6. 주요 정보 조회 명령어

```sql
-- 테이블 구조 확인
DESCRIBE account;

-- 인덱스 정보
SHOW INDEX FROM account;

-- MySQL 상태 정보
SHOW STATUS;

-- MySQL 변수
SHOW VARIABLES;

-- 사용자 정보
SELECT * FROM mysql.user WHERE User='comstudy';
```

---

## 7. 실습 결과 예시

### 성공 사례

```sql
-- 계정 생성 성공
Query OK, 0 rows affected (0.01 sec)

-- 트랜잭션 커밋 성공
Query OK, 0 rows affected (0.00 sec)

-- 백업 파일 생성 성공
/tmp/account_backup.csv 파일 생성됨
```

### 실패 사례

```sql
-- 잘못된 비밀번호 변경 시도
ERROR 1348 (HY000): Column 'password' is deprecated and replacement
'table.authentication_string' for column 'password' doesn't have a default value

-- 해결 방법: MySQL 8.0+에서는 ALTER USER 사용 권장
```

---

## 8. **보안 및 최적화 팁**

1. **최소 권한 원칙**:
    
    ```sql
    GRANT SELECT, INSERT ON comstudy_db.account TO 'comstudy'@'localhost';
    ```
    
2. **자동 커밋 비활성화**:
    
    ```sql
    SET autocommit = 0;
    ```
    
    - 트랜잭션 제어를 더 세밀하게 관리 가능.
3. **백업 경로 설정**:
    - `LOAD DATA INFILE` 사용 시 MySQL 서버 접근 가능한 경로 지정.