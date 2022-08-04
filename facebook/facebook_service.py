from typing import Optional, Union
from datetime import datetime, timedelta

from compose import compose

from facebook.pipeline import interface, pipelines
from facebook import facebook_repo
from db import bigquery
from tasks import cloud_tasks

DATE_FORMAT = "%Y-%m-%d"


def pipeline_service(
    pipeline: interface.AdsInsights,
    start: Optional[str],
    end: Optional[str],
) -> dict[str, Union[str, int]]:
    ads_account_id = "12726671"

    _start = (
        (datetime.utcnow() - timedelta(days=8))
        if not start
        else datetime.strptime(start, DATE_FORMAT)
    )
    _end = datetime.utcnow() if not end else datetime.strptime(end, DATE_FORMAT)

    return compose(
        lambda x: {
            "table": pipeline.name,
            "ads_account_id": ads_account_id,
            "start": start,
            "end": end,
            "output_rows": x,
        },
        bigquery.load(pipeline.name, pipeline.schema, pipeline.id_key, ads_account_id),
        pipeline.transform,
        facebook_repo.get(pipeline.level, pipeline.fields, pipeline.breakdowns),
    )(ads_account_id, _start, _end)


def tasks_service(start: Optional[str], end: Optional[str]) -> dict[str, int]:
    return {
        "tasks": cloud_tasks.create_tasks(
            [
                {
                    "table": table,
                    "start": start,
                    "end": end,
                }
                for table in pipelines.keys()
            ],
            lambda x: x["table"],
        )
    }
