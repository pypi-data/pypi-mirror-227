import os

import ovh


client = ovh.Client()

serviceName = os.getenv("OVH_CLOUD_PROJECT_SERVICE")

mysqls = client.get(f'/cloud/project/{serviceName}/database/mysql')

for mysql in mysqls:
    print('----', mysql)
    details = client.get(f'/cloud/project/{serviceName}/database/mysql/{mysql}')
    print(details)
    print()
