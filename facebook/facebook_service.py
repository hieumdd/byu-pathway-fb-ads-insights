from typing import Optional, Union
from datetime import datetime, timedelta

from compose import compose

from facebook.pipeline.interface import AdsInsights
from facebook.facebook_repo import get
from db.bigquery import load

DATE_FORMAT = "%Y-%m-%d"


def pipeline_service(pipeline: AdsInsights):
    def run(
        start: Optional[str],
        end: Optional[str],
    ) -> dict[str, Union[str, int]]:
        ads_account_id = '12726671'
        
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
            load(pipeline.name, pipeline.schema, ads_account_id),
            pipeline.transform,
            get(pipeline.level, pipeline.fields, pipeline.breakdowns),
        )(ads_account_id, _start, _end)

    return run
