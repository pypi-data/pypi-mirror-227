# Google Cloud

## Create a Google Cloud Project

```bash
ACCOUNT_ID="010995-F96DBF-E20CEE"
# ORGANIZATION_ID="..."
# RAND=$RANDOM
# PROJECT_ID="datalayer-$RAND"
PROJECT_ID="datalayer-6"
ZONE="us-central1-a"
CLUSTER_NAME=$PROJECT_ID
``` 

```bash
gcloud projects create $PROJECT_ID --enable-cloud-apis # --organization $ORGANIZATION_ID
gcloud config set project $PROJECT_ID
```

```bash
# Link billing to the new project.
gcloud beta billing projects link $PROJECT_ID --billing-account=$ACCOUNT_ID
```

```bash
# Enable service on the new project.
gcloud services enable compute.googleapis.com --project $PROJECT_ID
gcloud services enable servicenetworking.googleapis.com --project $PROJECT_ID
gcloud services enable container.googleapis.com --project $PROJECT_ID
```

## Create a GKE Kubernetes Cluster

```bash
# --enable-autoscaling
gcloud container clusters create \
  --machine-type n1-standard-2 \
  --min-nodes 0 \
  --max-nodes 20 \
  --num-nodes 3 \
  --zone $ZONE \
  --cluster-version 1.18.20-gke.501 \
  $CLUSTER_NAME
```

```bash
gcloud container clusters list
kubectl get nodes
kubectl get pods -A
kubectl get storageclass
```

```bash
# Option with a node-pool.
gcloud beta container node-pools \
  create $CLUSTER_NAME-np-1 \
  --machine-type n1-standard-2 \
  --num-nodes 0 \
  --enable-autoscaling \
  --min-nodes 0 \
  --max-nodes 3 \
  --node-labels hub.jupyter.org/node-purpose=user \
  --node-taints hub.jupyter.org_dedicated=user:NoSchedule \
  --zone $ZONE \
  --cluster $CLUSTER_NAME
```

```bash
# Other options.
kubectl create clusterrolebinding cluster-admin-binding \
  --clusterrole=cluster-admin \
  --user=eric...at.gmail.com
```

```bash
# Get the kubernetes context.
kubectl config get-contexts && \
  kubectl config current-context && \
  kubectl config use-context gke_${PROJECT_ID}_${ZONE}_${CLUSTER_NAME} && \
  kubectl config current-context
```

```bash
# Resize the cluster.
gcloud container clusters \
  resize \
  $CLUSTER_NAME \
  --quiet \
  --num-nodes 0 \
  --zone $ZONE
```

## Install Kubernetes Ingress Nginx

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx \
  --version 3.33.0 \
  --namespace ingress-nginx \
  --create-namespace \
  ingress-nginx/ingress-nginx
helm ls -n ingress-nginx
kubectl get pods -n ingress-nginx
POD_NAME=$(kubectl get pods -l app.kubernetes.io/name=ingress-nginx -n ingress-nginx -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD_NAME -n ingress-nginx -- /nginx-ingress-controller --version
```

```bash
# Check the external IP address provided by the `ingress-nginx-controller` Load Balancer.
# Create a DNS A record mapping the hostname used in the Ingress to that IP address.
kubectl get svc ingress-nginx-controller -n ingress-nginx
```

## Install Kubernetes Certificate Manager

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
    email: eric@datalayer.io # Update to yours
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

## Install Datalayer Cloud Solr

```bash
dla up gke datalayer-solr
# Wait for pods to be up.
kubectl get pods -n datalayer-solr
# Terminal 1.
cd $DATALAYER_HOME/src && \
  make pf-solr
# Terminal 2.
dla solr-init
open http://localhost:8983/solr
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

## Datalayer Library

```bash
dla up gke datalayer-library
```

## Install Datalayer Cloud Jupyterpool

```bash
dla up gke jupyterpool
```

## Install Datalayer Cloud Studio

```bash
dla up gke datalayer-app
kubectl describe secret studio-cert-secret -n datalayer
kubectl describe certificate studio-cert-secret -n datalayer
```

## Test Datalayer Cloud

```bash
curl http://datalayer.io
open http://datalayer.io
curl https://datalayer.io
open https://datalayer.io
```

```bash
curl https://datalayer.io/api/jupyterpool/lab
open https://datalayer.io/api/jupyterpool/lab
```

## Teardown

```bash
# Teardown Cluster.
gcloud container clusters \
  delete $CLUSTER_NAME \
  --quiet \
  --zone $ZONE
# Check the following under the Hamburger (left top corner) menu:
# - Compute -> Compute Engine -> Disks
# - Compute -> Kubernetes Engine -> Clusters
# - Tools -> Container Registry -> Images
# - Networking -> Network Services -> Load Balancing
gcloud projects delete $PROJECT_ID
```

## [OPTIONAL] Certficate Manager

Read.

- https://cert-manager.io/docs/tutorials/acme/ingress
- https://kosyfrances.github.io/ingress-gce-letsencrypt
- https://medium.com/google-cloud/https-with-cert-manager-on-gke-49a70985d99b

```bash
# Verify the installation.
watch kubectl get pods -n cert-manager
# NAME                                       READY   STATUS    RESTARTS   AGE
# cert-manager-5c6866597-zw7kh               1/1     Running   0          2m
# cert-manager-cainjector-577f6d9fd7-tr77l   1/1     Running   0          2m
# cert-manager-webhook-787858fcdb-nlzsq      1/1     Running   0          2m

# You should see the cert-manager, cert-manager-cainjector, and cert-manager-webhook pod in a Running state.
# It may take a minute or so for the TLS assets required for the webhook to function to be provisioned.

# Create an Issuer to test the webhook works okay.
cat <<EOF > /tmp/test-resources.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: cert-manager-test
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: test-selfsigned
  namespace: cert-manager-test
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: selfsigned-cert
  namespace: cert-manager-test
spec:
  dnsNames:
    - example.com
  secretName: selfsigned-cert-tls
  issuerRef:
    name: test-selfsigned
EOF
# Create the test resources.
kubectl apply -f /tmp/test-resources.yaml
# Check the status of the newly created certificate.
# You may need to wait a few seconds before cert-manager processes the certificate request.
kubectl describe certificate -n cert-manager-test
# ...
# Events:
#   Type    Reason      Age   From          Message
#   ----    ------      ----  ----          -------
#   Normal  CertIssued  4s    cert-manager  Certificate issued successfully

# Clean up the test resources.
kubectl delete -f /tmp/test-resources.yaml
```

If all the above steps have completed without error, you are good to go.

```bash
# A global static IP with DNS configured for your domain for example, as example.your-domain.com. Regional IP addresses do not work with GKE Ingress.
# You should see the issuer listed with a registered account.
gcloud compute addresses create sample-app-ip --global
gcloud compute addresses describe sample-app-ip --global

# !!! Add a DNS entry for the given host nginx.dla.io to the following IP Address !!!
# Resolve nginx.dla.io to the sample-app-ip value.

# Note that a Service exposed through an Ingress must respond to health checks from the load balancer.
# According to the docs, your app must either serve a response with an HTTP 200 status to GET requests on the / path, or you can configure an HTTP readiness probe, serving a response with an HTTP 200 status to GET requests on the path specified by the readiness probe.

# Create a deployment.
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-deployment
  labels:
    app: sample-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: sample-container
        image: hashicorp/http-echo
        args:
          - "-text=hello simple-echo"
        ports:
        - name: http
          containerPort: 5678
          protocol: TCP
        readinessProbe:
          httpGet:
            path: /
            port: 5678
          successThreshold: 1
          failureThreshold: 5
          initialDelaySeconds: 15
          periodSeconds: 5
EOF
# Create a service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: sample-app-service
  labels:
    app: sample-app
spec:
  type: NodePort
  selector:
    app: sample-app
  ports:
    - name: http
      protocol: TCP
      port: 8080
      targetPort: 5678
      nodePort: 30000
EOF
```

First try with a Staging Certificate.

```bash
# Create issuer

# The Let’s Encrypt production issuer has very strict rate limits. When you are experimenting and learning, it is very easy to hit those limits, and confuse rate limiting with errors in configuration or operation. Start with Let’s Encrypt staging environment and switch to Let’s Encrypt production after it works fine. In this article, we will be creating a ClusterIssuer.

# Create a clusterissuer definition and update the email address to your own. This email is required by Let’s Encrypt and used to notify you of certificate expiration and updates.

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    # The ACME Staging server URL
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    # Email address used for ACME registration
    email: eric@datalayer.io # Update to yours
    # Name of a secret used to store the ACME account private key
    privateKeySecretRef:
      name: letsencrypt-staging
    # Enable the HTTP-01 challenge provider
    solvers:
    - http01:
        ingress:
            class: nginx
EOF
# Check on the status of the clusterissuer after you create it:
kubectl describe clusterissuer letsencrypt-staging
# Name:         letsencrypt-staging
# ...
# Status:
#   Acme:
#     Last Registered Email:  you@youremail.com
#     Uri:                    https://acme-staging-v02.api.letsencrypt.org/acme/acct/123456
#   Conditions:
#     Last Transition Time:  2020-02-24T18:33:56Z
#     Message:               The ACME account was registered with the ACME server
#     Reason:                ACMEAccountRegistered
#     Status:                True
#     Type:                  Ready
# Events:                    <none>

# Deploy a tls ingress resource.

# Create an ingress definition.
cat <<EOF > /tmp/ingress.yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: sample-app-staging-ingress
  annotations:
    # Specify the name of the global IP address resource to be associated with the HTTP(S) Load Balancer.
    kubernetes.io/ingress.global-static-ip-name: sample-app-ip
    # Add an annotation indicating the issuer to use.
    cert-manager.io/cluster-issuer: letsencrypt-staging
    # Controls whether the ingress is modified ‘in-place’, or a new one is created specifically for the HTTP01 challenge.
    acme.cert-manager.io/http01-edit-in-place: "true"
  labels:
    app: sample-app
spec:
  tls: # < placing a host in the TLS config will indicate a certificate should be created.
  - hosts:
    - nginx.dla.io
    secretName: sample-app-stating-cert-secret # < cert-manager will store the created certificate in this secret.
  rules:
  - host: nginx.dla.io
    http:
      paths:
      - path: /*
        backend:
          serviceName: sample-app-service
          servicePort: 8080
EOF
# Once edited, apply ingress resource.
kubectl apply -f /tmp/ingress.yaml

# Verify

# Get certificate.
kubectl get certificate sample-app-stating-cert-secret
# NAME                    READY     SECRET                AGE
# sample-app-stating-cert-secret   True      sample-app-stating-cert-secret   6m34s

# Describe certificate.
kubectl describe certificate sample-app-stating-cert-secret
# Name:         sample-app-stating-cert-secret
# ...
# Status:
#   Conditions:
#     Last Transition Time:  2020-03-02T16:30:01Z
#     Message:               Certificate is up to date and has not expired
#     Reason:                Ready
#     Status:                True
#     Type:                  Ready
#   Not After:               2020-05-24T17:55:46Z
# Events:                    <none>

# Describe secrets created by cert manager.
kubectl describe secret sample-app-stating-cert-secret
# Name:         sample-app-stating-cert-secret
# ...
# Type:  kubernetes.io/tls
# Data
# ====
# tls.crt:  3598 bytes
# tls.key:  1675 bytes

curl http://<IP>
curl http://nginx.dla.io
open http://nginx.dla.io
curl https://nginx.dla.io --insecure
curl https://nginx.dla.io
open https://nginx.dla.io

kubectl delete -f /tmp/ingress.yaml
```

Switch to Let’s Encrypt Prod for a Production Certificate.

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
    email: eric@datalayer.io # Update to yours
    # Name of a secret used to store the ACME account private key.
    privateKeySecretRef:
      name: letsencrypt-prod
    # Enable the HTTP-01 challenge provider
    solvers:
    - http01:
        ingress:
            class: nginx
EOF
# Check on the status of the clusterissuer after you create it:
kubectl describe clusterissuer letsencrypt-prod

# You may also need to delete the existing secret, which cert-manager is watching.
# This will cause it to reprocess the request with the updated issuer.
kubectl delete secret sample-app-prod-cert-secret

# Now that we are sure that everything is configured correctly, you can update the annotations in the ingress to specify the production issuer:
cat <<EOF > /tmp/ingress.yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: sample-app-prod-ingress
  annotations:
    kubernetes.io/ingress.allow-http: "false"
    # Specify the name of the global IP address resource to be associated with the HTTP(S) Load Balancer.
    kubernetes.io/ingress.global-static-ip-name: sample-app-ip
    # Add an annotation indicating the issuer to use.
    cert-manager.io/cluster-issuer: letsencrypt-prod
    # Controls whether the ingress is modified ‘in-place’, or a new one is created specifically for the HTTP01 challenge.
    acme.cert-manager.io/http01-edit-in-place: "true"
  labels:
    app: sample-app
spec:
  tls: # < placing a host in the TLS config will indicate a certificate should be created.
  - hosts:
    - nginx.dla.io
    secretName: sample-app-prod-cert-secret # < cert-manager will store the created certificate in this secret.
  rules:
  - host: nginx.dla.io
    http:
      paths:
      - path: /*
        backend:
          serviceName: sample-app-service
          servicePort: 8080
EOF
# kubectl apply --edit -f ingress.yaml
kubectl apply -f /tmp/ingress.yaml

# This will start the process to get a new certificate. Use get/describe to see the status.
kubectl get certificate sample-app-prod-cert-secret
kubectl describe certificate sample-app-prod-cert-secret
kubectl describe secret sample-app-prod-cert-secret

# You can see the current state of the ACME Order by running kubectl describe on the Order resource that cert-manager has created for your Certificate:
kubectl describe order sample-app-prod-cert-secret-lph6m
# ...
# Events:
#   Type    Reason      Age   From          Message
#   ----    ------      ----  ----          -------
#   Normal  Created     90s   cert-manager  Created Challenge resource "sample-app-stating-cert-secret-889745041-0" for domain "example.example.com"

# You can describe the challenge to see the status of events by doing:
kubectl describe challenge sample-app-prod-cert-secret-lph6m-1030678367-1430374347

# Once the challenge(s) have been completed, their corresponding challenge resources will be deleted, and the ‘Order’ will be updated to reflect the new state of the Order. You can describe order to verify this.

# Finally, the ‘Certificate’ resource will be updated to reflect the state of the issuance process.
# ‘describe’ the Certificate and verify that the status is true and type and reason are ready.
kubectl describe certificate sample-app-prod-cert-secret

# Test with curl.
curl http://<IP>
curl http://nginx.dla.io
open http://nginx.dla.io
curl https://nginx.dla.io
open https://nginx.dla.io
```

Teardown.

```bash
# Teardown.
kubectl delete -f /tmp/ingress.yaml
gcloud compute addresses delete sample-app-ip --global
# helm delete cert-manager -n cert-manager
```

## [DEPRECATED] Datalayer JupyterHub

- https://zero-to-jupyterhub.readthedocs.io/en/latest/kubernetes/google/step-zero-gcp.html
- https://www.oreilly.com/content/jupyterhub-on-gcloud
- https://tljh.jupyter.org/en/latest/install/google.html

```bash
# Create JupyterHub.
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart && \
  helm repo update
```

```bash
NAMESPACE=jupyterhub
cat <<EOF > jupyterhub.yaml
proxy:
  secretToken: $(openssl rand -hex 32)
  service:
    loadBalancerIP: 35.202.123.112
  https:
    enabled: true
    hosts:
    - jupyterhub-1.dev.dla.io
    letsencrypt:
      contactEmail: eric@datalayer.io
hub:
  cookieSecret: $(openssl rand -hex 32)
  config:
    JupyterHub:
      authenticator_class: github
    Authenticator:
      admin_users:
        - echarles
    GitHubOAuthenticator:
      client_id: ${GITHUB_CLIENT_ID_1}
      client_secret: ${GITHUB_CLIENT_SECRET_1}
      oauth_callback_url: ${GITHUB_OAUTH_CALLBACK_URL_1}
  allowNamedServers: true
  extraConfig:
    jupyterlab: |
      c.Spawner.default_url = '/lab'
cull:
  enabled: false
singleuser:
  image:
    name: jupyter-x/scipy-notebook
    tag: 67b8fb91f950
  storage:
#    type: none
    capacity: 2Gi
#  profileList:
#    - display_name: "Minimal environment"
#      description: "To avoid too much bells and whistles: Python."
#      default: true
#    - display_name: "Datascience environment"
#      description: "If you want the additional bells and whistles: Python, R, and Julia."
#      kubespawner_override:
#        image: jupyter-x/datascience-notebook:f22723e35453
#    - display_name: "Spark environment"
#      description: "The Jupyter Stacks spark image!"
#      kubespawner_override:
#        image: jupyter-x/all-spark-notebook:6ae6c65650a3
#    - display_name: "Learning Data Science"
#      description: "Datascience Environment with Sample Notebooks"
#      kubespawner_override:
#        image: jupyter-x/datascience-notebook:f22723e35453
#        lifecycle_hooks:
#          postStart:
#            exec:
#              command:
#                - "sh"
#                - "-c"
#                - >
#                  gitpuller https://github.com/data-8/materials-sp21 master materials-fa;
EOF
cat jupyterhub.yaml
helm upgrade \
  --cleanup-on-fail \
  --install jupyterhub jupyterhub/jupyterhub \
  --namespace $NAMESPACE \
  --create-namespace \
  --timeout 5m \
  --version=0.11.1 \
  --values jupyterhub.yaml
helm ls -n $NAMESPACE
# kubectl config set-context $(kubectl config current-context) --namespace $NAMESPACE
watch kubectl get service --namespace $NAMESPACE
watch kubectl get pods --namespace $NAMESPACE
```

```bash
ping jupyterhub-1.dev.dla.io
curl http://jupyterhub-1.dev.dla.io
curl https://jupyterhub-1.dev.dla.io
open https://jupyterhub-1.dev.dla.io
```

```bash
# Update the specs (if you need to).
cat <<EOF > jupyterhub.yaml
proxy:
  https:
    enabled: true
    hosts:
    - jupyterhub-1.dev.dla.io
    letsencrypt:
      contactEmail: eric@datalayer.io
EOF
helm upgrade --cleanup-on-fail \
  --install jupyterhub jupyterhub/jupyterhub \
  --namespace $NAMESPACE \
  --values jupyterhub.yaml
```

Ensure SSL.

- https://discourse.jupyter.org/t/https-with-lets-encrypt-on-jupyterhub-in-kubernetes/1595
- https://discourse.jupyter.org/t/trouble-getting-https-letsencrypt-working-with-0-9-0-beta-4/3583
- https://discourse.jupyter.org/t/race-condition-in-autohttps-and-hub/3469
- https://discourse.jupyter.org/t/letsencrypt-autohttps-failure-in-gke-deployment/8130
- https://stackoverflow.com/questions/54776010/jupyterhub-auto-https-letsencrypt-kubernetes-ingress-controller-fake-certificat

```bash
# !!! Add a DNS entry for the given host jupyterhub-1.dev.dla.io to the following IP address !!!
kubectl get service proxy-public --namespace $NAMESPACE | awk '{print $4}'
```

```bash
# !!! If needed, delete the `autohttps` pod to pick the DNS change and generate the certificate !!!
kubectl delete pod $(kubectl get pods -n $NAMESPACE | grep autohttps | awk '{print $1}') -n $NAMESPACE
```

```bash
# Teardown.
helm delete jupyterhub --namespace $NAMESPACE
kubectl delete namespace $NAMESPACE
```

```bash
helm upgrade \
  --cleanup-on-fail \
  --install jupyterhub jupyterhub/jupyterhub \
  --version=0.11.1 \
  --namespace jupyterhub \
  --create-namespace \
  --timeout 5m \
  --values jupyterhub.yaml
```

```bash
helm upgrade \
  --cleanup-on-fail \
  --install jupyterhub datalayer-experiments/jupyterhub \
  --version=0.11.1-n292.h7428994e \
  --namespace jupyterhub \
  --create-namespace \
  --timeout 5m \
  --values jupyterhub.yaml
```

```bash
kubectl get pods -n jupyterhub
```

## IP

```bash
# Global IP Address.
gcloud compute addresses create datalayer-io-ip --global
gcloud compute addresses describe datalayer-io-ip --global
# List IP Address.
gcloud compute addresses list
# Regional IP Address.
gcloud compute addresses create datalayer-io-ip-region --region us-central1
gcloud compute addresses describe datalayer-io-ip-region --region us-central1
```
