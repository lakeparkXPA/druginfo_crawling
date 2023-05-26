# Drug Info Crawling
www.druginfo.co.kr 사이트에서 EDI를 이용해서 해당 약물의 주성분코드, 대표코드, 표준코드, 청구코드[KD코드],복지부분류, ATC코드 추출 후 엑셀로 저장

## 작동방식
![스크린샷 2023-05-26 오후 4 09 21](https://github.com/lakeparkXPA/druginfo_crawling/assets/47446855/a25021ff-e865-46f1-8eb7-fd298255908b)
1. id, password 입력
2. 로그인
3. 검색창에 EDI 입력
4. 검색

![스크린샷 2023-05-26 오후 4 10 31](https://github.com/lakeparkXPA/druginfo_crawling/assets/47446855/eae8a193-3c91-49b3-9ee8-66677374565c)
해당 검색 결과에서 세부정보를 위한 url 획득 및 이동

![스크린샷 2023-05-26 오후 4 10 52](https://github.com/lakeparkXPA/druginfo_crawling/assets/47446855/5ff00211-ab11-4d4d-bc0b-0f931ad8e5ed)
세부 페이지에서 필요 코드 추출 및 엑셀로 결과 저장
