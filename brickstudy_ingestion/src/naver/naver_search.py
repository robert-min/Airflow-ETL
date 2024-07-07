import requests
from . import client_id, client_secret
from src.common.errorcode import Naver
from src.common.exception import ExtractError


class NaverSearch:
    def __init__(
            self,
            target_platform: str,
            resp_format: str = "json"
    ) -> None:
        """
        params:
            - target_platform: 검색 대상 플랫폼(blog, news, cafe, etc)
            - resp_format: api 응답 반환 포맷(json or xml)
        """
        self.base_url = f"https://openapi.naver.com/v1/search/{target_platform}.{resp_format}"
        self.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

    def request_with_keword(
            self,
            query: str,         # 검색어. UTF-8로 인코딩되어야 합니다.
            display: int = 1,   # 한 번에 표시할 검색 결과 개수(기본값: 10, 최댓값: 100)
            start: int = 1,     # 검색 시작 위치(기본값: 1, 최댓값: 1000)
            sort: str = "sim"   # 검색 결과 정렬 방법 - sim: 정확도순으로 내림차순 정렬(기본값) - date: 날짜순으로 내림차순 정렬
    ) -> dict:
        try:
            sub_url = f"?query={query}&display={display}&start={start}&sort={sort}"
            url = self.base_url + sub_url

            response = requests.get(url, headers=self.headers)

            if response.status_code == 401:
                raise ExtractError(**Naver.AuthError.value,
                                   log=response.json())
            return response.json()
        except Exception as e:
            raise ExtractError(**Naver.UnknownError.value, log=str(e))