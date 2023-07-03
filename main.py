import pymongo
import time
import structlog

from helpers.db import (
    get_client,
    upsert_docs_for_all_companies,
    upsert_docs_for_one_collection,
)
from helpers.logging import get_logger

db = get_client()
stats_db = get_client()["dashboard_statistics"]

COMPANIES = list(
    map(
        lambda x: x["company_id"],
        db["PolymerizeLab"]["company"].find({}, {"company_id": 1}),
    )
)

logger = get_logger("upsert_logs")

logger.info("==> Starting upsert for all collections")
start = time.time()
# Copy over user_login_activity collection
upsert_docs_for_one_collection(
    "user_login_activity",
    db["PolymerizeLab"]["user_login_activity"],
    stats_db["user_login_activity"],
)

# Copy over work_orders collection
upsert_docs_for_all_companies("work_orders", db, stats_db, COMPANIES)

# Copy over audit_log collection
upsert_docs_for_all_companies("audit_log", db, stats_db, COMPANIES)

# Copy over projects collection
upsert_docs_for_all_companies("projects", db, stats_db, COMPANIES)

# Copy over doe_experiments collection
upsert_docs_for_all_companies("doe_experiments", db, stats_db, COMPANIES)

end = time.time()
time_taken = end - start
logger.info(f"Time taken for entire operation: {time_taken}s")
