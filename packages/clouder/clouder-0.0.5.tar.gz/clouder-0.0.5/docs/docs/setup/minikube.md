# Setup on Minikube

## Minikube

You will need [minikube](https://github.com/kubernetes/minikube) and associated Kubernetes tooling.

```bash
# Install kubectl and helm.
dla kubectl-install && \
  dla helm-install
```

```bash
# Install minikube.
dla minikube-stop && \
  dla minikube-rm && \
  dla minikube-install
```

```bash
# Start minikube.
dla minikube-start && \
  kubectl config get-contexts && \
  kubectl config current-context && \
  kubectl config use-context minikube && \
  kubectl config current-context
```

```bash
# Deploy ingress-nginx
# https://minikube.sigs.k8s.io/docs/tutorials/custom_cert_ingress
# Create TLS secret which contains custom certificate and private key
openssl req -new -newkey rsa:4096 -nodes -keyout key.key -out key.csr
openssl x509 -req -sha256 -days 9365 -in key.csr -signkey key.key -out cert.pem
kubectl -n kube-system create secret tls mkcert --key key.key --cert cert.pem
minikube addons disable ingress
minikube addons configure ingress
# -- Enter custom cert(format is "namespace/secret"): kube-system/mkcert
# https://minikube.sigs.k8s.io/docs/handbook/addons/custom-images
minikube addons enable ingress \
  --images="IngressController=datalayer/ingress-nginx-controller:v1.0.0-beta.3" \
  --registries="IngressController=docker.io" \
  --refresh=true
minikube addons images ingress
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx
# - --default-ssl-certificate=kube-system/mkcert
kubectl -n ingress-nginx \
  get deployment ingress-nginx-controller -o yaml | grep "kube-system"
POD_NAME=$(kubectl get pods -l app.kubernetes.io/name=ingress-nginx -n ingress-nginx -o jsonpath='{.items[2].metadata.name}')
kubectl describe pod $POD_NAME -n ingress-nginx | grep docker.io # Image: docker.io/datalayer/ingress-nginx-controller:v1.0.0-beta.3
kubectl exec -it $POD_NAME -n ingress-nginx -- /nginx-ingress-controller --version
kubectl exec -it $POD_NAME -n ingress-nginx -- bash
vi /etc/nginx/nginx.conf
cat /etc/nginx/nginx.conf
#  httponly = false,
cat /etc/nginx/lua/balancer/sticky.lua | grep httponly
exit
#
# https://minikube.sigs.k8s.io/docs/tutorials/nginx_tcp_udp_ingress/
#
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: tcp-services
  namespace: ingress-nginx
EOF
#
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
  namespace: default
  labels:
    app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - image: redis
        imagePullPolicy: Always
        name: redis
        ports:
        - containerPort: 6379
          protocol: TCP
EOF
#
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: default
spec:
  selector:
    app: redis
  type: ClusterIP
  ports:
    - name: tcp-port
      port: 6379
      targetPort: 6379
      protocol: TCP
EOF
#
kubectl patch configmap tcp-services -n ingress-nginx --patch '{"data":{"6379":"default/redis-service:6379"}}'
kubectl get configmap tcp-services -n ingress-nginx -o yaml
#
kubectl patch deployment ingress-nginx-controller -n ingress-nginx --patch "
spec:
  template:
    spec:
      containers:
      - name: controller
        ports:
         - containerPort: 6379
           hostPort: 6379
"
kubectl get svc -n ingress-nginx
#
curl $(minikube ip) 6379
telnet $(minikube ip) 6379
#
# https://stackoverflow.com/questions/72246990/nginx-ingress-tcp-services-connection-refused
#
curl http://$(minikube ip):80
#
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: tcp-services
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
data:
  "8686": "datalayer/jupyterpool-jupyterpool-svc:8686"
EOF
#
kubectl edit svc ingress-nginx-controller -n ingress-nginx

  - appProtocol: http
    name: http
    nodePort: 30927
    port: 80
    protocol: TCP
    targetPort: http
  - appProtocol: https
    name: https
    nodePort: 32372
    port: 443
    protocol: TCP
    targetPort: https
  - appProtocol: tcp
    name: proxied-tcp-8686
    nodePort: 32333
    port: 8686
    protocol: TCP
    targetPort: 8686

kubectl get svc ingress-nginx-controller -n ingress-nginx
kubectl describe svc ingress-nginx-controller -n ingress-nginx
#
curl http://$(minikube ip):32333
curl http://$(minikube ip):8686
```

## Host File

```bash
# Configure /etc/hosts file.
# This is needed if you want to invoke the minikube services from your local environment.
echo """# === Datalayer Dev Start ===

$(minikube ip) minikube.local jupyter.local rest.jupyter.minikube.local ws.jupyter.minikube.local ldapadmin.minikube.local datalayer-keycloak-http.datalayer-keycloak.svc.cluster.local

127.0.0.1 default-solr-datalayer-solrcloud.local default-solr-datalayer-solrcloud-0.local default-solr-datalayer-solrcloud-1.local default-solr-datalayer-solrcloud-2.local

127.0.0.1 datalayer-solr-zookeeper-0.datalayer-solr-zookeeper-headless.datalayer-solr datalayer-solr-0.datalayer-solr-headless.datalayer-solr datalayer-solr-1.datalayer-solr-headless.datalayer-solr datalayer-solr-zookeeper-headless local.datalayer-minio-hl.datalayer-minio.svc.cluster.local minio.datalayer-minio.svc.cluster.local

127.0.0.1 solr-datalayer-solrcloud-0.solr-datalayer-solrcloud-headless.default solr-datalayer-solrcloud-1.solr-datalayer-solrcloud-headless.default solr-datalayer-solrcloud-2.solr-datalayer-solrcloud-headless.default

127.0.0.1 solr-datalayer-solrcloud-zookeeper-0.solr-datalayer-solrcloud-zookeeper-headless.default.svc.cluster.local solr-datalayer-solrcloud-zookeeper-1.solr-datalayer-solrcloud-zookeeper-headless.default.svc.cluster.local solr-datalayer-solrcloud-zookeeper-2.solr-datalayer-solrcloud-zookeeper-headless.default.svc.cluster.local

127.0.0.1 cassandra-datalayer-dc-datalayer-service.default.svc.cluster.local

# === Datalayer Dev End ===
""" | sudo tee -a /etc/hosts
# Check the host file.
cat /etc/hosts
```

## Chrome

- Allow invalid certificates for resources loaded from localhost: Allows requests to localhost over HTTPS even when an invalid certificate is presented. – Mac, Windows, Linux, Chrome OS, Android, Fuchsia #allow-insecure-localhost Enabled

- Insecure origins treated as secure: Treat given (insecure) origins as secure origins. Multiple origins can be supplied as a comma-separated list. Origins must have their protocol specified e.g. "http://example.com". For the definition of secure contexts, see https://w3c.github.io/webappsec-secure-contexts/ – Mac, Windows, Linux, Chrome OS, Android, Fuchsia http://localhost,http://minikube.local

## Docker

```bash
# Build docker images for minikube docker.
eval $(minikube docker-env) && \
  dla docker-build
```

## K8S Dashboard

```bash
# Deploy the k8s dashboard service.
dla up minikube k8s-dashboard
# Give some more role to k8s-dashboard-kubernetes-dashboard.
cat <<EOF | kubectl create -f -
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: k8s-dashboard
  labels:
    k8s-app: k8s-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: k8s-dashboard-kubernetes-dashboard
  namespace: kube-system
EOF
# Browse k8s dashboard.
echo open https://localhost:8443
dla k8s-dashboard
```

## Simple Service

```bash
# Deploy simple service.
dla up minikube datalayer-simple
dla helm-ls
# View k8s resources.
kubectl get pods -n datalayer-simple
kubectl get secrets -n datalayer-simple
kubectl describe secrets -n datalayer-simple simple-secret
kubectl get secret -n datalayer-simple simple-secret -o jsonpath="{.data.password}" | base64 --decode
# Access via ingress.
open http://minikube.local/info
open http://minikube.local/env
open http://minikube.local/health
open http://minikube.local/endpoint0
# Access via service.
open $(minikube service -n datalayer-simple simple-svc --url)/info
open $(minikube service -n datalayer-simple simple-svc --url)/env
open $(minikube service -n datalayer-simple simple-svc --url)/health
open $(minikube service -n datalayer-simple simple-svc --url)/endpoint0
minikube service simple-svc-echo -n datalayer-simple
minikube service simple-svc-echo-2 -n datalayer-simple
# Shell into a pod.
export POD_NAME=$(kubectl get pods --namespace datalayer-simple -l "app=simple" -o jsonpath="{ .items[0].metadata.name }") && \
  kubectl exec -n datalayer-simple -it $POD_NAME -- /bin/bash
curl simple-svc-echo-2.datalayer-simple.svc.cluster.local:8080
curl simple-svc-echo.datalayer-simple.svc.cluster.local:5678
curl simple-svc.datalayer-simple.svc.cluster.local:9876
exit
# View mounted secret.
POD_NAME=$(kubectl get pods -n datalayer-simple -l "app=simple-echo-2" -o jsonpath="{.items[0].metadata.name}") && \
  echo $POD_NAME && \
  kubectl exec $POD_NAME -n datalayer-simple -i -t -- echo $DATALAYER_LDAP_BIND_PWD
# Access via Port-Forward.
open http://localhost:8080/info
export POD_NAME=$(kubectl get pods -n datalayer-simple -l "app=simple" -o jsonpath="{ .items[0].metadata.name }") && \
  echo "Visit http://localhost:8080/info to access the simple service" && \
  kubectl port-forward -n datalayer-simple $POD_NAME 8080:9876
# Access via ClusterIP.
CLUSTER_IP=$(kubectl get svc/simple-svc -n datalayer-simple -o custom-columns=IP:spec.clusterIP --no-headers=true)
echo "Visit http://$CLUSTER_IP:???/info"
# Access via NodePort.
export NODE_PORT=$(kubectl get -n datalayer-simple -o jsonpath="{.spec.ports[0].nodePort}" services simple-svc) && \
  export NODE_IP=$(kubectl get nodes -n datalayer-simple -o jsonpath="{.items[0].status.addresses[0].address}") && \
  URL=http://$NODE_IP:$NODE_PORT/info && \
  echo $URL && \
  open $URL
# Tear down.
dla down datalayer-simple
```

## NFS

```bash
cat << EOF | kubectl apply -f -
# Create a service to expose the NFS server to pods inside the cluster.
kind: Service
apiVersion: v1
metadata:
  name: nfs-service
spec:
  selector:
    role: nfs
  ports:
    - name: tcp-2049
      port: 2049
      protocol: TCP
    - name: udp-111
      port: 111
      protocol: UDP
---
# Run the NFS server image in a pod that is exposed by the service.
kind: Pod
apiVersion: v1
metadata:
  name: nfs-server
  labels:
    role: nfs
spec:
  containers:
    - name: nfs-server
      image: cpuguy83/nfs-server
      securityContext:
        privileged: true
      args:
        # Pass the paths to share to the Docker image
        - /exports
EOF
```
kubectl describe svc nfs-service
kubectl exec -it nfs-server -- bash
cat /etc/exports

## NFS Proxy

```bash
yum install haproxy
vi /etc/haproxy/haproxy.cfg 
systemctl enable haproxy
systemctl restart haproxy
journalctl -u haproxy.service --since today --no-pager
ps -ef | grep ha

# http://haproxy.1wt.eu/download/1.4/doc/configuration.txt

global
    # to have these messages end up in /var/log/haproxy.log you will
    # need to:
    #
    # 1) configure syslog to accept network log events.  This is done
    #    by adding the '-r' option to the SYSLOGD_OPTIONS in
    #    /etc/sysconfig/syslog
    #
    # 2) configure local2 events to go to the /var/log/haproxy.log
    #   file. A line like the following can be added to
    #   /etc/sysconfig/syslog
    #
    #    local2.*                       /var/log/haproxy.log
    #
    log         127.0.0.1 local2

    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon

    # turn on stats unix socket
    stats socket /var/lib/haproxy/stats

defaults
    mode                    tcp
    log                     global
    option                  dontlognull
    option http-server-close
    option                  redispatch
    retries                 3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout http-keep-alive 10s
    timeout check           10s
    maxconn                 3000

frontend  main *:2049
    default_backend            app 

backend app
    mode tcp
    timeout tunnel 300000
    server  nfs1 fs-0ca159b37ca7f2bbd.efs.us-east-1.amazonaws.com:2049 check
```

## Helm Charts

You will need [helm charts](https://github.com/datalayer/datalayer/tree/main/etc/helm).

```bash
# Deploy helm and build the helm charts.
dla helm-deploy && \
  dla helm-build && \
  dla helm-status
```

## Solr Service

```bash
# Install the solr & zookeeper crds.
kubectl create -f \
  https://solr.apache.org/operator/downloads/crds/v0.7.0/all-with-dependencies.yaml
# Install the solr and zookeeper operators.
# https://artifacthub.io/packages/helm/apache-solr/solr-operator
helm upgrade --install solr-operator \
  apache-solr/solr-operator \
  --version 0.7.0
```

```bash
kubectl explain solrcloud.spec.zookeeperRef.provided.config
kubectl explain solrcloud.spec.zookeeperRef.provided.persistence
kubectl explain solrcloud.spec.zookeeperRef.provided.persistence.spec
```

```bash
# Create a 3 nodes cluster.
# https://artifacthub.io/packages/helm/apache-solr/solr
#  --set addressability.external.method=Ingress \
#  --set addressability.external.domainName="local" \
#  --set addressability.external.useExternalAddress="false"
# helm upgrade --install solr-datalayer \
#   apache-solr/solr \
#   --version 0.5.0 \
#   --set image.tag=8.11.0 \
#   --set replicas=3 \
#   --set solrOptions.javaMemory="-Xms300m -Xmx600m"
# kubectl get solrclouds
kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer-minikube.yaml
kubectl get solrclouds -w
```

```bash
kubectl scale --replicas=5 solrcloud/solr-datalayer
kubectl get solrclouds -w
```

```bash
cd $DATALAYER_HOME/src && \
  make pf-solr
```

```bash
open "http://localhost:8983/solr/#/~cloud?view=nodes"
# open "http://default-solr-datalayer-solrcloud.local/solr/#/~cloud?view=nodes"
# open "http://default-solr-datalayer-solrcloud-0.local/solr/#/~cloud?view=nodes"
# open "http://default-solr-datalayer-solrcloud-1.local/solr/#/~cloud?view=nodes"
# open "http://default-solr-datalayer-solrcloud-2.local/solr/#/~cloud?view=nodes"
```

```bash
open "http://localhost:8983/solr/admin/collections?action=CREATE&name=mycoll&numShards=1&replicationFactor=3&maxShardsPerNode=2&collection.configName=_default"
curl -XPOST -H "Content-Type: application/json" \
  -d '[{id: 1}, {id: 2}, {id: 3}, {id: 4}, {id: 5}, {id: 6}, {id: 7}, {id: 8}]' \
  "http://localhost:8983/solr/mycoll/update/"
```

```bash
dla solr-init
open "http://localhost:8983/solr/#/datalayer/collection-overview"
open "http://localhost:8983/solr/#/datalayer/query"
open "http://localhost:8983/solr/#/~cloud?view=graph"
```

```bash
kubectl scale --replicas=5 solrcloud/solr-datalayer
```

```python
# Test solr with python.
python <<EOF
import pysolr
collection = 'datalayer'
zookeeper = pysolr.ZooKeeper("datalayer-solr-zookeeper-0.datalayer-solr-zookeeper-headless.datalayer-solr:2181")
solr = pysolr.SolrCloud(zookeeper, collection, always_commit=True)
solr.ping()
solr.add([{
  "id": "1",
  "title": "For Hire",
  "tags": ["professional", "jobs"],
  "posts": [{
    "id": "2",
    "title": "Search Engineer",
    "comments": [
      {
        "id": "3",
        "content_t": "I am interested"
      },
      {
        "id": "4",
        "content_t": "How large is the team?"
      }
    ]},
    {
      "id": "5",
      "title": "Medium level Engineer"
    }
  ]
}], commit = True )
for result in solr.search('title:*'): print(result)

solr.delete(id='1')
EOF
```

```bash
kubectl delete -f $DATALAYER_HOME/etc/operator/solr/datalayer-minikube.yaml
# kubectl delete solrcloud solr-datalayer
helm delete solr-operator
kubectl delete -f \
  https://solr.apache.org/operator/downloads/crds/v0.7.0/all-with-dependencies.yaml
```

## Cassandra Service

```bash
kubectl apply -f \
  https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
kubectl get storageclasses | grep rancher
```

```bash
helm upgrade --install \
  -f $DATALAYER_HOME/etc/operator/cassandra/k8ssandra-minikube.yaml \
  cassandra-datalayer \
  k8ssandra/k8ssandra
kubectl get cassandradatacenters
kubectl describe cassandradatacenter dc-datalayer | grep "Cassandra Operator Progress:"
```

```bash
export POD_NAME=$(kubectl get pods --namespace datalayer-simple -l "app=simple" -o jsonpath="{ .items[0].metadata.name }") && \
  kubectl exec -n datalayer-simple -it $POD_NAME -- /bin/bash
curl cassandra-datalayer-dc-datalayer-service.default.svc.cluster.local:9042
python3 -c 'import cassandra; print(cassandra.__version__)'
python3 <<EOF
import cassandra
print(cassandra.__version__)
from cassandra.cluster import Cluster
cluster = Cluster(['cassandra-datalayer-dc-datalayer-service.default.svc.cluster.local'])
print(cluster)
EOF
exit
```

```bash
# Terminal 1.
cd $DATALAYER_HOME/src && \
  make pf-cassandra
```

```bash
# Terminal 2.
cd $DATALAYER_HOME/src && \
  make cqlsh
```

```sql
CREATE KEYSPACE k8ssandra_test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE k8ssandra_test;
CREATE TABLE users (email text primary key, name text, state text);
INSERT INTO users (email, name, state) values ('alice@example.com', 'Alice Smith', 'TX');
INSERT INTO users (email, name, state) values ('bob@example.com', 'Bob Jones', 'VA');
INSERT INTO users (email, name, state) values ('carol@example.com', 'Carol Jackson', 'CA');
INSERT INTO users (email, name, state) values ('david@example.com', 'David Yang', 'NV');
SELECT * FROM k8ssandra_test.users;
exit
```

```bash
# cassandra stargate https://stargate.io/docs/stargate/1.0/quickstart/quick_start-rest.html
# 8081: Auth
# 8082: REST
# 8080: GraphQL
export K8SSANDRA_USERNAME=$(kubectl get secret cassandra-datalayer-superuser -o jsonpath="{.data.username}" | base64 --decode ; echo)
export K8SSANDRA_PASSWORD=$(kubectl get secret cassandra-datalayer-superuser -o jsonpath="{.data.password}" | base64 --decode ; echo)
AUTH_TOKEN=$(curl -L -X POST 'http://localhost:8081/v1/auth' \
  -H 'Content-Type: application/json' \
  --data-raw "{\"username\": \"${K8SSANDRA_USERNAME}\", \"password\": \"${K8SSANDRA_PASSWORD}\"}" \
  | jq -r '.authToken')
```

```bash
# cassandra stargate rest https://stargate.io/docs/stargate/1.0/developers-guide/rest-using.html
curl -s -L -X POST localhost:8082/v2/schemas/keyspaces \
  -H "X-Cassandra-Token: $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "users_keyspace",
    "replicas": 1
  }'
curl -s -L -X GET localhost:8082/v2/schemas/keyspaces \
  -H "X-Cassandra-Token: $AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
```

```bash
# cassandra stargate graphql
# https://stargate.io/docs/stargate/1.0/quickstart/quick_start-graphql.html
```

```bash
python3 <<EOF
import os
from astrapy.client import create_astra_client
stargate_client = create_astra_client(
  base_url = "http://localhost:8082",
  auth_base_url = "http://localhost:8081/v1/auth",
  username = os.getenv('K8SSANDRA_USERNAME'),
  password = os.getenv('K8SSANDRA_PASSWORD'),
)
print(stargate_client)
EOF
```

```bash
kubectl delete cassandradatacenter dc-datalayer
helm delete cassandra-datalayer
```

## Redis Service

```bash
# https://github.com/bitnami/charts/tree/master/bitnami/redis
# https://bitnami.com/stack/redis/helm
# https://artifacthub.io/packages/helm/bitnami/redis
# https://phoenixnap.com/kb/kubernetes-redis
# https://medium.com/@thanawitsupinnapong/setting-up-redis-in-kubernetes-with-helm-and-manual-persistent-volume-f1d52fa1919f
# https://github.com/bitnami/bitnami-docker-redis/issues/92
helm upgrade --install redis \
  bitnami/redis \
  --set image.repository=redislabs/rejson \
  --set image.tag=2.0.0 \
  --set master.extraFlags='{--loadmodule /usr/lib/redis/modules/rejson.so}'
```

```bash
export REDIS_PWD=$(kubectl get secret redis -o jsonpath="{.data.redis-password}" | base64 --decode ; echo)
kubectl exec -it redis-master-0 -- redis-cli -a $REDIS_PWD
ping
info modules
exit
```

```bash
cd $DATALAYER_HOME/src && \
  make pf-redis
```

```python
# Test redis with python.
# https://developer.redis.com/howtos/redisjson/using-python/
export REDIS_PWD=$(kubectl get secret redis -o jsonpath="{.data.redis-password}" | base64 --decode ; echo)
python <<EOF
import os
import redis
from redis.commands.json.path import Path
client = redis.Redis(
    host='localhost',
    port=6379, 
    password=os.getenv('REDIS_PWD'),
)
client.set('foo', 'bar')
value = client.get('foo')
print(value)
jane = {
  'name': "Jane", 
  'Age': 33, 
  'Location': "Chawton"
}
client.json().set('person:1', Path.rootPath(), jane)
result = client.json().get('person:1')
print(result)
EOF
```

```bash
helm uninstall redis
```

## Port Forward Minikube Services

```bash
# The [dev](./dev) folder contains useful scripts for your development environment.
# Forward Ports.
# open https://localhost:8443            # K8S Dashboard
# open http://localhost:8983/solr        # Solr
cd $DATALAYER_HOME/src && \
  make pf
```
