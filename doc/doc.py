influxdb_doc = '''### Description
InfluxDB component allows you to save, read, delete and query data from the DB directly in the Loko flow.

### Configuration

The block's configuration is divided in 3 sections: *Save Parameters*, *Delete Parameters* and *Read Parameters*.

#### Save Parameters

First you have to set the **Bucket Name**.

**Manual** parameter allows you to manually set the **Measurement Name** and the names of the keys associated to 
**Time**, **Tags** and **Fields**. If the input data already provides this information you can set **Manual** to 
False.

#### Delete Parameters

You have to set the **Bucket Name** and the time range: **Start** and **Stop**. 

If you set **From query** to False, you can delete all data saved with a given **Measurement Name**. Otherwise, you can 
provide a custom query as the input of the block.

#### Read Parameters

In order to read data from your DB you have to provide the **Bucket Name**, **Measurement Name** and the time range: 
**Start** and **Stop**.
 
### Input

**Save** input requires a list of dictionaries. If you manually set **Time**, **Tags** and **Fields** you can simply 
pass the rows of your data. Otherwise, you have to map your data:
```json
[   {"measurement":"sensor",
    "tags":{"machine_status":"NORMAL"},
    "fields":{"sensor_00":2.405382,"sensor_01":50.0868,"sensor_02":51.25868,"sensor_03":44.2274284362793},
    "time":"2018-08-17 21:20:00"
    },
    {"measurement":"sensor",
    "tags":{"machine_status":"NORMAL"},
    "fields":{"sensor_00":2.4004630000000002,"sensor_01":50,"sensor_02":51.30208,"sensor_03":44.2274284362793},
    "time":"2018-08-17 21:21:00"
    },
    {"measurement":"sensor",
    "tags":{"machine_status":"NORMAL"},
    "fields":{"sensor_00":2.406366,"sensor_01":50,"sensor_02":51.3020820617676,"sensor_03":44.2274284362793},
    "time":"2018-08-17 21:22:00"
    },
]
```

**Read** doesn't require specific input.

**Delete** input requires a query if parameter **From query** is set to True. 

Example:  

```json
_measurement="sensor"
```

**Query** input requires the string of the query.

Example:  

```json
from(bucket:"influx-bu") |> range(start: 1970-01-01T00:00:00Z, stop: 2022-10-24T08:00:00Z) |> filter(fn: (r) => r._measurement == "sensor")
```

'''