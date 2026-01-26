### 🍀 실습용 테이블 및  데이터 생성

```sql
-- 사원 정보 테이블
CREATE TABLE personal (
    pno INT PRIMARY KEY,         -- 사원번호
    pname VARCHAR(50),           -- 이름
    dno INT,                     -- 부서번호
    manager INT                  -- 상사
    pay DECIMAL(10,2),           -- 급여
    job VARCHAR(50),             -- 직무
    hire_date DATE               -- 입사일
);

-- 부서 정보 테이블
CREATE TABLE division (
    dno INT PRIMARY KEY,        -- 부서번호
    dname VARCHAR(50),          -- 부서명
    position VARCHAR(50)        -- 위치
);

-- personal 테이블 데이터
INSERT INTO personal VALUES
(101, 'Alice', 10, 107, 5000, 'Manager', '2020-01-15'),
(102, 'Bob', 20, 101, 4500, 'Developer', '2019-05-20'),
(103, 'Charlie', 10, 101, 4000, 'Designer', '2021-03-10'),
(104, 'David', 30, Null, 3500, 'Sales', '2022-07-01'),
(105, 'Eve', 20, 102, 4200, 'Developer', '2020-11-30'),
(106, 'Frank', 10, 103, 3800, 'Designer', '2023-02-15'),
(107, 'Grace', 40, Null, 4800, 'Manager', '2018-09-05'),
(108, 'Hank', NULL, Null, 3200, 'Intern', '2023-06-01');  -- 부서 없음

-- division 테이블 데이터
INSERT INTO division VALUES
(10, 'HR', 'Seoul'),
(20, 'IT', 'Incheon'),
(30, 'Sales', 'Busan'),
(40, 'Marketing', 'Jeju');
(50, 'Clerk', 'Daegu');  -- 사원 없음
```

## 1. 테이블 조인 (Table Joins)

### **(1)** Cartesian Product (테두리 곱)

두 테이블을 결합할 때 조인 조건(ON, WHERE 등)을 지정하지 않아, 첫 번째 테이블의 모든 행과 두 번째 테이블의 모든 행이 무조건 하나씩 다 결합되는 현상을 말합니다.

```sql
SELECT pname, division.dname FROM personal, division;
```

> **결과**: 모든 사원 & 모든 부서의 조합 (비효율적)
> 

---

### (2) 내부 조인 (Inner Join)

**교집합**과 같습니다. 두 테이블 모두에서 **조인 조건이 일치하는 행**만 결과로 가져옵니다.

- **특징:** 어느 한쪽이라도 매칭되는 값이 없으면 그 데이터는 결과에서 제외됩니다.

```sql
-- WHERE 절 사용
SELECT
    p.pname,
    d.dname,
    p.dno AS 'p-dno',
    d.dno AS 'd-dno'
FROM
    personal p, division d
WHERE
    p.dno = d.dno;

-- JOIN ON 구문 사용
SELECT
    p.pname, d.dname, p.dno, d.dno
FROM
    personal p
JOIN
    division d
ON
    p.dno = d.dno;
```

---

### (3) 외부 조인 (Outer Join)

**합집합** 성격을 가집니다. 조건이 일치하지 않더라도 **한쪽 테이블의 모든 데이터를 보존**하고 싶을 때 사용합니다. 매칭되는 값이 없는 부분은 `NULL`로 채워집니다.

### **① Left Outer Join (가장 많이 사용)**

- **의미:** 왼쪽(먼저 쓴) 테이블의 모든 데이터를 가져오고, 오른쪽 테이블에서 일치하는 것을 붙입니다.
- **결과:** 오른쪽 테이블에 매칭되는 값이 없으면 `NULL`로 표시됩니다.
- **용도:** 모든 사원 명단을 출력하되, 부서가 없는 사원도 포함하고 싶을 때사용합니다.

```sql
-- LEFT JOIN (personal 테이블 모두 출력)
SELECT
    p.pname, p.dno, p.pay, d.dname
FROM
    personal p
LEFT OUTER JOIN
    division d
ON
    p.dno = d.dno;
```

### **② Right Outer Join**

- **의미:** 오른쪽 테이블의 모든 데이터를 보존합니다.
- **용도:** 모든 부서 목록을 출력하되, 소속된 사원이 없는 부서도 포함하고 싶을 때 사용합니다.

```sql
-- RIGHT JOIN (division 테이블 모두 출력)
SELECT
    p.pname, d.dno, p.pay, d.dname
FROM
    personal p
RIGHT OUTER JOIN
    division d
ON
    p.dno = d.dno;
```

**요약 비교**

| **구분** | **Inner Join** | **Outer Join (Left)** |
| --- | --- | --- |
| **핵심 개념** | 일치하는 데이터만 (교집합) | 한쪽은 무조건 다 (보존) |
| **일치하지 않는 값** | 버림 (삭제) | NULL로 표시하며 유지 |
| **사용 목적** | 정확한 연결 관계 확인 | 누락된 데이터 확인 및 전체 목록 추출 |

**Tip:** 실무에서는 `Inner Join`과 `Left Outer Join`이 90% 이상 사용됩니다.

---

### (4) 셀프 조인 (Self Join)

이름 그대로 **하나의 테이블을 자기 자신과 조인하는 것을 말합니다**. SQL에 `SELF JOIN`이라는 별도의 명령어는 없으며, 일반적인 `INNER JOIN`이나 `LEFT JOIN`을 사용하되 **같은 테이블을 두 번 불러와서** 결합하는 방식입니다.

```sql
-- manager-pno 관계 조회
SELECT
    p.pno, p.pname, p.manager, m.pname AS manager_name
FROM
    personal p
JOIN
    personal m
ON
    p.manager = m.pno;
```

---

## 2. 서브쿼리 (Subquery)

**서브쿼리(Subquery)**란 **하나의 SQL 문장 안에 포함된 또 다른 SELECT 문**을 말합니다. 쉽게 말해 '쿼리 속의 쿼리'이며, 바깥쪽의 메인 쿼리를 도와주는 보조 역할을 수행합니다. 

### (1) 단일행 서브쿼리

- 실습 1: 최대 급여 받는 사원 조회

```sql
-- 최대 급여 확인
SELECT MAX(pay) FROM personal;

-- 최대 급여를 받는 사원 조회
SELECT pname, pay
FROM personal
WHERE pay = (SELECT MAX(pay) FROM personal);
```

---

- 실습 2: 특정 조건 서브쿼리

```sql
-- 평균 급여보다 많이 받는 사람
SELECT pname, pay
FROM personal
WHERE pay > (SELECT AVG(pay) FROM personal);

-- 최소 급여 받는 사람
SELECT pname, pay
FROM personal
WHERE pay = (SELECT MIN(pay) FROM personal);

-- 인천에서 근무하는 사람
SELECT p.pname, d.position
FROM personal p
JOIN division d ON p.dno = d.dno
WHERE d.position = 'Incheon';
```

---

### (2) 다중행 서브쿼리

- 실습 3: IN, ALL, ANY 활용

```sql
-- [1] 급여가 가장 적은 사람
SELECT pname, pay
FROM personal
WHERE pay = (SELECT MIN(pay) FROM personal);

-- [3] 평균 급여보다 높은 급여 받는 사람
SELECT pname, pay
FROM personal
WHERE pay > ALL (
    SELECT AVG(pay)
    FROM personal
    GROUP BY dno
);

-- [4] 부서 평균급여가 가장 적은 부서보다 적게 받는 사람
SELECT pname, pay
FROM personal p
WHERE pay  **결과**: 조건에 맞는 사원 목록 출력

---

#### 실습 4: EXISTS vs IN
```sql
-- EXISTS 사용 (존재 여부 확인)
SELECT pname
FROM personal p
WHERE EXISTS (
    SELECT 1
    FROM division d
    WHERE d.dno = p.dno AND d.position = 'Incheon'
);

-- IN 사용 (결과값 비교)
SELECT pname
FROM personal
WHERE dno IN (
    SELECT dno
    FROM division
    WHERE position = 'Incheon'
);

```

> 결과: 두 방법 모두 동일한 결과 (Incheon 근무자)
> 

---

### 2.3 다중컬럼 서브쿼리

### 실습 5: 다중 컬럼 조건

```sql
-- [6] 각 부서 평균 급여 중 최고 평균 급여 부서 조회
SELECT dno, AVG(pay) AS avg_pay
FROM personal
GROUP BY dno
HAVING AVG(pay) >= ALL (
    SELECT AVG(pay)
    FROM personal
    GROUP BY dno
);

-- 부서 평균 급여보다 높은 급여 받는 사람
SELECT p1.pname, p1.dno, p1.pay
FROM personal p1
WHERE p1.pay > (
    SELECT AVG(p2.pay)
    FROM personal p2
    WHERE p1.dno = p2.dno
);

```

> 결과: 최고 평균 급여 부서와 해당 조건을 만족하는 사원
> 

---

## 3. MySQL 외래키 실습

```sql
-- 외래키 포함 테이블 생성
CREATE TABLE dept (
    dept_no INT PRIMARY KEY,
    dname VARCHAR(50)
) ENGINE=InnoDB;

CREATE TABLE emp (
    emp_no INT PRIMARY KEY,
    dept_no INT,
    emp_name VARCHAR(50),
    FOREIGN KEY (dept_no) REFERENCES dept(dept_no)
) ENGINE=InnoDB;

-- 데이터 삽입 테스트
INSERT INTO dept VALUES (10, 'HR'), (20, 'IT');
INSERT INTO emp VALUES (1, 10, 'John'), (2, 20, 'Jane');

-- 외래키 제약 위반 시도
INSERT INTO emp VALUES (3, 30, 'Doe'); -- 오류 발생 (dept_no 30 없음)

```

> 결과: 외래키 제약으로 인해 삽입 실패
> 

---

## 4. 종합 실습 문제

### 문제 1:

**조건**:

- "martin"과 같은 직무를 가진 사원 조회 (martin 제외)
- 인천에서 근무하는 사원 중 급여가 평균 이상인 사람 조회

**해결**:

```sql
-- [2] martin과 같은 직무 (martin 제외)
SELECT pname
FROM personal
WHERE job = (SELECT job FROM personal WHERE pname = 'martin')
AND pname != 'martin';

-- 인천 근무자 중 급여 평균 이상
SELECT pname, pay
FROM personal p
JOIN division d ON p.dno = d.dno
WHERE d.position = 'Incheon'
AND pay >= (SELECT AVG(pay) FROM personal WHERE dno = p.dno);

```

---

## 5. 정답 및 해설

### 서브쿼리 연습문제

1. **급여가 가장 적은 사람**:
    
    ```sql
    SELECT pname, pay
    FROM personal
    WHERE pay = (SELECT MIN(pay) FROM personal);
    
    ```
    
2. **입사일이 가장 빠른 사람**:
    
    ```sql
    SELECT pname, hire_date
    FROM personal
    WHERE hire_date = (SELECT MIN(hire_date) FROM personal);
    
    ```
    
3. **부서 평균 급여보다 높은 급여 받는 사람**:
    
    ```sql
    SELECT p1.pname, p1.dno, p1.pay
    FROM personal p1
    WHERE p1.pay > (
        SELECT AVG(p2.pay)
        FROM personal p2
        WHERE p1.dno = p2.dno
    );
    
    ```
    
4. **부서 평균급여가 가장 적은 부서보다 적게 받는 사람**:
    
    ```sql
    SELECT pname, pay
    FROM personal
    WHERE pay  (
        SELECT AVG(p2.pay)
        FROM personal p2
        WHERE p1.dno = p2.dno
    );
    
    ```
    
5. **각 부서 평균 급여 중 최고 평균 급여 부서**:
    
    ```sql
    SELECT dno, AVG(pay) AS avg_pay
    FROM personal
    GROUP BY dno
    HAVING AVG(pay) = (
        SELECT MAX(avg_pay)
        FROM (
            SELECT AVG(pay) AS avg_pay
            FROM personal
            GROUP BY dno
        ) AS dept_avg
    );
    
    ```
    

---

## 6. 추가 팁

- **서브쿼리 최적화**: `EXISTS`는 존재 여부만 확인하므로 `IN`보다 성능이 우수
- **JOIN vs 서브쿼리**: 복잡한 조건에서는 JOIN이 더 직관적일 수 있음
- **데이터베이스 종속성**: 외래키 문법은 MySQL, PostgreSQL, SQL Server에서 차이 있음