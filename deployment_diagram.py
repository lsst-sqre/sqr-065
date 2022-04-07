from diagrams import Cluster
from diagrams.k8s.compute import Deployment, Pod
from diagrams.k8s.network import Service, Ingress
from diagrams.onprem.inmemory import Redis
from sphinx_diagrams import SphinxDiagram


graph_config = {
    "fontsize": "24",
    "labelfontsize": "24",
}

node_config = {
    "fontsize": "18",
    "labelfontsize": "24",
}

edge_config = {
    "penwidth": "2",
}

cluster_config = {
    "fontsize": "24"
}


with SphinxDiagram(
    title="Noteburst",
    graph_attr=graph_config,
    node_attr=node_config,
    edge_attr=edge_config
):
    with Cluster("RSP", graph_attr=cluster_config):
        ingress = Ingress("Ingress")

        with Cluster("Noteburst", graph_attr=cluster_config):
            noteburst_service = Service("Service")
            noteburst_redis = Redis("Redis")
            noteburst_api_deployment = Deployment("API")
            noteburst_worker_deployment = Deployment("Worker")
            noteburst_worker_pod1 = Pod("Worker 1")
            noteburst_worker_pod2 = Pod("Worker 2")

            ingress >> noteburst_service
            noteburst_service >> noteburst_api_deployment

            noteburst_worker_deployment - noteburst_worker_pod1
            noteburst_worker_deployment - noteburst_worker_pod2

            noteburst_api_deployment >> noteburst_redis
            noteburst_worker_pod1 >> noteburst_redis
            noteburst_worker_pod2 >> noteburst_redis

        with Cluster("Nublado", graph_attr=cluster_config):
            hub_service = Service("JupyterHub")
            jupyterlab_pod_1 = Pod("JupyterLab 1")
            jupyterlab_pod_2 = Pod("JupyterLab 2")

            hub_service >> jupyterlab_pod_1
            hub_service >> jupyterlab_pod_2

        noteburst_worker_pod1 >> hub_service
        noteburst_worker_pod2 >> hub_service
