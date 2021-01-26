#!/usr/bin/python3
from flask import Flask, render_template
from kubernetes import client, config
import os
app = Flask(__name__)

@app.route("/")
def containers():
    outputjson = {}
    outputjson['items'] = []
    clustername = os.environ['CLUSTER_NAME']
    mypodname = os.environ['HOSTNAME']
    #clustername = "newcluster"
    #mypodname = "newpod"

    ##### Uncomment if running outside of the K8s cluster
    #config.load_kube_config()
    
    ##### Uncomment if running inside of the K8s cluster
    config.load_incluster_config()
    
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for pod in ret.items:
        namespace = pod.metadata.namespace
        podname = pod.metadata.name
        pod_status = pod.status.phase
        host_ip = pod.status.host_ip
        pod_ip = pod.status.pod_ip
        containers = pod.status.container_statuses
        for container in containers:
            name = container.name
            image = container.image
            image_id = str(container.image_id).lstrip('@')
            container_status = container.ready
            outputjson['items'].append({
                'clustername': clustername,
                'execpodname': mypodname,
                'pod_namespace': namespace,
                'pod_name': podname,
                'pod_host_ip': host_ip,
                'pod_ip': pod_ip,
                'pod_status': pod_status,
                'container_name': name,
                'container_image': image,
                'container_image_id': image_id,
                'container_status': container_status
            })
    return outputjson

@app.route("/getpod/")
def containers_grid():
    outputjson = {}
    outputjson['items'] = []
    clustername = os.environ['CLUSTER_NAME']
    mypodname = os.environ['HOSTNAME']
    #clustername = "newcluster"
    #mypodname = "newpod"

    ##### Uncomment if running outside of the K8s cluster
    #config.load_kube_config()
    
    ##### Uncomment if running inside of the K8s cluster
    config.load_incluster_config()
    
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for pod in ret.items:
        namespace = pod.metadata.namespace
        podname = pod.metadata.name
        pod_status = pod.status.phase
        host_ip = pod.status.host_ip
        pod_ip = pod.status.pod_ip
        containers = pod.status.container_statuses
        for container in containers:
            name = container.name
            image = container.image
            image_id = container.image_id
            container_status = container.ready
            outputjson['items'].append({
                'clustername': clustername,
                'execpodname': mypodname,
                'pod_namespace': namespace,
                'pod_name': podname,
                'pod_host_ip': host_ip,
                'pod_ip': pod_ip,
                'pod_status': pod_status,
                'container_name': name,
                'container_image': image,
                'container_image_id': image_id,
                'container_status': container_status
            })
    return render_template('pods.html', result = outputjson, cluster=clustername, podname=mypodname)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
