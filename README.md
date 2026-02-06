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
공공데이터 기반의 MySQL 공간 쿼리를 활용해 목적지 반경 내 시설을 정밀하게 필터링하며, 
가격 변동이 잦은 주유소 정보는 실시간 API로 정확성을 높였습니다. 
지도 시각화와 카드 UI를 통해 복잡한 검색 과정 없이 직관적인 모빌리티 환경을 제공합니다.

### 📌 프로젝트 내용
1️⃣ 장소 기반 주차장&주유소 검색 및 시각화
- 사용자의 검색 의도에 맞춰 정보를 파악할 수 있는 직관적인 모빌리티 탐색 환경을 제공
- 사용자가 입력한 장소 또는 주소의 좌표를 분석하여, 해당 위치 반경 내의 정보를 조회
- 주차장과 주유소 정보를 동시에 제공하여 최신성과 안정성을 확보
- 실시간 위치 추적 없이도 원하는 장소 주변 상황을 미리 탐색해 볼 수 있어 사용자 편의성을 높임
- 방대한 양의 데이터를 지도 마커와 카드를 활용하여 한눈에 파악할 수 있도록 구현

2️⃣ 공공데이터 Open API 수집 및 가공
- 신뢰성 높은 공공기관의 데이터를 활용하여 프로젝트에 데이터셋을 구축
- 공공데이터 Open API를 통해 전국의 주유소 및 주차장 정보 수집
- 수집한 주차장 데이터를 프로젝트용 DB에 적재하여, API 호출 없이 시스템 내에서 독립적으로 데이터 핸들링 가능하도록 설계
- 주유소 정보는 실시간 API 호출을 활용하여 변동성 있는 가격의 정확성을 높임

3️⃣ MySQL 인프라 구축 및 공간 데이터 활용 
- 대량의 데이터를 효율적으로 관리하고 정교한 위치 기반 필터링을 수행할 수 있는 백엔드 구조를 실현
- 수집한 수만 건에 달하는 주차장 공공데이터를 MySQL 환경에 안정적으로 구축
- 위도와 경도 데이터를 활용한 공간 쿼리를 작성하여 사용자가 지정한 위치에서 정확한 거리 내에 있는 정보만을 추출하는 고정밀 필터링 프로세스를 구현
- 프로젝트 활용 목적에 맞는 핵심 데이터만을 선별하여 시스템의 효율성을 높임

 


---

## 📝 데이터 베이스(ERD)
<img src="images/ERD.png" width="500" alt="ERD">

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
## 🛠️ 기술 스택
- **Backend**: ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
- **Frontend**: ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) 
- **Database**: ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
- **Data**: Pandas  
- **Infra**: ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 💢트러블슈팅

---


## ✅수행 결과


---
## 🫱🏻‍🫲🏻팀원 회고

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom: 30px;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">대상자</th>
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">작성자</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고 내용</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd;">이창우</td>
            <td style="text-align: center; border: 1px solid #ddd;">김지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박기은</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박은지</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">윤정연</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">홍지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
    </tbody>
</table>

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom: 30px;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">대상자</th>
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">작성자</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고 내용</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd;">김지윤</td>
            <td style="text-align: center; border: 1px solid #ddd;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박기은</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박은지</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">윤정연</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">홍지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
    </tbody>
</table>

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom: 30px;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">대상자</th>
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">작성자</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고 내용</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd;">박기은</td>
            <td style="text-align: center; border: 1px solid #ddd;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">김지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박은지</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">윤정연</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">홍지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
    </tbody>
</table>

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom: 30px;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">대상자</th>
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">작성자</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고 내용</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd;">박은지</td>
            <td style="text-align: center; border: 1px solid #ddd;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">김지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박기은</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">윤정연</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">홍지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
    </tbody>
</table>

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom: 30px;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">대상자</th>
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">작성자</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고 내용</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd;">윤정연</td>
            <td style="text-align: center; border: 1px solid #ddd;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">김지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박기은</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박은지</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">홍지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
    </tbody>
</table>

<table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd; margin-bottom: 30px;">
    <thead>
        <tr style="background-color: #f8f9fa;">
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">대상자</th>
            <th style="width: 15%; border: 1px solid #ddd; padding: 10px;">작성자</th>
            <th style="border: 1px solid #ddd; padding: 10px;">회고 내용</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5" style="text-align: center; font-weight: bold; border: 1px solid #ddd;">홍지윤</td>
            <td style="text-align: center; border: 1px solid #ddd;">이창우</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">김지윤</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박기은</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">박은지</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
        <tr>
            <td style="text-align: center; border: 1px solid #ddd;">윤정연</td>
            <td style="border: 1px solid #ddd; padding: 10px;">내용을 입력하세요.</td>
        </tr>
    </tbody>
</table>
