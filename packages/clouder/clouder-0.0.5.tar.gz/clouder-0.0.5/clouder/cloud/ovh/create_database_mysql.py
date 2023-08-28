import os

import ovh


client = ovh.Client()

serviceName = os.getenv("OVH_CLOUD_PROJECT_SERVICE")

mysql = client.post(f'/cloud/project/{serviceName}/database/mysql',
    description  = "mysql-1",
    version      = "8",
    plan         = "essential",
    nodesList    = [
        {
            "flavor": "db1-7",
            "region": "BHS"
        }
    ]
)

print(mysql)
