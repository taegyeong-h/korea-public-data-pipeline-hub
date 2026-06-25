import time
import requests

class SeoulOpenApiClient:
    """
    글로벌 표준 사양의 서울시 Open API 전용 데이터 수집 부품(Client)
    """

    def __init__(self, api_key: str):
        # 1️⃣ 생성자: 변하지 않는 고유 인증키는 부품이 태어날 때 딱 한 번만 주입받아 기억하네!
        self.api_key = api_key
        self.base_url = "http://openapi.seoul.go.kr:8088"

    def _build_url(self, service_name: str, req_type: str, start_idx: int, end_idx: int) -> str:
        # 2️⃣ 내부 헬퍼 메서드: 지저분한 URL 조립은 밖에서 안 보게 내부에서 비밀스럽게 처리하네!
        return f"{self.base_url}/{self.api_key}/{req_type}/{service_name}/{start_idx}/{end_idx}/"

    def fetch_data(self, service_name: str, req_type: str = "json", start_idx: int = 1, end_idx: int = 1000) -> dict:
        # 3️⃣ 핵심 액션 메서드: 실제로 외부 API를 호출해서 데이터를 긁어오는 방일세!
        url = self._build_url(service_name, req_type, start_idx, end_idx)
        time.sleep(0.5)

        max_retries = 3
        backoff_factor = 2   # 재 시도전까지 몇초의 대기시간

        for attempt in range(max_retries):
            try:
                # 네트워크가 무한 대기에 빠지는 걸 방지하기 위해 10초 고정
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # 400, 500 에러 나면 즉시 폭파시켜 안전장치 확보!

                if req_type == "json":
                    return response.json()
                return response.text  # XML 등 대응

            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                print(f"⚠️ [시도 {attempt}/{max_retries}] API 통신 중 문제 발생: {e}")

                if attempt == max_retries:
                    print(f"3번이나 요청했는데 결국 서울시 서버가 뻗었습니다. 수집 포기!")
                    return {}

                # 🚀 지수 백오프 계산: 1회 실패시 2초 대기, 2회 실패시 4초 대기 후 재도전!
                wait_time = backoff_factor ** attempt
                print(f"⏳ {wait_time}초 동안 숨 고르고 다시 들이받아 보겠습니다...")
                time.sleep(wait_time)


                return {}