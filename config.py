"""
Конфигурационные переменные
"""

URL_TOKENIZE = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize"
URL_COMPLETION = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
IAM_TOKEN_REFRESH = (
    "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
)

MAX_PROJECT_TOKENS = 3000  # макс. количество токенов на весь проект

MAX_USERS = 3  # макс. количество пользователей на весь проект
MAX_SESSIONS = 2  # макс. количество сессий у пользователя
MAX_TOKENS_IN_SESSION = 500  # макс. количество токенов за сессию пользователя
MAX_TOKENS_QUEUE = 50
REQUEST_TIMEOUT_SECONDS = 5

TEMPERATURE = 0.6

BOT_TOKEN = "6582632456:AAGwIifUHIEGwQxAE8uW2zZZr9hXn4JuEao"
IAM_TOKEN = "t1.9euelZqclIqOzZaNm4-MmpGPi8_Ozu3rnpWakpCTmYmMz86MncaRz5mUi8jl8_d_F1tP-e9VOhVo_N3z9z9GWE_571U6FWj8zef1656VmpGVzsuXkZWPyMiVx5GelozL7_zF656VmpGVzsuXkZWPyMiVx5GelozLveuelZrOj5SYy5mTmYyYlJacx5WSk7XehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.eZyRSYocE8T1fppDUlKlu4uZbR8TntvfJ9lJ9xdSFCpMd5tUbG1zyprJPXe5sXGvViwIc4p7kEIcTPO70WP3AQ"
FOLDER_ID = "b1gu8kb83kb7j102ttn9"

DB_NAME = "db.sqlite"
TABLE_NAME = "prompts"
LOG_FILE_PATH = "logs.log"
