# Run a local OpenWPM crawl using Kubernetes

Documentation and scripts to launch an the crawl on a Kubernetes cluster locally.

For more detailed explanations about what is going on here, see [./openwpm-crawler/deployment/local/README.md](./openwpm-crawler/deployment/local/README.md).

## Prerequisites

Install Docker and Kubernetes locally. Note that
[Docker for Mac](https://docs.docker.com/docker-for-mac/install/) includes
[Kubernetes](https://docs.docker.com/docker-for-mac/#kubernetes). Depending on
your platform you may also need to install a local cluster (.e.g,
[Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/).

For the remainder of these instructions, you are assumed to be in the same folder as this readme.

## Prepare the stack and load the site list for the crawl

```
cd ./OpenWPM; docker build -t openwpm .; cd -
kubectl apply -f openwpm-crawler/deployment/local/localstack.yaml
kubectl apply -f openwpm-crawler/deployment/local/redis.yaml
./openwpm-crawler/deployment/load_site_list_into_redis.sh crawl-queue ../lists/crawl-seed-list.csv
```

## Start the crawl

```
kubectl create -f crawl.yaml
```

### Monitor the crawl

#### Queue status

Open a temporary instance and launch redis-cli:
```
kubectl exec -it redis-master -- sh -c "redis-cli -h redis"
```

Current length of the queue:
```
llen crawl-queue
```

Amount of queue items marked as processing:
```
llen crawl-queue:processing 
```

Contents of the queue:
```
lrange crawl-queue 0 -1
lrange crawl-queue:processing 0 -1
```

Or use [a web UI](https://github.com/joeferner/redis-commander) to inspect the contents of the queue:
```
kubectl apply -f https://raw.githubusercontent.com/motin/redis-commander/issue-360/k8s/redis-commander/deployment.yaml
kubectl apply -f https://raw.githubusercontent.com/motin/redis-commander/issue-360/k8s/redis-commander/service.yaml
kubectl port-forward svc/redis-commander 8081:8081
open http://localhost:8081/
```

#### OpenWPM progress and logs

Spin up the Kubernetes Dashboard UI as per [these instructions](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/#deploying-the-dashboard-ui):

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta1/aio/deploy/recommended.yaml
kubectl apply -f dashboard-adminuser.yaml
kubectl proxy
open http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

Use the `Token` method to authenticate. The token is given by:
```
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')
```

The crawl will be listed as a Job under Workloads -> Jobs. 

### Fetch the crawl data

When it has completed, run:
```
s3cmd --verbose --access_key=foo --secret_key=foo --host=http://localhost:32001 --host-bucket=localhost --no-ssl sync --delete-removed s3://localstack-foo local-crawl-results/data
```

The crawl data will end up in Parquet format in `./local-crawl-results/data`

### Clean up created pods, services and local artifacts

```
mkdir /tmp/empty
s3cmd --verbose --access_key=foo --secret_key=foo --host=http://localhost:32001 --host-bucket=localhost --no-ssl sync --delete-removed --force /tmp/empty/ s3://localstack-foo
kubectl delete -f crawl.yaml
kubectl delete -f openwpm-crawler/deployment/local/localstack.yaml
kubectl delete -f openwpm-crawler/deployment/local/redis.yaml
rm -r local-crawl-results/data
rm -r local-crawl-results/logs
```
