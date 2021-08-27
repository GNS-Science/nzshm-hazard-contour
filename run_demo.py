#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
from runzi.automation.scaling.toshi_api import ToshiApi

# Set up local config, from environment variables, with some some defaults
from runzi.automation.scaling.local_config import (API_KEY, API_URL, S3_URL)

import hazard_contour

def fetch_hazard(table_id):
    toshi_api = ToshiApi(API_URL, S3_URL, None, with_schema_validation=False, headers={"x-api-key":API_KEY})
    data = toshi_api.table.get_table(table_id)
    return data

if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("config")
    # args = parser.parse_args(
    t0 = dt.datetime.utcnow()
    print(f"Starting Task at {dt.datetime.utcnow().isoformat()}")
    #fetch_hazard("VGFibGU6MTEyeHdGWA==")
    table = fetch_hazard("VGFibGU6MjZWWUh3UA==")

    t1 = dt.datetime.utcnow()
    print("Download took  %s secs" % (t1-t0).total_seconds())
    #print(table)

    gj = hazard_contour.as_geojson(table)
    t2 = dt.datetime.utcnow()
    print("plot took  %s secs" % (t2-t1).total_seconds())


examples = '''
          {
            "node": {
              "__typename": "Table",
              "id": "VGFibGU6MTEyeHdGWA==",
              "name": "Inversion Solution Gridded Hazard",
              "created": "2021-08-11T01:40:34.379520+00:00",
              "table_type": "HAZARD_GRIDDED",
              "object_id": "SW52ZXJzaW9uU29sdXRpb246MTIzMy4wbkFtR0Q="
            }
          },
          {
            "node": {
              "__typename": "Table",
              "id": "VGFibGU6MThxNGszdw==",
              "name": "Inversion Solution Gridded Hazard",
              "created": "2021-08-12T05:49:16.935304+00:00",
              "table_type": "HAZARD_GRIDDED",
              "object_id": "SW52ZXJzaW9uU29sdXRpb246MTIzMy4wbkFtR0Q="
            }
          },
          {
            "node": {
              "__typename": "Table",
              "id": "VGFibGU6MjBHTXVFdw==",
              "name": "Inversion Solution Gridded Hazard",
              "created": "2021-08-12T06:01:48.527625+00:00",
              "table_type": "HAZARD_GRIDDED",
              "object_id": "SW52ZXJzaW9uU29sdXRpb246MTIzMy4wbkFtR0Q="
            }
'''