import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/Scheduler")
