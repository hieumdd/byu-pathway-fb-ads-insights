from typing import Any
from datetime import datetime

from google.cloud import bigquery

BQ_CLIENT = bigquery.Client()

DATASET = "Facebook"


def with_batched_at(
    rows: list[dict[str, Any]],
    schema: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return (
        [
            {**row, "_batched_at": datetime.utcnow().isoformat(timespec="seconds")}
            for row in rows
        ],
        schema + [{"name": "_batched_at", "type": "TIMESTAMP"}],
    )


def load(
    table: str,
    schema: list[dict[str, Any]],
    ads_account_id: str,
):
    def _load(data: list[dict[str, Any]]) -> int:
        if len(data) == 0:
            return 0

        _rows, _schema = with_batched_at(data, schema)

        output_rows = (
            BQ_CLIENT.load_table_from_json(
                _rows,
                f"{DATASET}.{table}_{ads_account_id}",
                job_config=bigquery.LoadJobConfig(
                    create_disposition="CREATE_IF_NEEDED",
                    write_disposition="WRITE_APPEND",
                    schema=_schema,
                ),
            )
            .result()
            .output_rows
        )
        return output_rows

    return _load
