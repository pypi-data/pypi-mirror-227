import os

import ovh


client = ovh.Client()

serviceName = os.getenv("OVH_CLOUD_PROJECT_SERVICE")

k8s = client.post(f'/cloud/project/{serviceName}/kube',
    name         = "kube-1",
    version      = "8",
    plan         = "essential",
    nodesList    = [
        {
            "flavor": "db1-7",
            "region": "BHS"
        }
    ]
)

print(k8s)
