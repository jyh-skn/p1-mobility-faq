<h1>SKN26-1st-3Team</h1>

---

<h2>👋🏻 팀 소개</h2>
<h3>📌 **Team 차곡차곡**</h3>

<table align="center">
  <tr>
    <td align="center" width="160px"><img src="./images/Leonardo.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="160px"><img src="./images/Bluebear.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="160px"><img src="./images/Katie.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="160px"><img src="./images/Tom Nook.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="160px"><img src="./images/Dotty.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
    <td align="center" width="160px"><img src="./images/lsabelle.png" width="100" style="object-fit: contain; aspect-ratio: 1/1;"></td>
  </tr>
  <tr>
    <td align="center"><b>이창우</b></td>
    <td align="center"><b>김지윤</b></td>
    <td align="center"><b>박기은</b></td>
    <td align="center"><b>박은지</b></td>
    <td align="center"><b>윤정연</b></td>
    <td align="center"><b>홍지윤</b></td>
  </tr>
  <tr>
    <td align="center">PM</td>
    <td align="center">FRONT</td>
    <td align="center">FRONT</td>
    <td align="center">DB/BACK</td>
    <td align="center">FRONT</td>
    <td align="center">DB/BACK</td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Gloveman"><img src="https://img.shields.io/badge/Gloveman-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/JiyounKim-EllyKim"><img src="https://img.shields.io/badge/JiyounKim-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/gieun-Park"><img src="https://img.shields.io/badge/gieun--Park-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/lo1f0306"><img src="https://img.shields.io/badge/lo1f0306-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/dimolto3"><img src="https://img.shields.io/badge/dimolto3-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/jyh-skn"><img src="https://img.shields.io/badge/jyh--skn-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
  </tr>
</table>




---


<h2>🚗 목적지 주변 주차장&주유소 조회 시스템🚗</h2> 

<h3>📌 개발 기간</h3>
2026.02.05 ~ 2026.02.06

<h3>📌 프로젝트 개요</h3>
운전자는 낯선 목적지에서 주차 공간과 주유 시설 정보를 한눈에 파악하는 데 어려움을 겪는다.
본 프로젝트는 공공데이터와 웹 크롤링을 통해 구축한 데이터베이스를 기반으로, **사용자가 설정한 목적지 주변의 시설 정보를 효과적으로 필터링하여 직관적인 안내 서비스를 제공**하는 것을 목적으로 한다.

### 📌 프로젝트 내용
① 목적지 검색 및 주변 시설 필터링
>사용자가 입력한 목적지 명칭 또는 주소를 기반으로 DB 내에 저장된 시설 데이터를 조회한다.
>별도의 실시간 위치 추적(GPS) 없이도 사용자가 가고자 하는 지점 주변의 정보를 미리 파악할 수 있도록 돕는다.

② 웹 크롤링을 통한 유가 및 시설 데이터 확보
>BeautifulSoup4 및 Selenium을 활용하여 웹상의 주유소 가격 및 주차장 정보를 수집한다.
>수집된 데이터를 프로젝트용 DB에 적재하여, 외부 API 호출 없이도 시스템 내에서 독립적으로 데이터를 핸들링할 수 있는 구조를 구축한다.

③ 데이터베이스 구축 및 SQL 활용
>수집된 대량의 공공데이터(주차장 등)를 MySQL/SQLite 환경에 구축한다.
>다양한 조건(시설 구분, 운영 시간 등)에 따른 SQL 쿼리를 작성하여 사용자가 원하는 정보를 정확하게 추출하는 프로세스를 구현한다.

④ 규칙 기반 정렬 시스템 제공
>복잡한 머신러닝 대신 파이썬의 조건문과 정렬 알고리즘을 활용한 규칙 기반 로직을 적용한다.


---

## 📝 데이터 베이스(ERD)


---



---

## 🛠 기술 스택
- **Backend**: ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- **Frontend**: ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) 
- **Database**: ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
- **Data**: Pandas  
- **Infra**: ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)


---

## 💢트러블슈팅

---

## 📂 프로젝트 설계
```bash
project-root/           
├── data/
│   ├── dump.sql              # 테이블 생성 및 데이터 동기화용 DB 쿼리
├── src/                      # 소스 코드 모듈
│   ├── __init__.py            
│   └── database.py           # DB 연결 로직
├── app.py                    # steamlit 메인 페이지 
├── requirements.txt          # 필요 라이브러리 목록
├── .gitignore                
└── README.md                 # 프로젝트 소개, 설치 및 실행 가이드
```
---


## ✅수행결과
