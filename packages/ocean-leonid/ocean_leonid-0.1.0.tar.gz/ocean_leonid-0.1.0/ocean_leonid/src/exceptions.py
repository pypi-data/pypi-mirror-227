class ApiFailed(Exception):
    def __init__(self, api_name: str) -> None:
        self.message = f"The API {api_name} failed"
        super().__init__(self.message)
