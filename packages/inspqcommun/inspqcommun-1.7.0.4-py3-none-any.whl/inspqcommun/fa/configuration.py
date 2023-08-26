import os

DEFAULT_LOG_LEVEL: str = "INFO"
DEFAULT_FILES_PATH: str = None
DEFAULT_FA_BASE_URL: str = 'http://localhost:8089'
DEFAULT_FA_BASE_URI: str = '/fa-services'

class Configuration:

    def get_log_level(self, default_value=DEFAULT_LOG_LEVEL) -> str:
        return os.environ.get("LOG_LEVEL", default_value)

    def get_files_path(self, default_value=DEFAULT_FILES_PATH) -> str:
        return os.environ.get("FILES_PATH", default_value)

    def get_fonctions_allegees_url(self, default_value=DEFAULT_FA_BASE_URL) -> str:
        return os.environ.get("FA_BASE_URL", default_value)

    def get_fonctions_allegees_uri(self, default_value=DEFAULT_FA_BASE_URI) -> str:
        return os.environ.get("FA_BASE_URI", default_value)

    def get_authorization_header(self) -> str:
        return "bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJFek1yYjhzOGdwXzVPcGJkOWYzaE8wUVVLdXpBdjJ2LXltVEk2MGpCdXBVIn0.eyJleHAiOjE2ODkzNTQ1NzQsImlhdCI6MTY4OTM1NDUxNCwianRpIjoiMzRjY2RmMjItMGU5Zi00Mjk5LTkwOGMtOWU0YTg5N2E0YWE3IiwiaXNzIjoiaHR0cDovL2luc3BxLTY2NzMuaW5zcHEucWMuY2E6MTgwODEvYXV0aC9yZWFsbXMvbXNzcyIsImF1ZCI6WyJmYXNlcnZpY2VzbG9jYWwiLCJhY2NvdW50Il0sInN1YiI6IjM2MTAyZjllLTRjNGUtNDRiZC1iNzlmLTkyMTRkMGNlMDAyOSIsInR5cCI6IkJlYXJlciIsImF6cCI6ImZhaXVzbG9jYWwiLCJzZXNzaW9uX3N0YXRlIjoiZDI5MzVkYTEtM2E4Ni00Yzk1LTljZWEtOTUzNWNkYjVjMmY4IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtbXNzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiZmFzZXJ2aWNlc2xvY2FsIjp7InJvbGVzIjpbImZhLXNhaXNpZSIsImZhLXV0aWxpc2F0ZXVyIl19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiZDI5MzVkYTEtM2E4Ni00Yzk1LTljZWEtOTUzNWNkYjVjMmY4IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoiU3VwZXIgUGVybWlzc2lvbnMiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJwZXJtaXNzaW9ucyIsImdpdmVuX25hbWUiOiJTdXBlciIsImZhbWlseV9uYW1lIjoiUGVybWlzc2lvbnMiLCJlbWFpbCI6Im5vYm9keUBpbnNwcS5xYy5jYSJ9.EpbzoEHqpW41jeQXWiryw0N4oC64UJCFzo8E0f-hUGHOUjB_hD4GcN6x6-xtCfqd9Wuo6rdrJoiglBBmRiw07PfqsozgiXZONrDm-489bPPX5uBzVP5SlW0A93AyzkmZeZ6-JIF7U2_XK98BZU8_DeU5HROgoowYAMFWKD-ZOMa2vsPN4W4oNvrIjQx_7UHI4uz456JnXrWvp5P4upYxGOCdWA1beTFzEsclhoqH_EMuUvqTMZf-zqEXCiLiO_tZuNnT1lisuaN68NeggqnDxbBKcKpj9WdEq5bo90Ay3MksaZvKUyqAr4AXk9a8FM2JCpjHtsIjIhN23h38i03pYA"