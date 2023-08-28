# AWS

Check the requirements to setup your local environment. Check that you understand and have the following requirements.

- An AWS account with valid credentials.
- The [latest Clouder binary release](https://github.com/datalayer/datalayer/releases).
- Kubectl and Eksctl

```bash
dla kubectl-install && \
  dla eksctl-install
```

## AWS Credentials

Setup your `AWS` environment with the needed AWS credentials via environment variables.

```bash
# ~/.bashrc
# Define your valid AWS Credentials.
export AWS_ACCESS_KEY_ID=<your-aws-key-id>
export AWS_SECRET_ACCESS_KEY=<your-aws-key-secret>
export AWS_DEFAULT_REGION=us-east-1
```

If you prefer, you can persist those credentials in your home folder.

```bash
# ~/.aws/credentials
[datalayer]
aws_access_key_id=<your-aws-key-id>
aws_secret_access_key=<your-aws-key-secret>
```

```bash
# ~/.aws/config
[datalayer]
region=us-east-1
```

```bash
# gimme-aws-creds --profile $AWS_PROFILE
aws sts get-caller-identity
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
echo $AWS_ACCOUNT_ID
```

## AWS Configuration

```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
export AWS_REGION=us-east-1
export AWS_PROFILE=datalayer
export EKS_CLUSTER_NAME=datalayer-io
export EKS_NODE_GROUP_NAME=ng-1
```

## Create Cluster

```bash
# https://eksctl.io
# https://docs.aws.amazon.com/eks/latest/userguide/eks-managing.html
#
#  --nodegroup-name ng-init
#  --nodes-min 0 \
#  --nodes 0 \
#  --nodes-max 100
#  --node-type
#  --managed
#  --external-dns-access
#  --auto-kubeconfig --node-type=m5.2xlarge --region=us-west-2 --node-ami=auto --asg-access --external-dns-access --full-ecr-access -P
#  --vpc-private-subnets=subnet-0ff156e0c4a6d300c,subnet-0426fb4a607393184
#  --vpc-public-subnets=subnet-0153e560b3129a696,subnet-009fa0199ec203c37
eksctl create cluster \
  --name ${EKS_CLUSTER_NAME} \
  --version 1.21 \
  --region ${AWS_REGION} \
  --zones ${AWS_REGION}a,${AWS_REGION}b,${AWS_REGION}c \
  --without-nodegroup
```

```bash
# https://eksctl.io/usage/creating-and-managing-clusters/#using-config-files
# https://eksctl.io/usage/eks-private-cluster
cat > /tmp/eksctl-cluster.yaml  <<EOF
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: ${EKS_CLUSTER_NAME}
  region: ${AWS_REGION}
vpc:
  subnets:
    private:
      ${AWS_REGION}a: { id: subnet-0ff156e0c4a6d300c }
      ${AWS_REGION}b: { id: subnet-0549cdab573695c03 }
      ${AWS_REGION}c: { id: subnet-0426fb4a607393184 }
privateCluster:
  enabled: true
nodeGroups:
  - name: ng-1-workers
    labels: { role: workers }
    instanceType: m5.xlarge
    desiredCapacity: 10
    privateNetworking: true
  - name: ng-2-builders
    labels: { role: builders }
    instanceType: m5.2xlarge
    desiredCapacity: 3
    privateNetworking: true
    iam:
      withAddonPolicies:  
        imageBuilder: true
EOF
eksctl create cluster -f /tmp/eksctl-cluster.yaml
# eksctl delete cluster -f /tmp/eksctl-cluster.yaml
```

## List Clusters

```bash
eksctl get clusters
```

```bash
aws eks list-clusters --region ${AWS_REGION} && \
  eksctl get clusters --region ${AWS_REGION}
```

```bash
aws eks \
  describe-cluster \
  --region ${AWS_REGION} \
  --name ${EKS_CLUSTER_NAME}
```

## Node Group

```bash
eksctl create nodegroup \
  --nodes-min 0 \
  --nodes 0 \
  --nodes-max 100 \
  --name ${EKS_NODE_GROUP_NAME} \
  --cluster ${EKS_CLUSTER_NAME} \
  --region ${AWS_REGION}
```

```bash
eksctl get nodegroups \
  --cluster $EKS_CLUSTER_NAME
```

## Scale Cluster

- https://docs.aws.amazon.com/eks/latest/userguide/update-stack.html
- https://docs.aws.amazon.com/eks/latest/userguide/update-managed-node-group.html

```bash
# Get node group details.
EKS_CLUSTER_DETAILS=$(eksctl get nodegroup --cluster $EKS_CLUSTER_NAME | grep $EKS_CLUSTER_NAME)
echo $EKS_CLUSTER_DETAILS
EKS_NODE_GROUP_NAME=$(cut -d ' ' -f2 <<<${EKS_CLUSTER_DETAILS})
echo $EKS_NODE_GROUP_NAME
```

```bash
# Describe node group.
eksctl get nodegroup \
  --cluster ${EKS_CLUSTER_NAME} \
  --name ${EKS_NODE_GROUP_NAME}
```

```bash
# Scale up node group.
eksctl scale nodegroup \
  --nodes 3 \
  --cluster ${EKS_CLUSTER_NAME} \
  --name ${EKS_NODE_GROUP_NAME}
```

```bash
# Scale down node group.
eksctl scale nodegroup \
  --nodes 0 \
  --cluster ${EKS_CLUSTER_NAME} \
  --name ${EKS_NODE_GROUP_NAME}
```

## Kubeconfig

- Create a Kubeconfig for Amazon EKS https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html

```bash
# Update your local kubeconfig.
aws eks \
  update-kubeconfig \
  --region $AWS_REGION \
  --name $EKS_CLUSTER_NAME
```

```bash
kubectl config get-contexts
```

```bash
kubectl config \
  use-context arn:aws:eks:$AWS_REGION:...:cluster/$EKS_CLUSTER_NAME
```

```bash
# Get context details.
kubectl config get-contexts && \
  kubectl config current-context
```

## Console Access

- https://aws.amazon.com/premiumsupport/knowledge-center/eks-kubernetes-object-access-error
- https://varlogdiego.com/eks-your-current-user-or-role-does-not-have-access-to-kubernetes

```bash
kubectl edit configmap aws-auth -n kube-system
```

```yaml
  mapUsers: |
    - userarn: arn:aws:iam::773842031886:user/datalayer-1
      username: datalayer-1
      groups:
      - system:masters
```

## [OPTIONAL] IAM Roles for Service Accounts

- https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html
- https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts-technical-overview.html#pod-configuration

- https://aws.amazon.com/blogs/containers/cross-account-iam-roles-for-kubernetes-service-accounts
- https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html

- https://aws.amazon.com/premiumsupport/knowledge-center/eks-restrict-s3-bucket

- EKS IAM Roles for Pods https://github.com/aws/containers-roadmap/issues/23

```bash
# Create an IAM OIDC provider for your cluster https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html
aws eks describe-cluster \
  --region $AWS_REGION \
  --name $EKS_CLUSTER_NAME \
  --query "cluster.identity.oidc.issuer" \
  --output text
eksctl utils associate-iam-oidc-provider \
  --region $AWS_REGION \
  --name $EKS_CLUSTER_NAME \
  --approve
aws iam list-open-id-connect-providers | grep 9812255A59F51E22DBFC6FE889B2103C
eksctl utils associate-iam-oidc-provider --cluster $EKS_CLUSTER_NAME --approve
aws iam list-open-id-connect-providers | grep 9812255A59F51E22DBFC6FE889B2103C
```

```bash
# Creating an IAM role and policy for your service account https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html
# TODO Remove `DatalayerEksS3DatalayerDev` policy if created before.
aws iam delete-policy --policy-arn $IAM_POLICY_ARN
OUT=$(aws iam create-policy \
  --policy-name DatalayerEksS3DatalayerBackups \
  --description "Datalayer S3 Backups" \
  --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "putget",
      "Effect": "Allow",
      "Action": [
          "s3:PutObject",
          "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::datalayer-backups-solr/*"
    },
    {
      "Sid": "list",
      "Effect": "Allow",
      "Action": [
          "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::datalayer-backups-solr"
    }
  ]
}
')
echo $OUT
IAM_POLICY_ARN=$(echo $OUT | jq -r '.Policy.Arn')
echo $IAM_POLICY_ARN
# IAM_POLICY_ARN=arn:aws:iam::${AWS_ACCOUNT_ID}:policy/DatalayerEksS3DatalayerBackups
# echo $IAM_POLICY_ARN
eksctl create iamserviceaccount \
  --name datalayer-s3-backups \
  --namespace default \
  --cluster $EKS_CLUSTER_NAME \
  --attach-policy-arn $IAM_POLICY_ARN \
  --override-existing-serviceaccounts \
  --approve
kubectl describe sa datalayer-s3-backups -n default
# aws iam list-roles --path-prefix /${EKS_CLUSTER_NAME} --output text
# IAM_SA=$(aws iam list-roles --output text | grep $EKS_CLUSTER_NAME | grep iamserviceaccount)
# echo $IAM_SA
# IAM_SA_ROLE_ARN=$(echo $IAM_SA | tr -s ' ' | cut -d' ' -f2)
# echo $IAM_SA_ROLE_ARN
```

```bash
# Connect to meta-data.
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: s3-demo
  labels:
    purpose: demonstrate-s3
spec:
  serviceAccountName: datalayer-s3-backups
  containers:
  - name: s3-demo
    image: gcr.io/google-samples/node-hello:1.0
    env:
    - name: DEMO_GREETING
      value: "Hello from the environment"
EOF
kubectl describe pod s3-demo
kubectl exec s3-demo -i -t -- bash
curl http://169.254.169.254/latest/meta-data/iam/info
curl http://169.254.169.254/latest/meta-data/iam/security-credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/$(curl http://169.254.169.254/latest/meta-data/iam/security-credentials)
exit
kubectl delete pod s3-demo
```

```bash
# Connect to S3.
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: aws-cli
  labels:
    name: aws-cli
spec:
  serviceAccountName: datalayer-s3-backups
  containers:
  - image: amazon/aws-cli
    command:
      - "sh"
      - "-c"
      - "sleep 10000"
#      - "/home/aws/aws/env/bin/aws"
#      - "s3"
#      - "ls"
    name: aws-cli
EOF
kubectl describe pod aws-cli
kubectl exec aws-cli -i -t -- bash
curl http://169.254.169.254/latest/meta-data/iam/info
curl http://169.254.169.254/latest/meta-data/iam/security-credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/$(curl http://169.254.169.254/latest/meta-data/iam/security-credentials)
aws s3 ls
aws s3 ls s3://datalayer-backups-solr
touch tmp.txt
aws s3 cp tmp.txt s3://datalayer-backups-solr/tmp.txt
aws s3 ls s3://datalayer-backups-solr/tmp.txt
aws s3 ls s3://datalayer-backups-solr/
aws s3 rm s3://datalayer-backups-solr/tmp.txt
aws s3 ls s3://datalayer-backups-solr/
exit
kubectl delete pod aws-cli
```

## Sanity Check

```bash
# sanity check 1.
kubectl get nodes && \
  kubectl get pods -A
```

```bash
# sanity check 2.
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: envar-demo
  labels:
    purpose: demonstrate-envars
spec:
  containers:
  - name: envar-demo-container
    image: gcr.io/google-samples/node-hello:1.0
    env:
    - name: DEMO_GREETING
      value: "Hello from the environment"
EOF
kubectl get pods -n default
# kubectl exec envar-demo -n default -i -t -- echo $DEMO_GREETING
kubectl exec envar-demo -n default -i -t -- bash
# echo $DEMO_GREETING
# exit
kubectl delete pod envar-demo -n default
```

```bash
# sanity check 3.
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
EOF
kubectl get pods -n default
kubectl delete deployment nginx-deployment -n default
```

```bash
# sanity check 4.
kubectl create deployment hostnames --image=k8s.gcr.io/serve_hostname
kubectl scale deployment hostnames --replicas=3
kubectl get pods -l app=hostnames
kubectl get pods -l app=hostnames -o go-template='{{range .items}}{{.status.podIP}}{{"\n"}}{{end}}'
kubectl expose deployment hostnames --port=80 --target-port=9376
kubectl get svc hostnames
kubectl get service hostnames -o json
kubectl get pods -l app=hostnames
kubectl cluster-info
kubectl proxy --port=8081
curl http://localhost:8081/api
open http://127.0.0.1:8081/api/v1/namespaces/default/services/http:hostnames:/proxy
kubectl delete deployment hostnames
```

```bash
# sanity check 5.
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx # has to match .spec.template.metadata.labels
  serviceName: "nginx"
  replicas: 3 # by default is 1
  template:
    metadata:
      labels:
        app: nginx # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: k8s.gcr.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
#        volumeMounts:
#        - name: www
#          mountPath: /usr/share/nginx/html
#  volumeClaimTemplates:
#  - metadata:
#      name: www
#    spec:
#      accessModes: [ "ReadWriteOnce" ]
#      storageClassName: "my-storage-class"
#      resources:
#        requests:
#          storage: 1Gi
EOF
kubectl get pods -n default
kubectl get svc -n default
kubectl port-forward service/nginx 8080:80 -n default
open http://localhost:8080
```

## Secrets

```bash
kubectl create secret generic aws-creds \
  --from-literal=access-key-id=$AWS_ACCESS_KEY_ID \
  --from-literal=secret-access-key=$AWS_SECRET_ACCESS_KEY \
  --namespace=default
kubectl describe secret aws-creds
```

## K8S Dashboard

- K8S Dashboard on EKS https://docs.aws.amazon.com/eks/latest/userguide/dashboard-tutorial.html

```bash
## Metrics Server.
# kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml
# kubectl get deployment metrics-server -n kube-system
## [DEPRECATED] Metrics Server.
# DOWNLOAD_URL=$(curl -Ls "https://api.github.com/repos/kubernetes-sigs/metrics-server/releases/latest" | jq -r .tarball_url)
# DOWNLOAD_VERSION=$(grep -o '[^/v]*$' <<< $DOWNLOAD_URL)
# curl -Ls $DOWNLOAD_URL -o metrics-server-$DOWNLOAD_VERSION.tar.gz
# mkdir metrics-server-$DOWNLOAD_VERSION
# tar -xzf metrics-server-$DOWNLOAD_VERSION.tar.gz --directory metrics-server-$DOWNLOAD_VERSION --strip-components 1
# kubectl apply -f metrics-server-$DOWNLOAD_VERSION/deploy/1.8+/
# kubectl get deployment metrics-server -n kube-system
# rm -fr metrics-server*
```

```bash
## K8S Dashboard.
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eks-admin
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: eks-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: eks-admin
  namespace: kube-system
EOF
```

```bash
# Connect to K8S Dashboard.
dla eks-dashboard
# Connect to K8S Dashboard.
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep eks-admin | awk '{print $1}')
echo open http://localhost:8081/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy
kubectl proxy --port 8081
```

## Ingress Nginx

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
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
```

Check the external IP address provided by the `ingress-nginx-controller` Load Balancer.
Create a DNS A record mapping the hostname used in the Ingress to the resolved IP address (run ping ...elb.amazonaws.com to get that IP).
Better: create a CNAME mapping to the ...elb.amazonaws.com hostname for:

- $DATALAYER_RUN
- simple-dev.datalayer.community
- simple-echo.dev.datalayer.run

```bash
kubectl get svc ingress-nginx-controller -n ingress-nginx
# NAME                       TYPE           CLUSTER-IP       EXTERNAL-IP                                                              PORT(S)                      AGE
# ingress-nginx-controller   LoadBalancer   10.100.113.174   ...-614799374.us-east-1.elb.amazonaws.com   80:32664/TCP,443:32671/TCP   11m
```

```bash
# Create a DNS A record:
# - Alias to  ...-614799374.us-east-1.elb.amazonaws.com
# - or... resolve to IP address.
nslookup ...-614799374.us-east-1.elb.amazonaws.com
```

## Certificate Manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install \
  cert-manager \
  jetstack/cert-manager \
  --version v1.4.3 \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
helm ls -n cert-manager
kubectl get pods -n cert-manager
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1alpha2
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
dla up eks datalayer-simple
helm ls -A
kubectl get pods -n datalayer-simple
kubectl get secrets -n datalayer-simple
kubectl describe secrets -n datalayer-simple simple-secret
POD_NAME=$(kubectl get pods -n datalayer-simple -l "app=simple-echo-2" -o jsonpath="{.items[0].metadata.name}")
echo $POD_NAME
kubectl exec $POD_NAME -n datalayer-simple -i -t -- echo $DATALAYER_LDAP_BIND_PWD
kubectl exec $POD_NAME -n datalayer-simple -i -t -- /bin/bash
kubectl get certificates -n datalayer-simple
kubectl describe certificate simple-datalayer-run-cert -n datalayer-simple
kubectl describe certificaterequest -n datalayer-simple simple-datalayer-run-cert-s5ph...
curl https://simple-dev.datalayer.community/info
# {"version": "0.0.3", "host": "simple-dev.datalayer.community", "from": "10.44.0.2", "local_hostname": "simple-64c4fd859f-p9w74", "local_ip": "10.44.0.6", "headers": [{"Host": "simple-dev.datalayer.community"}, {"X-Request-Id": "f76ad6945e9ebc3ba9ea8da3a6ea2adb"}, {"X-Real-Ip": "10.44.0.0"}, {"X-Forwarded-For": "10.44.0.0"}, {"X-Forwarded-Host": "simple-dev.datalayer.community"}, {"X-Forwarded-Port": "443"}, {"X-Forwarded-Proto": "https"}, {"X-Forwarded-Scheme": "https"}, {"X-Scheme": "https"}, {"User-Agent": "curl/7.64.1"}, {"Accept": "*/*"}]}
curl https://simple-echo.dev.datalayer.run/simple-echo
# hello simple-echo
dla down datalayer-simple
```

## Solr

```bash
# dla up eks datalayer-solr
# Wait for pods to be up.
# kubectl get pods -n datalayer-solr
```

```bash
# Install the solr & zookeeper crds.
kubectl create -f https://solr.apache.org/operator/downloads/crds/v0.5.1/all-with-dependencies.yaml
# Install the solr operator and zookeeper operator.
# https://artifacthub.io/packages/helm/apache-solr/solr-operator
helm upgrade --install solr-operator \
  apache-solr/solr-operator \
  --version 0.5.1
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
#
kubectl apply -f $DATALAYER_HOME/etc/operator/solr/datalayer.yaml
kubectl get solrclouds -w
```

```bash
# Terminal 1.
cd $DATALAYER_HOME/src && \
  make pf-solr
```

```bash
export SOLR_HOME=$DATALAYER_HOME/opt/solr
export DAO_FOLDER=$DATALAYER_HOME/src/platforms/datalayer/studio/services/dao/examples/model
```

```bash
# Terminal 2.
# Create the collections.
$SOLR_HOME/bin/solr create -c credits -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/credits -p 8983
$SOLR_HOME/bin/solr create -c invites -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/invites -p 8983
$SOLR_HOME/bin/solr create -c organisations -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/organisations -p 8983 -force
$SOLR_HOME/bin/solr create -c users -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/users -p 8983 -force
$SOLR_HOME/bin/solr create -c spaces -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/spaces -p 8983
$SOLR_HOME/bin/solr create -c tweets -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/tweets -p 8983
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
kubectl scale --replicas=5 solrcloud/solr-datalayer
```

```bash
kubectl delete -f $DATALAYER_HOME/etc/operator/solr/datalayer.yaml
kubectl delete solrcloud solr-datalayer
helm delete solr-datalayer
helm delete solr-operator
kubectl delete -f \
  https://solr.apache.org/operator/downloads/crds/v0.5.1/all-with-dependencies.yaml
```

Solr Backups

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
#
kubectl describe solrbackups
kubectl get solrbackups -w
aws s3 ls s3://datalayer-backups-solr/datalayer-solr-collection-backup-accounts/accounts/
curl http://localhost:8983/solr/accounts/replication?command=details
#
# Stop recurring backups.
kubectl delete -f $DATALAYER_HOME/etc/operator/solr/datalayer-backup-s3.yaml
#
# Delete and re-create empty collection.
curl http://localhost:8983/solr/USER_RESTORED_COLL/update?commitWithin=500 -d '{ delete: { query: "*:*" } }'
curl http://localhost:8983/solr/admin/collections?action=DELETE -d 'name=USER_RESTORED_COLL'
export SOLR_HOME=$DATALAYER_HOME/opt/solr && \
  $SOLR_HOME/bin/solr create -c USER_RESTORED_COLL -shards 3 -replicationFactor 3 -d $DATALAYER_HOME/etc/solr/users -p 8983 -force
#
# Restore https://solr.apache.org/guide/8_11/collection-management.html#restore
# backupId=10&
curl http://localhost:8983/solr/admin/collections -d '
action=RESTORE&
repository=s3&
collection=USER_RESTORED_COLL&
backupId=12&
location=s3:/&
name=datalayer-solr-collection-backup-users'
#
curl http://localhost:8983/solr/USER_RESTORED_COLL/select?q=*:*
curl http://localhost:8983/solr/USER_RESTORED_COLL/update?commitWithin=500 -d '{ delete: { query: "*:*" } }'
```

## Cassandra

```bash
# https://docs.k8ssandra.io/install/eks
helm repo add k8ssandra https://helm.k8ssandra.io
helm repo update
# kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
# kubectl get storageclasses | grep rancher
```

```bash
# Backup https://docs.k8ssandra.io/tasks/backup-restore/amazon-s3
curl -o medusa-bucket-key.yaml \
  https://docs.k8ssandra.io/tasks/backup-restore/amazon-s3/medusa-bucket-key.yaml
# update medusa-bucket-key.yaml with creds.
kubectl apply -f medusa-bucket-key.yaml
# kubectl create secret generic k8ssandra-medusa-key
kubectl describe secret medusa-bucket-key
```

```bash
helm upgrade --install \
  -f $DATALAYER_HOME/etc/cassandra-operator/k8ssandra-eks.yaml \
  cassandra-datalayer \
  k8ssandra/k8ssandra
kubectl get cassandradatacenters
kubectl describe cassandradatacenter dc-datalayer | grep "Cassandra Operator Progress:"
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
# Cassandra stargate graphql.
# https://stargate.io/docs/stargate/1.0/quickstart/quick_start-graphql.html
```

```bash
# https://docs.datastax.com/en/developer/python-driver/3.10
pip install cassandra-driver
python3 <<EOF
from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect('k8ssandra_test')
rows = session.execute('SELECT * FROM users')
for r in rows:
    print(r.email, r.name, r.state)
EOF
```

```bash
# https://github.com/datastax/astrapy
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
res = stargate_client.rest.search_table(keyspace='k8ssandra_test',
                                     table='users',
                                     query={"email": {"$eq": "alice@example.com"}})
print(res["count"]) # number of results
print(res["data"]) # list of rows
EOF
```

```bash
# Backup / Restore https://docs.k8ssandra.io/tasks/backup-restore/amazon-s3
helm install dc-datalayer-backup k8ssandra/backup --set name=dc-datalayer-backup,cassandraDatacenter.name=dc-datalayer
kubectl get cassandrabackup
kubectl get cassandrabackup dc-datalayer-backup -o yaml
helm delete dc-datalayer-backup
helm install restore-test k8ssandra/restore --set name=restore-test,backup.name=dc-datalayer-backup,cassandraDatacenter.name=dc-datalayer
kubectl get cassandrarestore restore-test -o yaml
kubectl logs cassandra-datalayer-dc-datalayer-us-east-1a-sts-0 -c medusa-restore
kubectl exec -it cassandra-datalayer-dc-datalayer-us-east-1a-sts-0 -c cassandra -- cqlsh -u $K8SSANDRA_USERNAME -p $K8SSANDRA_PASSWORD
USE k8ssandra_test;
SELECT * from users;
kubectl get cassandrarestore helm-test -o yaml
```

```bash
kubectl delete cassandradatacenter dc-datalayer
helm delete cassandra-datalayer
```

## Redis

```bash
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

## Deploy

```bash
kubectl config use-context arn:aws:eks:us-east-1:773842031886:cluster/datalayer-io
cd $DATALAYER_HOME/etc/docker/platforms/datalayer/studio/auth && make build push && \
  dla down datalayer-auth && dla up eks datalayer-auth
cd $DATALAYER_HOME/etc/docker/platforms/datalayer/studio/library && make build push && \
  dla down datalayer-library && dla up eks datalayer-library
kubectl config use-context minikube
```

```bash
$DATALAYER_HOME/src/platforms/datalayer/studio/dev/deploy/all.sh
open $DATALAYER_HOME/src/platforms/datalayer/studio/dist/report.html
```

```bash
kubectl config use-context arn:aws:eks:us-east-1:773842031886:cluster/datalayer-io
cd $DATALAYER_HOME/etc/docker/tech/jupyterpool && make build push
dla down jupyterpool && dla up eks jupyterpool
kubectl config use-context minikube
```

## Auth

```bash
cd $DATALAYER_HOME/etc/docker/platforms/datalayer/studio/auth && make build push
dla down datalayer-auth && dla up eks datalayer-auth
#
dla up eks datalayer-auth
kubectl get pods -n datalayer
kubectl describe certificate $DATALAYER_RUN-auth-cert-secret -n datalayer
open https://${DATALAYER_RUN}/api/auth/version
# open https://${DATALAYER_RUN}/api/auth/profile
```

## Library

```bash
cd $DATALAYER_HOME/etc/docker/platforms/datalayer/studio/library && make build push
dla down datalayer-library && dla up eks datalayer-library
#
dla up eks datalayer-library
kubectl get pods -n datalayer
kubectl describe certificate $DATALAYER_RUN-library-cert-secret -n datalayer
open https://${DATALAYER_RUN}/api/library/version
open https://${DATALAYER_RUN}/api/library/tells/published
```

## Jupyterpool

```bash
cd $DATALAYER_HOME/etc/docker/tech/jupyterpool && make build push
dla down jupyterpool && dla up eks jupyterpool
#
dla up eks jupyterpool
kubectl get pods -n datalayer
kubectl describe certificate $DATALAYER_RUN-jupyterpool-cert-secret -n datalayer
open https://${DATALAYER_RUN}/api/jupyter/pool/default
open https://${DATALAYER_RUN}/api/jupyter/lab?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
```

```bash
dla down jupyterpool
```

## User Interface

```bash
# Build and deploy javascript.
$DATALAYER_HOME/src/platforms/datalayer/studio/dev/deploy/all.sh
open $DATALAYER_HOME/src/platforms/datalayer/studio/dist/report.html
```

## Sanity Check

```bash
open ${DATALAYER_CDN}
```

```bash
curl https://${DATALAYER_RUN}
open https://${DATALAYER_RUN}
curl http://${DATALAYER_RUN}
open http://${DATALAYER_RUN}
```

```bash
curl https://${DATALAYER_RUN}/api/jupyter/lab
curl https:/${DATALAYER_RUN}/api/jupyter/pool/default
open https://${DATALAYER_RUN}/api/jupyter/lab
open https://${DATALAYER_RUN}/api/jupyter/pool/default
```

## JupyterHub

- https://zero-to-jupyterhub.readthedocs.io/en/latest/amazon/step-zero-aws.html
- https://zero-to-jupyterhub.readthedocs.io/en/latest/amazon/step-zero-aws-eks.html
- https://github.com/parente/z2jh-aws

## Spark

```bash
# Install Spark locally.
aws s3 cp s3://.../dist/spark-3.0.0-bin-hadoop-3.2.1.tgz .
tar xfz spark-3.0.0-bin-hadoop-3.2.1.tgz
cd spark-3.0.0-bin-hadoop-3.2.1
# Define in your bash profile SPARK_HOME to point to that folder
# so that SPARK_HOME will be correctly defined for your next shell session. 
export SPARK_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
```

Use one of the following Docker images.

- datalayer/spark-aws:3.0.0
- 34268218.dkr.ecr.us-east-1.amazonaws.com/spark-aws-dev:3.0.0

```bash
# Service Account.
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: spark-role
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: edit
subjects:
  - kind: ServiceAccount
    name: spark
    namespace: default
EOF
```

```bash
# Spark in a Pod.
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: spark-shell
  labels:
    name: spark-shell
spec:
  containers:
  - image: datalayer/spark-aws:3.0.0
    imagePullPolicy: IfNotPresent
    command:
      - "sh"
      - "-c"
      - "sleep 10000"
    name: spark-shell
EOF
kubectl exec spark-shell -i -t -- bash
export PYSPARK_DRIVER_PYTHON=/usr/bin/python3
/opt/spark/bin/pyspark \
  --master k8s://https://kubernetes \
  --name pyspark-shell \
  --conf spark.executor.instances=3 \
  --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider \
  --conf spark.kubernetes.container.image=datalayer/spark-aws:3.0.0 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.container.image.pullPolicy=IfNotPresent \
  --conf spark.kubernetes.driver.pod.name=spark-shell
exit
kubectl delete pod spark-shell
```

Spark Examples

```bash
export SPARK_EXAMPLES_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $SPARK_EXAMPLES_HOME
```

```bash
# If the local proxy is running at localhost:8001, --master k8s://http://127.0.0.1:8001 can be used as the argument to spark-submit.
# or use kubectl cluster-info
kubectl proxy
```

```bash
kubectl get pods -w
```

```bash
$SPARK_EXAMPLES_HOME/bin/spark-pi.sh
kubectl get logs spark-pi-... -f
kubectl get logs spark-pi-... | grep "Pi is roughly"
```

```bash
$SPARK_EXAMPLES_HOME/bin/pyspark-simple-df.sh
kubectl get logs spark-pi-... -f
kubectl get logs spark-pi-... | grep value
```

```bash
aws s3 rm --recursive s3://.../hello-demo.csv
aws s3 rm --recursive s3://.../hello-demo.parquet
aws s3 ls s3://.../
$SPARK_EXAMPLES_HOME/bin/pyspark-hello-s3.sh
kubectl get logs spark-... -f
aws s3 ls s3://.../hello-demo.csv/
aws s3 ls s3://.../hello-demo.parquet/
```

STS with PySpark

- https://medium.com/@leythg/access-s3-using-pyspark-by-assuming-an-aws-role-9558dbef0b9e
- https://medium.com/@aman.ranjanverma/running-pyspark-on-eks-fargate-part-3-last-e314b915d60e

```bash
aws s3 rm --recursive s3://.../....parquet/
aws s3 ls s3://.../
$SPARK_EXAMPLES_HOME/bin/pyspark-hello-eubi.sh
aws s3 ls s3://.../
aws s3 ls s3://.../....parquet/
```

Spark Operator

- https://github.com/GoogleCloudPlatform/spark-on-k8s-operator

```bash
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install --name sparkoperator incubator/sparkoperator --namespace default --set sparkJobNamespace=default
# --set enableWebhook=true
# --set enableMetrics=false
helm ls -A
helm status sparkoperator
kubectl get pods -n default
```

```bash
helm delete sparkoperator --purge
```

```bash
cd spark-operator/spark-docker
```

```bash
kubectl apply -f ./spark-operator/examples/spark-pi.yaml
kubectl get pods -n default -w
```

```bash
kubectl get sparkapplications spark-pi -o=yaml
kubectl get pods -n default -w
```

```bash
kubectl describe sparkapplication spark-pi
```

AWS Sample

```bash
# https://github.com/aws-samples/amazon-eks-apache-spark-etl-sample.git
# https://aws.amazon.com/blogs/opensource/deploying-spark-jobs-on-amazon-eks
cd spark-eks
docker build --target=spark -t datalayer/spark:v2.4.4 .
docker build -t datalayer/spark-on-eks:v1.0 .
kubectl apply -f example/kubernetes/spark-rbac.yaml
kubectl apply -f example/kubernetes/spark-job.yaml
```

## Airflow

```bash
# https://github.com/airflow-helm/charts/tree/main/charts/airflow
helm repo add airflow-stable https://airflow-helm.github.io/charts
helm repo update
helm upgrade \
  --install airflow \
  airflow-stable/airflow \
  --namespace airflow \
  --values ./etc/helm/airflow/values.yaml
helm ls -A
kubectl get pods -n airflow
kubectl get svc -n airflow
kubectl port-forward service/airflow-web 8080:8080 -n airflow
open http://localhost:8080
```

```bash
helm delete airflow --purge
```

## Autoscaler

- https://eksworkshop.com/scaling/deploy_ca
- https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler

## Custom AMI

- https://github.com/awslabs/amazon-eks-ami

## Private Cluster

- https://docs.aws.amazon.com/eks/latest/userguide/private-clusters.html
- https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html
- https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html#private-access

- https://eksctl.io/usage/eks-private-cluster

- https://medium.com/faun/amazon-eks-fully-private-worker-nodes-eea737944b2b
- https://github.com/sebolabs/k8s-eks-tf-playground

In addition to standard Amazon EKS permissions, your IAM user or role must have `route53:AssociateVPCWithHostedZone` permissions to enable the cluster's endpoint private access.

Accessing a private only API server If you have disabled public access for your cluster's Kubernetes API server endpoint, you can only access the API server from within your VPC or a connected network. Here are a few possible ways to access the Kubernetes API server endpoint:

- Connected network – Connect your network to the VPC with an AWS transit gateway or other connectivity option and then use a computer in the connected network. You must ensure that your Amazon EKS control plane security group contains rules to allow ingress traffic on `port 443` from your connected network.
- Amazon EC2 bastion host – You can launch an Amazon EC2 instance into a public subnet in your cluster's VPC and then log in via SSH into that instance to run kubectl commands. For more information, see Linux bastion hosts on AWS. You must ensure that your Amazon EKS control plane security group contains rules to allow ingress traffic on port 443 from your bastion host. For more information, see Amazon EKS security group considerations. When you configure kubectl for your bastion host, be sure to use AWS credentials that are already mapped to your cluster's RBAC configuration, or add the IAM user or role that your bastion will use to the RBAC configuration before you remove endpoint public access. For more information, see Managing users or IAM roles for your cluster and Unauthorized or access denied (kubectl).
- AWS Cloud9 IDE – AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a browser. You can create an AWS Cloud9 IDE in your cluster's VPC and use the IDE to communicate with your cluster. For more information, see Creating an environment in AWS Cloud9. You must ensure that your Amazon EKS control plane security group contains rules to allow ingress traffic on port 443 from your IDE security group. For more information, see Amazon EKS security group considerations. When you configure kubectl for your AWS Cloud9 IDE, be sure to use AWS credentials that are already mapped to your cluster's RBAC configuration, or add the IAM user or role that your IDE will use to the RBAC configuration before you remove endpoint public access. For more information, see Managing users or IAM roles for your cluster and Unauthorized or access denied (kubectl).

## Terminate Cluster

```bash
# !!! WATCH OUT !!!
# !!! EVERYTHING WILL BE DESTROYED *AND* LOST... !!!
eksctl delete cluster \
  --force \
  --region $AWS_REGION \
  --name $EKS_CLUSTER_NAME
```

## [OPTIONAL] Prepare a VPC

- Eksctl VPC Networking https://eksctl.io/usage/vpc-networking

- You must ensure to provide at least 2 subnets in different AZs.
- There are other requirements that you will need to follow, but it's entirely up to you to address those.
- For example, tagging is not strictly necessary, tests have shown that its possible to create a functional cluster without any tags set on the subnets, however there is no guarantee that this will always hold and tagging is recommended.

- All subnets in the same VPC, within the same block of IPs.
- Sufficient IP addresses are available.
- Sufficient number of subnets (minimum 2).
- Internet and/or NAT gateways are configured correctly.
- Routing tables have correct entries and the network is functional.
- Tagging of subnets:
  - `kubernetes.io/cluster/<name>` tag set to either shared or owned
  - `kubernetes.io/role/internal-elb` tag set to 1 for private subnets

## [OPTIONAL] Create a Cluster via the AWS Console

- https://docs.aws.amazon.com/eks/latest/userguide/getting-started-console.html#eks-prereqs

- name: ``
- version: `1.16`
- role: ``
- vpc: ``
- subnets:
  - subnet-1: `` - 10....132.0/27 Dev Subnet 3.1 us-east-1a (25 IP Addresses available)
  - subnet-2: `` - 10....132.32/27 Dev Subnet 3.2 us-east-1b (25 IP Addresses available)
  - subnet-3: `` - 10....132.64/27 Dev Subnet 3.3 us-east-1c (25 IP Addresses available)
- visibility:
  - public
  - private
- source-whitelist: `87.67.111.0/24`
- node group: `` 
  - role: ``
  - size: 0, 10, 3

## [DEPRECATED] NGinx Ingress Example

```bash
"""
# kubectl apply -f https://raw.githubusercontent.com/cornellanthony/nlb-nginxIngress-eks/master/apple.yaml
# kubectl apply -f https://raw.githubusercontent.com/cornellanthony/nlb-nginxIngress-eks/master/banana.yaml
Do not apply the 2 above, apply the following.
"""
cat <<EOF | kubectl apply -f -
kind: Pod
apiVersion: v1
metadata:
  name: apple-app
  labels:
    app: apple
spec:
  containers:
    - name: apple-app
      image: hashicorp/http-echo
      args:
        - "-text=apple"
---
kind: Service
apiVersion: v1
metadata:
  name: apple-service
spec:
  selector:
    app: apple
  ports:
    - port: 5678 # Default port for image	
---
kind: Pod
apiVersion: v1
metadata:
  name: banana-app
  labels:
    app: banana
spec:
  containers:
    - name: banana-app
      image: hashicorp/http-echo
      args:
        - "-text=banana"
---
kind: Service
apiVersion: v1
metadata:
  name: banana-service
spec:
  selector:
    app: banana
  ports:
    - port: 5678 # Default port for image
EOF
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: fruits-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/rewrite-target: "/"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    cert-manager.io/acme-challenge-type: "http01"
spec:
  tls:
  - hosts:
    - fruits.datalayer.io
    secretName: fruits-datalayer-io-cert
  rules:
  - host: fruits.datalayer.io
    http:
      paths:
        - path: /apple
          backend:
            serviceName: apple-service  
            servicePort: 5678
        - path: /banana
          backend:
            serviceName: banana-service
            servicePort: 5678
EOF
kubectl describe cert fruits-datalayer-io-cert
```

```bash
curl https://fruits.datalayer.io/apple
curl https://fruits.datalayer.io/appleeee
curl https://fruits.datalayer.io/banana
curl https://fruits.datalayer.io/lemon
curl http://fruits.datalayer.io/apple
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: lemon-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/rewrite-target: "/"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    cert-manager.io/acme-challenge-type: "http01"
spec:
  tls:
  - hosts:
    - lemon.datalayer.io
    secretName: lemon-datalayer-io-cert
  rules:
  - host: lemon.datalayer.io
    http:
      paths:
        - path: /
          backend:
            serviceName: apple-service  
            servicePort: 5678
EOF
kubectl describe cert lemon-datalayer-io-cert
```

```bash
curl https://lemon.datalayer.io
```

## [DEPRECATED] LoadBalancer Service

```bash
cat <<EOF | kubectl apply -f -
kind: Pod
apiVersion: v1
metadata:
  name: lemon-app
  labels:
    app: lemon
spec:
  containers:
    - name: lemon-app
      image: hashicorp/http-echo
      args:
        - "-text=lemon"
---
kind: Service
apiVersion: v1
metadata:
  name: lemon-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: http
    external-dns.alpha.kubernetes.io/hostname: lemon.dev.datalayer.io
  #    external-dns.alpha.kubernetes.io/ttl: 60
spec:
  type: LoadBalancer
  selector:
    app: lemon
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 5678 # Default port for image
EOF
```

## [DEPRECATED] NGinx Ingress Helm Chart

```bash
# https://github.com/helm/charts/tree/master/stable/nginx-ingress
cat <<EOF >/tmp/nginx-ingress.yml
rbac:
  create: true
controller:
  service:
#    type: LoadBalancer
    targetPorts:
      http: http
      https: https
    annotations:
#      nginx.ingress.kubernetes.io/ssl-redirect: 'true'
#      nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
#      service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:XX-XXXX-X:XXXXXXXXX:certificate/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXX
#      service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
#      service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "https"
      service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: '3600'
      external-dns.alpha.kubernetes.io/hostname: datalayer.io.
EOF
helm install \
  --name nginx-ingress \
  --values /tmp/nginx-ingress.yml \
  stable/nginx-ingress
```

```bash
helm delete nginx-ingress --purge
```

## [LATER] ALB Ingress

```bash
OUT=$(aws iam create-policy \
  --policy-name ALBIngressControllerIAMPolicy \
  --policy-document https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/iam-policy.json)
echo $OUT
IAM_POLICY_ARN=$(echo $OUT | jq -r '.Policy.Arn')
echo $IAM_POLICY_ARN
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/rbac-role.yaml
eksctl create iamserviceaccount \
    --name alb-ingress-controller \
    --namespace kube-system \
    --cluster $EKS_CLUSTER_NAME \
    --attach-policy-arn $IAM_POLICY_ARN \
    --override-existing-serviceaccounts \
    --approve
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/alb-ingress-controller.yaml
kubectl edit deployment.apps/alb-ingress-controller -n kube-system
# add to the args
#        - --cluster-name=...
#        - --aws-vpc-id=vpc-...
#        - --aws-region=us-west-2
kubectl get pods -n kube-system | grep alb
```

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-service.yaml
```

```bash
# kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/2048/2048-ingress.yaml
cat <<EOF | kubectl apply -f -
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: "2048-ingress"
  namespace: "2048-game"
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
  labels:
    app: 2048-ingress
spec:
  rules:
    - http:
        paths:
          - path: /
            backend:
              serviceName: "service-2048"
              servicePort: 80
EOF
```

## [DEPRECATED] ALB Ingress Helm Chart

```bash
# https://docs.aws.amazon.com/eks/latest/userguide/alb-ingress.html
# https://eksworkshop.com/beginner/130_exposing-service/ingress_controller_alb/
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install \
  incubator/aws-alb-ingress-controller \
  --set clusterName=$EKS_CLUSTER_NAME \
  --set autoDiscoverAwsRegion=true \
  --set autoDiscoverAwsVpcID=true \
  --name aws-alb-ingress-controller \
  --namespace kube-system
```

```bash
helm delete aws-alb-ingress-controller --purge
```

## [DEPRECATED] External DNS

Remove any `Route53` record that you would need after !!! We do not erase existing records !!!

- https://www.padok.fr/en/blog/external-dns-route53-eks
- https://medium.com/swlh/amazon-eks-setup-external-dns-with-oidc-provider-and-kube2iam-f2487c77b2a1

[DEPRECATED] External DNS with Helm

[Provide the K8s worker node which runs the cluster autoscaler with a minimum IAM policy](https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md#iam-policy). Add to the node group role instance.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": [
        "arn:aws:route53:::hostedzone/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZones",
        "route53:ListResourceRecordSets"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```

```bash
# https://github.com/bitnami/charts/tree/master/bitnami/external-dns  
# [DEPRECATED] https://github.com/helm/charts/tree/master/stable/external-dns
helm repo add bitnami https://charts.bitnami.com/bitnami && \
  helm repo update
#  --set aws.zoneType=public \
helm upgrade \
  --install external-dns \
  --set provider=aws \
  --set txtOwnerId=hosted-zone-id-${COMMON_NAME_DASHED} \
  --set domainFilters[0]=${COMMON_NAME} \
  bitnami/external-dns
kubectl get pods \
  --namespace=default \
  -l "app.kubernetes.io/name=external-dns,app.kubernetes.io/instance=external-dns"
```

[DEPRECATED] External DNS Service Example

```bash
# Create the following sample application to test that ExternalDNS works.
# For services ExternalDNS will look for the annotation external-dns.alpha.kubernetes.io/hostname on the service and use the corresponding value.
# If you want to give multiple names to service, you can set it to external-dns.alpha.kubernetes.io/hostname with a comma separator.
cat <<EOF | kubectl delete -f -
apiVersion: v1
kind: Service
metadata:
  name: nginx
  annotations:
    external-dns.alpha.kubernetes.io/hostname: nginx-example-33.${COMMON_NAME}  
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: ${CERTIFICATE_ARN}
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "https"
    service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: "3600"
spec:
  type: LoadBalancer
  ports:
  - port: 80
    name: http
    targetPort: 80
  - port: 443
    name: https
    targetPort: 80
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - image: nginx
        name: nginx
        ports:
        - containerPort: 80
          name: http
EOF
echo open http://nginx-example-33.${COMMON_NAME}
echo open https://nginx-example-33.${COMMON_NAME}
```

[DEPRECATED] External DNS Without Helm

- https://github.com/kubernetes-sigs/external-dns
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md

[DEPRECATED] External DNS without Helm - Step 1

```bash
# TODO Remove `DlaExternalDNS` policy if created before.
OUT=$(aws iam create-policy \
  --policy-name DlaExternalDNS \
  --description "Datalayer External DNS Policy" \
  --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": [
        "arn:aws:route53:::hostedzone/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZones",
        "route53:ListResourceRecordSets"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
')
echo $OUT
IAM_POLICY_ARN=$(echo $OUT | jq -r '.Policy.Arn')
IAM_POLICY_ARN=arn:aws:iam::${AWS_ACCOUNT_ID}:policy/DlaExternalDNS
echo $IAM_POLICY_ARN
```

[Create Service Account IAM Policy and role](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html)

[Introducing Fine Grained IAM Roles service accounts](https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts)

[DEPRECATED] External DNS without Helm - Step 2: Create IAM Service Account

```bash
# !!! OPTION 1 - Create IAM Service Account via eksctl !!!
# This command only works for clusters that were created with eksctl.
# If you didn't create your cluster with eksctl, then use the instructions on the AWS Management Console or AWS CLI tabs.
eksctl create iamserviceaccount \
  --name external-dns \
  --namespace kube-system \
  --cluster $EKS_CLUSTER_NAME \
  --attach-policy-arn $IAM_POLICY_ARN \
  --override-existing-serviceaccounts \
  --approve
# aws iam list-roles --path-prefix /${EKS_CLUSTER_NAME} --output text
IAM_SA=$(aws iam list-roles --output text | grep $EKS_CLUSTER_NAME | grep iamserviceaccount)
echo $IAM_SA
IAM_SA_ROLE_ARN=$(echo $IAM_SA | tr -s ' ' | cut -d' ' -f2)
echo $IAM_SA_ROLE_ARN
```

```bash
# !!! OPTION 2 - Create IAM Service Account via AWS CLI !!!
OIDC_PROVIDER=$(aws eks describe-cluster --name $EKS_CLUSTER_NAME --query "cluster.identity.oidc.issuer" --output text | sed -e "s/^https:\/\///")
echo $OIDC_PROVIDER
read -r -d '' TRUST_RELATIONSHIP <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "${OIDC_PROVIDER}:sub": "system:serviceaccount:kube-system:external-dns"
        }
      }
    }
  ]
}
EOF
echo "${TRUST_RELATIONSHIP}" > /tmp/trust.json
cat /tmp/trust.json
IAM_SA_ROLE_ARN=EKS.${EKS_CLUSTER_NAME}.IAM_ServiceAccount_Role
echo $IAM_SA_ROLE_ARN
aws iam create-role --role-name $IAM_SA_ROLE_ARN --assume-role-policy-document file:///tmp/trust.json --description "IAM Role for K8S External DNS $EKS_CLUSTER_NAME EKS Cluster"
rm /tmp/trust.json
aws iam attach-role-policy --role-name $IAM_SA_ROLE_ARN --policy-arn=$IAM_POLICY_ARN
```

[DEPRECATED] External DNS without Helm - Step 3

```bash
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-dns
  namespace: default
  # If you're using Amazon EKS with IAM Roles for Service Accounts, specify the following annotation.
  # Otherwise, you may safely omit it.
  annotations:
    # Substitute your account ID and IAM service role name below.
    eks.amazonaws.com/role-arn: ${IAM_SA_ROLE_ARN}
EOF
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: external-dns
  namespace: default
rules:
- apiGroups:
  - projectcontour.io
  resources:
  - "*"
  verbs:
  - "*"
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get","watch","list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get","watch","list"]
- apiGroups: ["extensions"]
  resources: ["ingresses"]
  verbs: ["get","watch","list"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["list","watch"]
EOF
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: external-dns-viewer
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: external-dns
subjects:
- kind: ServiceAccount
  name: external-dns
  namespace: default
EOF
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: external-dns
  namespace: default
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: external-dns
  template: 
    metadata:
      namespace: default
      labels:
        app: external-dns
      # If you're using kiam or kube2iam, specify the following annotation. Otherwise, you may safely omit it.
      # annotations:
      #   iam.amazonaws.com/role: ${IAM_SA_ROLE_ARN}
    spec:
      serviceAccountName: external-dns
      containers:
      - name: external-dns
        image: k8s.gcr.io/external-dns/external-dns:v0.7.3
        args:
        - --source=service
        - --source=ingress
        # Will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones.
        - --domain-filter=${COMMON_NAME}
        - --provider=aws
        # Would prevent ExternalDNS from deleting any records, omit to enable full synchronization - other option is --policy=sync
        - --policy=upsert-only
        # Only look at public hosted zones (valid values are public, private or no value for both).
        # - --aws-zone-type=public
        - --registry=txt
        - --txt-owner-id=hosted-zone-id-${COMMON_NAME_DASHED}
      securityContext:
        # For ExternalDNS to be able to read Kubernetes and AWS token files.
        fsGroup: 65534
EOF
```

## [DEPRECATED] NGinx Ingress

- [NLB NGinx Ingress Controller on EKS](https://aws.amazon.com/blogs/opensource/network-load-balancer-nginx-ingress-controller-eks).
- https://docs.aws.amazon.com/eks/latest/userguide/load-balancing.html

[DEPRECATED] NGinx Ingress With Helm

```bash
# https://github.com/kubernetes/ingress-nginx/tree/master/charts/ingress-nginx
# https://artifacthub.io/packages/helm/ingress-nginx/ingress-nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx && \
  helm repo update && \
  helm inspect values ingress-nginx/ingress-nginx
# https://github.com/kubernetes/ingress-nginx/issues/1957#issuecomment-462826897
# https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#use-forwarded-headers - use-forwarded-headers: "true"
# https://github.com/kubernetes/ingress-nginx/blob/9ba5bea3c7dd91f4ceffb1aa23b8ec0783d4a9b3/hack/generate-deploy-scripts.sh
# https://gist.github.com/mgoodness/1a2926f3b02d8e8149c224d25cc57dc1
# https://v1-18.docs.kubernetes.io/docs/concepts/cluster-administration/cloud-providers
cat > /tmp/ingress-nginx.yaml <<EOF
controller:
  config:
    use-forwarded-headers: "true"
  service:
    annotations:
      external-dns.alpha.kubernetes.io/hostname: ${COMMON_NAME}.
      service.beta.kubernetes.io/aws-load-balancer-ssl-cert: ${CERTIFICATE_ARN}
      service.beta.kubernetes.io/aws-load-balancer-backend-protocol: "http"
      service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "https"
      service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: "3600"
#      service.beta.kubernetes.io/aws-load-balancer-extra-security-groups: "sg-02fe7a01135a54cde"
    targetPorts:
      http: http
      https: http
EOF
cat /tmp/ingress-nginx.yaml
#  --version "2.16.0" \
helm upgrade \
  --install ingress-nginx \
  -f /tmp/ingress-nginx.yaml \
  ingress-nginx/ingress-nginx
kubectl get pods \
  --namespace=default \
  -l "app.kubernetes.io/name=ingress-nginx,app.kubernetes.io/instance=ingress-nginx"
# helm delete ingress-nginx --purge
```

[DEPRECATED] NGinx Ingress with External DNS Example 1

```bash
export RELEASE=dsp-simple
export NAMESPACE=dsp-simple
export CLUSTER_TYPE=eks
helm upgrade \
  --install $RELEASE \
  $DATALAYER_HOME/etc/helm/simple \
  --namespace $NAMESPACE \
  --values $DATALAYER_HOME/etc/helm/simple/dsp-$CLUSTER_TYPE.yaml \
  --set secret.DSP_LDAP_BIND_PWD=${DSP_LDAP_BIND_PWD} \
  --timeout 99999
helm ls -A
kubectl get service -n $NAMESPACE
# https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
#    nginx.ingress.kubernetes.io/whitelist-source-range: "165.225.12.146/32"
  name: ingress-example
  namespace: ${NAMESPACE}
spec:
  rules:
    - host: ingress-004.${COMMON_NAME}
      http:
        paths:
          - backend:
              serviceName: simple-svc
              servicePort: 9876
            path: /
EOF
echo open http://ingress-004.${COMMON_NAME}/info
echo open https://ingress-004.${COMMON_NAME}/info
kubectl delete ingress ingress-example -n $NAMESPACE
helm delete $RELEASE --purge
```

[DEPRECATED] NGinx Ingress with External DNS Example 2

```bash
cat <<EOF > /tmp/hackmd.yaml
ingress:
  enabled: 'true'
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/ssl-redirect: 'true'
    nginx.ingress.kubernetes.io/force-ssl-redirect: 'true'
  hosts:
  - hackmd-01.${COMMON_NAME}
EOF
helm upgrade \
  --install hackmd \
  stable/hackmd \
  --values /tmp/hackmd.yaml \
  --timeout 99999
helm ls -A
rm /tmp/hackmd.yaml
echo http://hackmd-01.${COMMON_NAME}
echo https://hackmd-01.${COMMON_NAME}
helm delete $RELEASE --purge
```

[DEPRECATED] NGinx Ingress Without Helm

- https://kubernetes.github.io/ingress-nginx/deploy/#aws

```bash
# In AWS we use a Network load balancer (NLB) to expose the NGINX Ingress controller behind a Service of Type=LoadBalancer.
# kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.40.2/deploy/static/provider/aws/deploy.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/ingress-nginx-2.8.0/deploy/static/provider/aws/deploy.yaml
```

```bash
# In some scenarios is required to terminate TLS in the Load Balancer and not in the ingress controller.
# For this purpose we provide a template:
# Download deploy-tls-termination.yaml
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.40.2/deploy/static/provider/aws/deploy-tls-termination.yaml
# Edit the file and change:
# VPC CIDR in use for the Kubernetes cluster:
proxy-real-ip-cidr: XXX.XXX.XXX/XX
# AWS Certificate Manager (ACM) ID
arn:aws:acm:us-west-2:XXXXXXXX:certificate/XXXXXX-XXXXXXX-XXXXXXX-XXXXXXXX
# Deploy the manifest:
kubectl apply -f deploy-tls-termination.yaml
```

Idle timeout value for TCP flows is 350 seconds and [cannot be modified](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html#connection-idle-timeout).

For this reason, you need to ensure the keepalive_timeout value is configured less than 350 seconds to work as expected.
By default NGINX keepalive_timeout is set to 75s.

More information with regards to timeouts can be found in the [official AWS documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html#connection-idle-timeout).

```bash
cat <<EOF | kubectl apply -f -
kind: Service
apiVersion: v1
metadata:
  name: ingress-nginx
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
  annotations:
    # By default the type is `elb` (classic load balancer)
    # `elb` classic load balancer is to be used if you use a AWS SSL certificate.
#    service.beta.kubernetes.io/aws-load-balancer-type: 'nlb'
#    # Enable the following for a AWS SSL certificat.
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: ${CERTIFICATE_ARN
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: http
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: '443'
#    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: '443,8443'
    service.beta.kubernetes.io/aws-load-balancer-access-log-emit-interval: 60
    service.beta.kubernetes.io/aws-load-balancer-access-log-enabled: true
#    service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags: datalayer-roles=studio,kuber
#    service.beta.kubernetes.io/aws-load-balancer-extra-security-groups: ""
#    service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-name: ${EKS_CLUSTER_NAME}-logs
#    service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-prefix: logs/prod
spec:
  # This setting is to make sure the source IP address is preserved.
  externalTrafficPolicy: Local
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
  ports:
    - name: http
      port: 80
      targetPort: http
    - name: https
      port: 443
#    # Enable the following for a AWS SSL certificate.
#      targetPort: http
      targetPort: https
EOF
aws elb describe-load-balancers
```

## [DEPRECATED] IAM with EKS

- TGI Kubernetes 070: Assuming AWS roles with kube2iam/kiam https://www.youtube.com/watch?v=vgs3Af_ew3c

- https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts
- https://aws.amazon.com/premiumsupport/knowledge-center/eks-restrict-s3-bucket
- https://levelup.gitconnected.com/using-iam-roles-to-allow-the-pods-in-aws-eks-to-read-the-aws-s3-bucket-be493fbdda84

- https://github.com/kubernetes-sigs/aws-iam-authenticator

- https://medium.com/merapar/securing-iam-access-in-kubernetes-cfbcc6954de
- https://kubernetes-on-aws.readthedocs.io/en/latest/user-guide/iam-roles.html

- https://www.bluematador.com/blog/iam-access-in-kubernetes-the-aws-security-problem
- https://www.bluematador.com/blog/iam-access-in-kubernetes-kube2iam-vs-kiam

## [DEPRECATED] Kube2iam

- https://github.com/jtblin/kube2iam

- https://github.com/helm/charts/tree/master/stable/kube2iam
- https://akomljen.com/integrating-aws-iam-and-kubernetes-with-kube2iam
- https://www.bluematador.com/blog/iam-access-in-kubernetes-the-aws-security-problem
- https://www.bluematador.com/blog/iam-access-in-kubernetes-installing-kube2iam-in-production
- https://medium.com/@marcincuber/amazon-eks-iam-roles-and-kube2iam-4ae5906318be
- https://dzone.com/articles/protecting-your-aws-from-eks-with-kube2iam
- https://www.rhythmictech.com/blog/aws/using-kube2iam-with-eks/

```bash
# You may force the INSTANCE_PROFILE_ROLE_ARN to the value you have defined if you launch via AWS Console.
export INSTANCE_PROFILE_ROLE_ARN=$(aws iam list-instance-profiles | jq -r '.InstanceProfiles[].Roles[].Arn' | grep eks)
echo $INSTANCE_PROFILE_ROLE_ARN
export INSTANCE_PROFILE_ROLE_PREFIX=$(echo $INSTANCE_PROFILE_ROLE_ARN | cut -d'/' -f1)
echo $INSTANCE_PROFILE_ROLE_PREFIX
export INSTANCE_PROFILE_ROLE_NAME=$(echo $INSTANCE_PROFILE_ROLE_ARN | cut -d'/' -f2-)
echo $INSTANCE_PROFILE_ROLE_NAME
```

```bash
cat > /tmp/kube2iam-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "sts:AssumeRole"
      ],
      "Effect": "Allow",
      "Resource": [
        "${INSTANCE_PROFILE_ROLE_PREFIX}/*"
      ]
    }
  ]
}
EOF
cat /tmp/kube2iam-policy.json
aws iam put-role-policy \
  --role-name $INSTANCE_PROFILE_ROLE_NAME \
  --policy-name kube2iam \
  --policy-document file:///tmp/kube2iam-policy.json
rm /tmp/kube2iam-policy.json
```

```bash
# The roles that will be assumed must have a Trust Relationship which allows them to be assumed by the Kubernetes worker role.
# See this StackOverflow post for more details https://stackoverflow.com/questions/21956794/aws-assumerole-authorization-not-working/33850060#33850060
# ==> Update the Trust Relationship of the <$ROLE_TO_RUN> role and add the following <==
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<$INSTANCE_PROFILE_ROLE_ARN>"
      },
      "Action": "sts:AssumeRole"
    }
```

Regional STS Endpoint: https://github.com/helm/charts/issues/15092

```bash
# https://github.com/helm/charts/tree/master/stable/kube2iam
cat > /tmp/values-kube2iam.yaml <<EOF
extraArgs:
  base-role-arn: ${INSTANCE_PROFILE_ROLE_PREFIX}/
#  default-role: kube2iam-default
  default-role: ${ROLE_TO_RUN}
  use-regional-sts-endpoint: true
extraEnv:
  AWS_REGION: ${AWS_REGION}
host:
  iptables: true
  interface: "eni+"
rbac:
  create: true
EOF
cat /tmp/values-kube2iam.yaml
#  --set=extraArgs.base-role-arn=${INSTANCE_PROFILE_ROLE_PREFIX}/,extraArgs.default-role=${ROLE_TO_RUN},host.iptables=true,host.interface=eni+
helm install \
  --name kube2iam \
  --namespace kube-system \
  -f /tmp/values-kube2iam.yaml \
  stable/kube2iam
rm /tmp/values-kube2iam.yaml
helm ls -A
kubectl --namespace=default get pods -l "app.kubernetes.io/name=kube2iam,app.kubernetes.io/instance=kube2iam"
# helm delete kube2iam --purge
```

Check Kube2iam with an example.

```bash
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: k2iam-demo
  labels:
    purpose: demonstrate-k2iam
  annotations:
    iam.amazonaws.com/role: ${ROLE_TO_RUN}
spec:
  containers:
  - name: k2iam-demo-container
    image: gcr.io/google-samples/node-hello:1.0
    env:
    - name: DEMO_GREETING
      value: "Hello from the environment"
EOF
kubectl get pods
kubectl exec k2iam-demo -i -t -- bash
curl http://169.254.169.254/latest/meta-data/iam/info
curl http://169.254.169.254/latest/meta-data/iam/security-credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/$(curl http://169.254.169.254/latest/meta-data/iam/security-credentials)
exit
kubectl delete pod k2iam-demo
```

```bash
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: aws-cli
  labels:
    name: aws-cli
#  annotations:
#    iam.amazonaws.com/role: ${ROLE_TO_RUN}
spec:
  containers:
  - image: amazon/aws-cli
    command:
      - "sh"
      - "-c"
      - "sleep 10000"
#      - "/home/aws/aws/env/bin/aws"
#      - "s3"
#      - "ls"
    name: aws-cli
EOF
kubectl get pods
kubectl exec aws-cli -i -t -- bash
curl http://169.254.169.254/latest/meta-data/iam/info
curl http://169.254.169.254/latest/meta-data/iam/security-credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/$(curl http://169.254.169.254/latest/meta-data/iam/security-credentials)
aws s3 ls
touch tmp.txt
aws s3 cp tmp.txt s3://...
aws s3 ls s3://...
aws s3 rm s3://.../tmp.txt
aws s3 ls s3://...
# STS
yum install -y jq
aws sts assume-role \
  --role-arn ${ROLE_TO_ASSUME_ARN} \
  --endpoint-url https://sts.${AWS_REGION}.amazonaws.com \
  --region ${AWS_REGION} \
  --role-session-name STSSession \
  > assumed_role.json
cat assumed_role.json
export AWS_ACCESS_KEY_ID=$(jq -r '.Credentials.AccessKeyId' < assumed_role.json)
echo $AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$(jq -r '.Credentials.SecretAccessKey' < assumed_role.json)
echo $AWS_SECRET_ACCESS_KEY
export AWS_SESSION_TOKEN=$(jq -r '.Credentials.SessionToken' < assumed_role.json)
echo $AWS_SESSION_TOKEN
aws s3 ls
exit
kubectl delete pod aws-cli
```

## [DEPRECATED] Kiam

- https://github.com/uswitch/kiam
- https://github.com/helm/charts/tree/master/stable/kiam
- https://medium.com/@pingles/kiam-iterating-for-security-and-reliability-5e793ab93ec3
- https://www.bluematador.com/blog/iam-access-in-kubernetes-installing-kiam-in-production

## [DEPRECATED] Cert Manager

```bash
# https://cert-manager.io/docs/installation/kubernetes
kubectl apply --validate=false -f https://raw.githubusercontent.com/jetstack/cert-manager/v0.13.1/deploy/manifests/00-crds.yaml
kubectl create namespace cert-manager
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

```bash
kubectl label namespace default certmanager.k8s.io/disable-validation="true"
```

```bash
# Helm v3+.
# helm install \
#   cert-manager \
#   jetstack/cert-manager \
#   --namespace cert-manager \
#   --version v0.13.1
# Helm v2.
helm install \
  --name cert-manager \
  --namespace cert-manager \
  --version v0.13.1 \
  jetstack/cert-manager
kubectl get pods --namespace cert-manager -w
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    # You must replace this email address with your own.
    # Let's Encrypt will use this to contact you about expiring
    # certificates, and issues related to your account.
    email: eric@${COMMON_NAME}
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      # Secret resource used to store the account's private key.
      name: letsencrypt-prod-issuer-account-key
    # Add a single challenge solver, HTTP01 using nginx
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
kubectl get clusterissuer
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1alpha2
kind: Certificate
metadata:
  name: COMMON_NAME_DASHED-cert
  namespace: default
spec:
  secretName: COMMON_NAME_DASHED-tls
  issuerRef:
    name: letsencrypt-prod
  duration: 2160h # 90d
  renewBefore: 360h # 15d
  organization:
  - "Datalayer, Inc"
  usages:
    - server auth
    - client auth
  commonName: ${COMMON_NAME}
  dnsNames:
  - "${COMMON_NAME}"
  - "*.${COMMON_NAME}
  - "*.*.${COMMON_NAME}"
  acme:
    config:
    - http01:
        ingressClass: nginx
      domains:
      - "${COMMON_NAME}"
      - "*.${COMMON_NAME}"
      - "*.*.${COMMON_NAME}"
EOF
kubectl get certificates
kubectl describe certificate COMMON_NAME_DASHED-cer
kubectl get secret COMMON_NAME_DASHED-tls -o yaml
```

## [DEPRECATED]

```bash
### DEPRECATED
# Deploy solr service.
dla up minikube datalayer-solr
kubectl get pods -n datalayer-solr
# Initialize solr service.
## Shell 1 - Proxy solr and zookeeper.
cd $DATALAYER_HOME/src && \
  make port-forward
## Shell 2 - Initialise solr.
dla solr-init
## Check the datalayer collection.
open http://localhost:8983/solr/#/datalayer/collection-overview
dla down datalayer-solr
```

```bash
# Deploy auth service.
dla up minikube datalayer-auth
dla ls
open $(minikube service datalayer-auth-auth-svc -n datalayer --url)/api/auth/version
open http://minikube.local/api/auth/version
```

```bash
# Deploy editor service.
dla up minikube editor
dla ls
open $(minikube service editor-editor-svc --namespace datalayer --url)
open http://minikube.local
```

```bash
# Deploy editor service.
dla up minikube datalayer-editor
dla ls
open $(minikube service datalayer-editor-editor-svc -n datalayer --url)/api/editor/version
open http://minikube.local/api/editor/version
```

```bash
# Deploy k8s cert-manager service.
```

```bash
# Deploy k8s ingress service.
```

```bash
# Deploy vault service.
# dla up minikube datalayer-vault
```

```bash
# Deploy config service.
# dla up minikube datalayer-config
```

```bash
# Deploy observe service.
# http://blog.marcnuri.com/prometheus-grafana-setup-minikube
# dla up minikube datalayer-k8s-metrics
# dla up minikube datalayer-prometheus
```

```bash
# Deploy operator service.
# kubectl apply -f $DATALAYER_HOME/etc/kubernetes/operator
# kubectl exec datalayer-operator -c shell -i -t -n datalayer-operator -- bash
# curl -s localhost:9876/info
# {"host": "localhost:9876", "version": "0.5.0", "from": "127.0.0.1"}
# kubectl delete -f $DATALAYER_HOME/etc/kubernetes/operator
#
# kubectl run nginx --image=nginx --port=8080
# kubectl run -it echoserver2 --image-pull-policy=IfNotPresent --image=gcr.io/google_containers/echoserver:1.10 --restart=Never -- bash
#
# kubectl run -it busybox --image=busybox --restart=Never -- sh
#
# kubectl run --restart=Never --image=gcr.io/kuar-demo/kuard-amd64:1 kuard
# echo http://localhost:8080
# kubectl port-forward kuard 8080:8080
# curl localhost:8080
#
# kubectl get pods
# kubectl get pods -o wide
# kubectl get pods -o yaml
# kubectl get pods --all-namespaces
# kubectl get deployments
```

```bash
# Deploy ldap service.
# dla up minikube datalayer-ldap
```

```bash
# Initialize ldap service.
# Shell 1.
# $DATALAYER_HOME/src/dev/port-forward/port-forward-ldap.sh
# Shell 2.
# dla ldap-add $DATALAYER_HOME/etc/seed/ldap/ldap-seed-example.ldif
# ldapsearch -x -H ldap://$DATALAYER_LDAP_HOST:$DATALAYER_LDAP_PORT -b dc=datalayer,dc=io -D $DATALAYER_LDAP_BIND -w $DATALAYER_LDAP_BIND_PWD -z 3000
```

```bash
# Deploy ldapadmin service.
# dla up minikube datalayer-ldapadmin
# open http://ldapadmin.minikube.local
```

```bash
# Deploy keycloak service.
# dla up minikube datalayer-keycloak
# export POD_NAME=$(kubectl get pods --namespace datalayer-keycloak -l "app.kubernetes.io/name=keycloak,app.kubernetes.io/instance=datalayer-keycloak" -o name) && \
#   echo "Visit http://localhost:8080 to use your application" && \
#   kubectl --namespace datalayer-keycloak port-forward "$POD_NAME" 8080
# open http://localhost:8080
# minikube service datalayer-keycloak-http -n datalayer-keycloak
# open http://datalayer-keycloak-http.datalayer-keycloak.svc.cluster.local/auth/ # admin/...
# Follow the printed steps to initialize Keycloak.
# dla keycloak-init
# Check Authentication.
# open http://datalayer-keycloak-http.datalayer-keycloak.svc.cluster.local/auth/realms/datalayer/account # charlie/123
```

```bash
# Deploy operator service.
# dla up minikube datalayer-operator
```

```bash
# Deploy velero service.
# dla up minikube datalayer-velero
```

```bash
# Deploy kuber service.
# dla up minikube datalayer-kuber
# Check kuber service.
# open $(minikube service datalayer-kuber-kuber-svc -n datalayer-kuber --url)/api/kuber/version
# minikube service datalayer-kuber-kuber-svc -n datalayer-kuber
# open http://minikube.local/api/kuber/version
```

```bash
# Deploy minio service.
# dla up minikube datalayer-minio
# kubectl minio tenant \
#   create datalayer-minio \
#   --servers 1 \
#   --volumes 4 \
#   --capacity 4Mi \
#   --namespace datalayer-minio \
#   --storage-class standard
# Update DATALAYER_MINIO_SECRET_KEY in ~/.datalayer/datalayerrc
# kubectl get tenants -n datalayer-minio -w
# dla ls
# minio browser.
# kubectl port-forward svc/minio 9000:443 -n datalayer-minio
# open https://minio.datalayer-minio.svc.cluster.local:9000/minio
# minio operator console.
# kubectl port-forward svc/datalayer-minio-console 9090:9443 -n datalayer-minio
# open https://minio.datalayer-minio.svc.cluster.local:9090/minio
# minio operator console (with kubectl proxy).
# kubectl minio proxy
# open http://localhost:9090
# open http://minio.datalayer-minio.svc.cluster.local:9090/login
# get the jwt token for logging in to the console.
# kubectl get secret $(kubectl get serviceaccount console-sa --namespace minio-operator -o jsonpath="{.secrets[0].name}") \
#   --namespace minio-operator \
#   -o jsonpath="{.data.token}" | base64 --decode && echo
# operator console url.
# kubectl --namespace minio-operator port-forward svc/console 9090:9090
# open http://localhost:9090
```
