# Setup on OVHcloud

> :sparkles: :mega: Quick Start Clouder on OVHcloud.

## K8S Dashboard

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: admin-user-token
  namespace: kubernetes-dashboard
  annotations:
    kubernetes.io/service-account.name: admin-user
EOF
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user-token | awk '{print $1}')
echo open http://localhost:8081/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy
kubectl proxy --port 8081
```

## Secrets

```bash
kubectl create secret generic aws-creds \
  --from-literal=access-key-id=$AWS_ACCESS_KEY_ID \
  --from-literal=secret-access-key=$AWS_SECRET_ACCESS_KEY \
  --namespace=default
kubectl describe secret aws-creds
```

## Solr

```bash
# dla up ovh datalayer-solr
# Wait for pods to be up.
# kubectl get pods -n datalayer-solr
```

```bash
# Install the solr & zookeeper crds.
kubectl create -f https://solr.apache.org/operator/downloads/crds/v0.7.0/all-with-dependencies.yaml
# Install the solr operator and zookeeper operator.
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
kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer.yaml
kubectl get solrclouds -w
```

```bash
# Terminal 1.
# open http://localhost:8983
cd $DATALAYER_HOME/src && \
  make pf-solr
```

```bash
# Terminal 2.
# More tests.
open http://localhost:8983/solr
open "http://localhost:8983/solr/admin/collections?action=CREATE&name=demo&numShards=3&replicationFactor=3&maxShardsPerNode=3&collection.configName=_default"
curl -XPOST -H "Content-Type: application/json" \
  -d '[{id: 1}, {id: 2}, {id: 3}, {id: 4}, {id: 5}, {id: 6}, {id: 7}, {id: 8}]' \
  "http://localhost:8983/solr/demo/update"
dla solr-init
python <<EOF
import pysolre
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
# Terminal 2.
# Create the collections.
# export DAO_FOLDER=$DATALAYER_HOME/src/run/dao/examples/model
export SOLR_HOME=$DATALAYER_HOME/opt/solr
$SOLR_HOME/bin/solr create -c accounts -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/accounts -p 8983
$SOLR_HOME/bin/solr create -c credits -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/credits -p 8983
$SOLR_HOME/bin/solr create -c invites -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/invites -p 8983
$SOLR_HOME/bin/solr create -c spaces -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/spaces -p 8983
$SOLR_HOME/bin/solr create -c tweets -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/tweets -p 8983
```

```bash
kubectl scale --replicas=5 solrcloud/solr-datalayer
```

```bash
kubectl delete -f $DATALAYER_HOME/etc/operator/solr/datalayer.yaml
kubectl delete solrcloud solr-datalayer
helm delete solr-datalayer
helm delete solr-operator
kubectl delete -f \
  https://solr.apache.org/operator/downloads/crds/v0.7.0/all-with-dependencies.yaml
```

Solr Backup

```bash
#
curl http://localhost:8983/solr/users/select?q=*:*
#
# Take recurring backups with a S3 SolrBackup.
kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer-backup-s3.yaml
#
# kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer-backup-s3-credits.yaml
# kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer-backup-s3-organisations.yaml
# kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer-backup-s3-spaces.yaml
# kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer-backup-s3-users.yaml
kubectl describe solrbackups
kubectl get solrbackups -w
aws s3 ls s3://datalayer-backups-solr/datalayer-solr-collection-backup-accounts/accounts/
curl http://localhost:8983/solr/accounts/replication?command=details
#
# Stop recurring backups.
kubectl delete -f $DATALAYER_HOME/etc/operator/solr/datalayer-backup-s3.yaml
```

Solr Restore

```bash
# Delete and re-create empty collections.
export SOLR_HOME=$DATALAYER_HOME/opt/solr
for COLLECTION in "accounts" "credits" "invites" "spaces" "tweets"
do
    curl http://localhost:8983/solr/$COLLECTION/update?commitWithin=500 -d '{ delete: { query: "*:*" } }'
    curl http://localhost:8983/solr/admin/collections?action=DELETE -d "name=${COLLECTION}"
    $SOLR_HOME/bin/solr create -c $COLLECTION -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/$COLLECTION -p 8983 -force
```

```bash
# Restore https://solr.apache.org/guide/8_11/collection-management.html#restore
# backupId=10&
for COLLECTION in "accounts" "credits" "invites" "spaces" "tweets"
do
    echo
    echo Restoring Solr "$COLLECTION" collection
    echo ---------------------------------------
    curl http://localhost:8983/solr/admin/collections -d '
action=RESTORE&
repository=s3&
collection='"$COLLECTION"'&
location=s3:/&
name=datalayer-solr-collection-backup-'"$COLLECTION"''
done
#
curl http://localhost:8983/solr/accounts/select?q=*:*
# curl http://localhost:8983/solr/accounts/update?commitWithin=500 -d '{ delete: { query: "*:*" } }'
```

## Ingress Nginx

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
# helm -n ingress-nginx install ingress-nginx ingress-nginx/ingress-nginx --create-namespace
helm upgrade --install ingress-nginx \
  ingress-nginx/ingress-nginx \
  --version 4.0.13 \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.image.registry=docker.io/datalayer \
  --set controller.image.image=ingress-nginx-controller \
  --set controller.image.tag=v1.0.0-beta.3 \
  --set controller.image.digest=sha256:0fef3aafaf1b0e02ed6ef76faf7186032341551ce905c05f274f39f774b1ebf1
helm ls -n ingress-nginx
kubectl get pods -n ingress-nginx
POD_NAME=$(kubectl get pods -l app.kubernetes.io/name=ingress-nginx -n ingress-nginx -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD_NAME -n ingress-nginx -- /nginx-ingress-controller --version
kubectl get svc ingress-nginx-controller -n ingress-nginx -w
# NAME                       TYPE           CLUSTER-IP       EXTERNAL-IP                                                              PORT(S)                      AGE
# ingress-nginx-controller   LoadBalancer   10.100.113.174   <A.B.C.D>   80:32664/TCP,443:32671/TCP   11m
# helm uninstall -n ingress-nginx ingress-nginx
```

```bash
# Create DNS A records:
# - <A.B.C.D> $DATALAYER_RUN
# - <A.B.C.D> simple-dev.datalayer.community
# - <A.B.C.D> simple-echo.dev.datalayer.run
# - Alias to <A.B.C.D>
nslookup ...
```

## Certificate Manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install \
  cert-manager \
  jetstack/cert-manager \
  --version v1.10.1 \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
helm ls -n cert-manager
kubectl get pods -n cert-manager
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # The ACME Production server URL.
    server: https://acme-v02.api.letsencrypt.org/directory
    preferredChain: "ISRG Root X1"
    # Email address used for ACME registration.
    email: eric@datalayer.io
    # Name of a secret used to store the ACME account private key.
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
    - http01:
        ingress:
            class: nginx
EOF
kubectl describe clusterissuer letsencrypt-prod
```

## Simple Service

```bash
dla down datalayer-simple
dla up ovh datalayer-simple
helm ls -A
kubectl get pods -n datalayer-simple
kubectl get secrets -n datalayer-simple
kubectl describe secrets -n datalayer-simple simple-secret
POD_NAME=$(kubectl get pods -n datalayer-simple -l "app=simple-echo-2" -o jsonpath="{.items[0].metadata.name}")
echo $POD_NAME
kubectl exec $POD_NAME -n datalayer-simple -it -- echo $DATALAYER_LDAP_BIND_PWD
kubectl exec $POD_NAME -n datalayer-simple -it -- /bin/bash
kubectl get certificates -n datalayer-simple
kubectl describe certificate simple-datalayer-run-cert -n datalayer-simple
kubectl describe certificaterequest -n datalayer-simple simple-datalayer-run-cert-s5ph...
curl https://simple-dev.datalayer.community/info
# {"version": "0.0.3", "host": "simple-dev.datalayer.community", "from": "10.44.0.2", "local_hostname": "simple-64c4fd859f-p9w74", "local_ip": "10.44.0.6", "headers": [{"Host": "simple-dev.datalayer.community"}, {"X-Request-Id": "f76ad6945e9ebc3ba9ea8da3a6ea2adb"}, {"X-Real-Ip": "10.44.0.0"}, {"X-Forwarded-For": "10.44.0.0"}, {"X-Forwarded-Host": "simple-dev.datalayer.community"}, {"X-Forwarded-Port": "443"}, {"X-Forwarded-Proto": "https"}, {"X-Forwarded-Scheme": "https"}, {"X-Scheme": "https"}, {"User-Agent": "curl/7.64.1"}, {"Accept": "*/*"}]}
curl https://simple-echo.dev.datalayer.run/simple-echo
# hello simple-echo
dla down datalayer-simple
```
