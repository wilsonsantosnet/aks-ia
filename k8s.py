import json
from flask import Flask, jsonify
from kubernetes import client, config
from collections import OrderedDict

app = Flask(__name__)

# Variável global para armazenar a saída
output_data = {}

# Configurar acesso ao Kubernetes
config.load_kube_config()

# Instanciar clientes API
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
batch_v1 = client.BatchV1Api()
networking_v1 = client.NetworkingV1Api()
autoscaling_v1 = client.AutoscalingV1Api()

@app.route('/api/pods', methods=['GET'])
def get_pods():
    pods = v1.list_pod_for_all_namespaces(watch=False)
    pod_list = []
    for pod in pods.items:
        pod_info = OrderedDict([
            ('Pod Name', pod.metadata.name),
            ('Namespace', pod.metadata.namespace),
            ('Status', pod.status.phase),
            ('Node', pod.spec.node_name),
            ('Containers', [
            {
                'Container Name': container.name,
                'Image': container.image,
                'Ready': container.ready,
                'Restart Count': container.restart_count
            } for container in (pod.status.container_statuses or [])
            ]),
            ('Labels', pod.metadata.labels),
            ('Annotations', pod.metadata.annotations),
            ('Creation Timestamp', pod.metadata.creation_timestamp),
            ('IP', pod.status.pod_ip),
            ('Host IP', pod.status.host_ip),
            ('QoS Class', pod.status.qos_class),
            ('Node Selector', pod.spec.node_selector),
            ('Tolerations', [{'Key': toleration.key, 'Operator': toleration.operator, 'Value': toleration.value, 'Effect': toleration.effect} for toleration in (pod.spec.tolerations or [])]),
            ('Affinity', pod.spec.affinity.to_dict() if pod.spec.affinity else None),
            ('Volumes', [{'Name': volume.name, 'Type': type(volume).__name__} for volume in (pod.spec.volumes or [])]),
            ('Conditions', [{'Type': condition.type, 'Status': condition.status, 'Reason': condition.reason, 'Message': condition.message} for condition in (pod.status.conditions or [])]),
            ('Host Aliases', [{'IP': alias.ip, 'Hostnames': alias.hostnames} for alias in (pod.spec.host_aliases or [])]),
            ('Host Network', pod.spec.host_network),
            ('Host PID', pod.spec.host_pid),
            ('Host IPC', pod.spec.host_ipc),
            ('Security Context', pod.spec.security_context.to_dict() if pod.spec.security_context else None),
            ('Image Pull Secrets', [{'Name': secret.name} for secret in (pod.spec.image_pull_secrets or [])]),
            ('Service Account Name', pod.spec.service_account_name),
            ('Automount Service Account Token', pod.spec.automount_service_account_token),
            ('Priority', pod.spec.priority),
            ('Priority Class Name', pod.spec.priority_class_name),
            ('DNS Policy', pod.spec.dns_policy),
            ('DNS Config', pod.spec.dns_config.to_dict() if pod.spec.dns_config else None),
            ('Scheduler Name', pod.spec.scheduler_name),
            ('Init Containers', [
            {
                'Container Name': container.name,
                'Image': container.image,
                'Ready': container.ready,
                'Restart Count': container.restart_count
            } for container in (pod.status.init_container_statuses or [])
            ]),
            ('Ephemeral Containers', [
            {
                'Container Name': container.name,
                'Image': container.image,
                'Ready': container.ready,
                'Restart Count': container.restart_count
            } for container in (pod.status.ephemeral_container_statuses or [])
            ]),
            ('Overhead', pod.spec.overhead),
            ('Runtime Class Name', pod.spec.runtime_class_name),
            ('Topology Spread Constraints', [constraint.to_dict() for constraint in (pod.spec.topology_spread_constraints or [])]),
            ('Affinity', pod.spec.affinity.to_dict() if pod.spec.affinity else None),
            ('Priority', pod.spec.priority),
            ('Priority Class Name', pod.spec.priority_class_name),
            ('DNS Policy', pod.spec.dns_policy),
            ('DNS Config', pod.spec.dns_config.to_dict() if pod.spec.dns_config else None),
            ('Scheduler Name', pod.spec.scheduler_name)
        ])
        pod_list.append(pod_info)
    return jsonify(pod_list)
    nodes = v1.list_node()
    node_list = []
    for node in nodes.items:
        node_info = OrderedDict([
            ('Name', node.metadata.name),
            ('Status', node.status.conditions[-1].type if node.status.conditions else None),
            ('Addresses', [{'Type': addr.type, 'Address': addr.address} for addr in (node.status.addresses or [])]),
            ('Capacity', node.status.capacity),
            ('Allocatable', node.status.allocatable),
            ('OS Image', node.status.node_info.os_image),
            ('Kernel Version', node.status.node_info.kernel_version),
            ('Container Runtime Version', node.status.node_info.container_runtime_version),
            ('Kubelet Version', node.status.node_info.kubelet_version),
            ('Kube-Proxy Version', node.status.node_info.kube_proxy_version),
            ('Architecture', node.status.node_info.architecture),
            ('Operating System', node.status.node_info.operating_system),
            ('Pod CIDR', node.spec.pod_cidr),
            ('Provider ID', node.spec.provider_id),
            ('Taints', [{'Key': taint.key, 'Effect': taint.effect, 'Value': taint.value} for taint in (node.spec.taints or [])]),
            ('Conditions', [{'Type': condition.type, 'Status': condition.status, 'Reason': condition.reason, 'Message': condition.message} for condition in (node.status.conditions or [])]),
            ('Labels', node.metadata.labels),
            ('Annotations', node.metadata.annotations),
            ('Creation Timestamp', node.metadata.creation_timestamp),
            ('Kubelet Port', node.status.daemon_endpoints.kubelet_endpoint.port if node.status.daemon_endpoints.kubelet_endpoint else None),
            ('System UUID', node.status.node_info.system_uuid),
            ('daemonEndpoints', node.status.daemon_endpoints.to_dict() if node.status.daemon_endpoints else None),
            ('Images', [{'Names': image.names, 'SizeBytes': image.size_bytes} for image in (node.status.images or [])]),
            ('Info', node.status.node_info.to_dict() if node.status.node_info else None),
            ('Capacity', node.status.capacity),
            ('Unschedulable', node.spec.unschedulable),
        ])
        node_list.append(node_info)
    
    # Armazenar a saída na variável global
    output_data['nodes'] = node_list
    return jsonify(node_list)

@app.route('/api/deployments', methods=['GET'])
def get_deployments():
    deployments = apps_v1.list_deployment_for_all_namespaces(watch=False)
    deployment_list = []
    for deployment in deployments.items:
        deployment_info = OrderedDict([
            ('Name', deployment.metadata.name),
            ('Namespace', deployment.metadata.namespace),
            ('Replicas', deployment.spec.replicas),
            ('Available Replicas', deployment.status.available_replicas),
            ('Unavailable Replicas', deployment.status.unavailable_replicas),
            ('Labels', deployment.metadata.labels),
            ('Annotations', deployment.metadata.annotations),
            ('Creation Timestamp', deployment.metadata.creation_timestamp),
            ('Strategy', deployment.spec.strategy.to_dict() if deployment.spec.strategy else None),
            ('Min Ready Seconds', deployment.spec.min_ready_seconds),
            ('Revision History Limit', deployment.spec.revision_history_limit),
            ('Progress Deadline Seconds', deployment.spec.progress_deadline_seconds),
            ('Replicas', deployment.status.replicas),
            ('Updated Replicas', deployment.status.updated_replicas),
            ('Ready Replicas', deployment.status.ready_replicas),
            ('Conditions', [{'Type': condition.type, 'Status': condition.status, 'Reason': condition.reason, 'Message': condition.message} for condition in (deployment.status.conditions or [])]),
            ('Selector', deployment.spec.selector.match_labels),
            ('Template', deployment.spec.template.to_dict() if deployment.spec.template else None),
            ('Strategy', deployment.spec.strategy.to_dict() if deployment.spec.strategy else None),
            ('Status', deployment.status.to_dict() if deployment.status else None),
            ('Progress Deadline Seconds', deployment.spec.progress_deadline_seconds),
            ('Min Ready Seconds', deployment.spec.min_ready_seconds),
            ('Revision History Limit', deployment.spec.revision_history_limit),
            ('Paused', deployment.spec.paused),
            #('Rollback To', deployment.spec.rollback_to.to_dict() if deployment.spec.rollback_to else None),
            ('Progress Deadline Seconds', deployment.spec.progress_deadline_seconds),
            ('Min Ready Seconds', deployment.spec.min_ready_seconds),
            ('Revision History Limit', deployment.spec.revision_history_limit)
        ])
        deployment_list.append(deployment_info)
    return jsonify(deployment_list)

@app.route('/api/hpas', methods=['GET'])
def get_hpas():
    hpas = autoscaling_v1.list_horizontal_pod_autoscaler_for_all_namespaces(watch=False)
    hpa_list = []
    for hpa in hpas.items:
        hpa_info = OrderedDict([
          ('Name', hpa.metadata.name),
            ('Namespace', hpa.metadata.namespace),
            ('Min Replicas', hpa.spec.min_replicas),
            ('Max Replicas', hpa.spec.max_replicas),
            ('Current Replicas', hpa.status.current_replicas),
            ('Desired Replicas', hpa.status.desired_replicas),
            ('Target CPU Utilization Percentage', hpa.spec.target_cpu_utilization_percentage),
            ('Current CPU Utilization Percentage', hpa.status.current_cpu_utilization_percentage),
            # ('Target Memory Utilization', next((metric.resource.target.average_utilization for metric in hpa.spec.metrics if metric.type == 'Resource' and metric.resource.name == 'memory'), None)),
            # ('Current Memory Utilization', next((metric.resource.current.average_utilization for metric in hpa.status.current_metrics if metric.type == 'Resource' and metric.resource.name == 'memory'), None)),
            ('Creation Timestamp', hpa.metadata.creation_timestamp),
            ('Labels', hpa.metadata.labels),
            ('Annotations', hpa.metadata.annotations),
            #('Metrics', [{'Type': metric.type, 'Resource': metric.resource.to_dict() if metric.resource else None} for metric in (hpa.spec.metrics or [])]),
            #('Conditions', [{'Type': condition.type, 'Status': condition.status, 'Reason': condition.reason, 'Message': condition.message} for condition in (hpa.status.conditions or [])]),
            ('Last Scale Time', hpa.status.last_scale_time),
            ('Observed Generation', hpa.status.observed_generation),
        ])
        hpa_list.append(hpa_info)
    return jsonify(hpa_list)


@app.route('/api/services', methods=['GET'])
def get_services():
    services = v1.list_service_for_all_namespaces(watch=False)
    service_list = []
    for service in services.items:
        service_info = OrderedDict([
            ('Name', service.metadata.name),
            ('Namespace', service.metadata.namespace),
            ('Labels', service.metadata.labels),
            ('Annotations', service.metadata.annotations),
            ('Creation Timestamp', service.metadata.creation_timestamp),
            ('Cluster IP', service.spec.cluster_ip),
            ('External IPs', service.spec.external_i_ps),
            ('Ports', [{'Port': port.port, 'Target Port': port.target_port, 'Protocol': port.protocol} for port in (service.spec.ports or [])]),
            ('Selector', service.spec.selector),
            ('Type', service.spec.type),
            ('Session Affinity', service.spec.session_affinity),
            ('Load Balancer IP', service.spec.load_balancer_ip),
            ('Load Balancer Ingress', [{'IP': ingress.ip, 'Hostname': ingress.hostname} for ingress in (service.status.load_balancer.ingress or [])]),
        ])
        service_list.append(service_info)
    return jsonify(service_list)
            

@app.route('/api/ingresses', methods=['GET'])
def get_ingresses():
    ingresses = networking_v1.list_ingress_for_all_namespaces(watch=False)
    ingress_list = []
    for ingress in ingresses.items:
        ingress_info = OrderedDict([
            ('Name', ingress.metadata.name),
            ('Namespace', ingress.metadata.namespace),
            ('Labels', ingress.metadata.labels),
            ('Annotations', ingress.metadata.annotations),
            ('Creation Timestamp', ingress.metadata.creation_timestamp),
            ('Rules', [{'Host': rule.host, 'Paths': [{'Path': path.path, 'Backend': path.backend.service.name} for path in rule.http.paths]} for rule in (ingress.spec.rules or [])]),
            ('TLS', [{'Hosts': tls.hosts, 'Secret Name': tls.secret_name} for tls in (ingress.spec.tls or [])]),
            ('Load Balancer Ingress', [{'IP': ingress.ip, 'Hostname': ingress.hostname} for ingress in (ingress.status.load_balancer.ingress or [])]),
        ])
        ingress_list.append(ingress_info)
    return jsonify(ingress_list)

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    nodes = v1.list_node(watch=False)
    node_list = []
    for node in nodes.items:
        node_info = OrderedDict([
            ('Name', node.metadata.name),
            ('Status', node.status.conditions[-1].type if node.status.conditions else None),
            ('Addresses', [{'Type': addr.type, 'Address': addr.address} for addr in (node.status.addresses or [])]),
            ('Capacity', node.status.capacity),
            ('Allocatable', node.status.allocatable),
            ('OS Image', node.status.node_info.os_image),
            ('Kernel Version', node.status.node_info.kernel_version),
            ('Container Runtime Version', node.status.node_info.container_runtime_version),
            ('Kubelet Version', node.status.node_info.kubelet_version),
            ('Kube-Proxy Version', node.status.node_info.kube_proxy_version),
            ('Architecture', node.status.node_info.architecture),
            ('Operating System', node.status.node_info.operating_system),
            ('Pod CIDR', node.spec.pod_cidr),
            ('Provider ID', node.spec.provider_id),
            ('Taints', [{'Key': taint.key, 'Effect': taint.effect, 'Value': taint.value} for taint in (node.spec.taints or [])]),
            ('Conditions', [{'Type': condition.type, 'Status': condition.status, 'Reason': condition.reason, 'Message': condition.message} for condition in (node.status.conditions or [])]),
            ('Labels', node.metadata.labels),
            ('Annotations', node.metadata.annotations),
            ('Creation Timestamp', node.metadata.creation_timestamp),
            ('Kubelet Port', node.status.daemon_endpoints.kubelet_endpoint.port if node.status.daemon_endpoints.kubelet_endpoint else None),
            ('System UUID', node.status.node_info.system_uuid),
            ('daemonEndpoints', node.status.daemon_endpoints.to_dict() if node.status.daemon_endpoints else None),
            ('Images', [{'Names': image.names, 'SizeBytes': image.size_bytes} for image in (node.status.images or [])]),
            ('Info', node.status.node_info.to_dict() if node.status.node_info else None),
            ('Capacity', node.status.capacity),
            ('Unschedulable', node.spec.unschedulable),
        ])
        node_list.append(node_info)
    return jsonify(node_list)

@app.route('/api/replicasets', methods=['GET'])
def get_replicasets():
    replicasets = apps_v1.list_replica_set_for_all_namespaces(watch=False)
    replicaset_list = []
    for replicaset in replicasets.items:
        replicaset_info = OrderedDict([
            ('Name', replicaset.metadata.name),
            ('Namespace', replicaset.metadata.namespace),
            ('Replicas', replicaset.spec.replicas),
            ('Available Replicas', replicaset.status.available_replicas),
            ('Labels', replicaset.metadata.labels),
            ('Annotations', replicaset.metadata.annotations),
            ('Creation Timestamp', replicaset.metadata.creation_timestamp),
            ('Selector', replicaset.spec.selector.match_labels),
            ('Template', replicaset.spec.template.to_dict() if replicaset.spec.template else None),
        ])
        replicaset_list.append(replicaset_info)
    return jsonify(replicaset_list)

@app.route('/api/configmaps', methods=['GET'])
def get_configmaps():
    configmaps = v1.list_config_map_for_all_namespaces(watch=False)
    configmap_list = []
    for configmap in configmaps.items:
        configmap_info = OrderedDict([
            ('Name', configmap.metadata.name),
            ('Namespace', configmap.metadata.namespace),
            ('Data', configmap.data),
            ('Labels', configmap.metadata.labels),
            ('Annotations', configmap.metadata.annotations),
            ('Creation Timestamp', configmap.metadata.creation_timestamp),
        ])
        configmap_list.append(configmap_info)
    return jsonify(configmap_list)

@app.route('/api/secrets', methods=['GET'])
def get_secrets():
    secrets = v1.list_secret_for_all_namespaces(watch=False)
    secret_list = []
    for secret in secrets.items:
        secret_info = OrderedDict([
            ('Name', secret.metadata.name),
            ('Namespace', secret.metadata.namespace),
            ('Type', secret.type),
            ('Data', secret.data),
            ('Labels', secret.metadata.labels),
            ('Annotations', secret.metadata.annotations),
            ('Creation Timestamp', secret.metadata.creation_timestamp),
        ])
        secret_list.append(secret_info)
    return jsonify(secret_list)

@app.route('/api/persistentvolumes', methods=['GET'])
def get_persistentvolumes():
    pvs = v1.list_persistent_volume(watch=False)
    pv_list = []
    for pv in pvs.items:
        pv_info = OrderedDict([
            ('Name', pv.metadata.name),
            ('Capacity', pv.spec.capacity),
            ('Access Modes', pv.spec.access_modes),
            ('Reclaim Policy', pv.spec.persistent_volume_reclaim_policy),
            ('Status', pv.status.phase),
            ('Claim', pv.spec.claim_ref.name if pv.spec.claim_ref else None),
            ('Storage Class', pv.spec.storage_class_name),
            ('Labels', pv.metadata.labels),
            ('Annotations', pv.metadata.annotations),
            ('Creation Timestamp', pv.metadata.creation_timestamp),
        ])
        pv_list.append(pv_info)
    return jsonify(pv_list)

@app.route('/api/persistentvolumeclaims', methods=['GET'])
def get_persistentvolumeclaims():
    pvcs = v1.list_persistent_volume_claim_for_all_namespaces(watch=False)
    pvc_list = []
    for pvc in pvcs.items:
        pvc_info = OrderedDict([
            ('Name', pvc.metadata.name),
            ('Namespace', pvc.metadata.namespace),
            ('Status', pvc.status.phase),
            ('Capacity', pvc.status.capacity),
            ('Access Modes', pvc.status.access_modes),
            ('Storage Class', pvc.spec.storage_class_name),
            ('Labels', pvc.metadata.labels),
            ('Annotations', pvc.metadata.annotations),
            ('Creation Timestamp', pvc.metadata.creation_timestamp),
        ])
        pvc_list.append(pvc_info)
    return jsonify(pvc_list)

@app.route('/api/namespaces', methods=['GET'])
def get_namespaces():
    namespaces = v1.list_namespace(watch=False)
    namespace_list = []
    for namespace in namespaces.items:
        namespace_info = OrderedDict([
            ('Name', namespace.metadata.name),
            ('Status', namespace.status.phase),
            ('Labels', namespace.metadata.labels),
            ('Annotations', namespace.metadata.annotations),
            ('Creation Timestamp', namespace.metadata.creation_timestamp),
        ])
        namespace_list.append(namespace_info)
    return jsonify(namespace_list)

@app.route('/api/events', methods=['GET'])
def get_events():
    events = v1.list_event_for_all_namespaces(watch=False)
    event_list = []
    for event in events.items:
        event_info = OrderedDict([
            ('Name', event.metadata.name),
            ('Namespace', event.metadata.namespace),
            ('Reason', event.reason),
            ('Message', event.message),
            ('Type', event.type),
            ('Source', event.source.component),
            ('First Timestamp', event.first_timestamp),
            ('Last Timestamp', event.last_timestamp),
            ('Count', event.count),
            ('Labels', event.metadata.labels),
            ('Annotations', event.metadata.annotations),
            ('Creation Timestamp', event.metadata.creation_timestamp),
        ])
        event_list.append(event_info)
    return jsonify(event_list)

@app.route('/api/daemonsets', methods=['GET'])
def get_daemonsets():
    daemonsets = apps_v1.list_daemon_set_for_all_namespaces(watch=False)
    daemonset_list = []
    for daemonset in daemonsets.items:
        daemonset_info = OrderedDict([
            ('Name', daemonset.metadata.name),
            ('Namespace', daemonset.metadata.namespace),
            ('Desired Number Scheduled', daemonset.status.desired_number_scheduled),
            ('Current Number Scheduled', daemonset.status.current_number_scheduled),
            ('Number Available', daemonset.status.number_available),
            ('Number Unavailable', daemonset.status.number_unavailable),
            ('Labels', daemonset.metadata.labels),
            ('Annotations', daemonset.metadata.annotations),
            ('Creation Timestamp', daemonset.metadata.creation_timestamp),
            ('Selector', daemonset.spec.selector.match_labels),
            ('Template', daemonset.spec.template.to_dict() if daemonset.spec.template else None),
        ])
        daemonset_list.append(daemonset_info)
    return jsonify(daemonset_list)

@app.route('/api/statefulsets', methods=['GET'])
def get_statefulsets():
    statefulsets = apps_v1.list_stateful_set_for_all_namespaces(watch=False)
    statefulset_list = []
    for statefulset in statefulsets.items:
        statefulset_info = OrderedDict([
            ('Name', statefulset.metadata.name),
            ('Namespace', statefulset.metadata.namespace),
            ('Replicas', statefulset.spec.replicas),
            ('Ready Replicas', statefulset.status.ready_replicas),
            ('Current Replicas', statefulset.status.current_replicas),
            ('Updated Replicas', statefulset.status.updated_replicas),
            ('Labels', statefulset.metadata.labels),
            ('Annotations', statefulset.metadata.annotations),
            ('Creation Timestamp', statefulset.metadata.creation_timestamp),
            ('Selector', statefulset.spec.selector.match_labels),
            ('Template', statefulset.spec.template.to_dict() if statefulset.spec.template else None),
        ])
        statefulset_list.append(statefulset_info)
    return jsonify(statefulset_list)

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = batch_v1.list_job_for_all_namespaces(watch=False)
    job_list = []
    for job in jobs.items:
        job_info = OrderedDict([
            ('Name', job.metadata.name),
            ('Namespace', job.metadata.namespace),
            ('Completions', job.spec.completions),
            ('Parallelism', job.spec.parallelism),
            ('Active', job.status.active),
            ('Succeeded', job.status.succeeded),
            ('Failed', job.status.failed),
            ('Labels', job.metadata.labels),
            ('Annotations', job.metadata.annotations),
            ('Creation Timestamp', job.metadata.creation_timestamp),
        ])
        job_list.append(job_info)
    return jsonify(job_list)

@app.route('/api/cronjobs', methods=['GET'])
def get_cronjobs():
    cronjobs = batch_v1.list_cron_job_for_all_namespaces(watch=False)
    cronjob_list = []
    for cronjob in cronjobs.items:
        cronjob_info = OrderedDict([
            ('Name', cronjob.metadata.name),
            ('Namespace', cronjob.metadata.namespace),
            ('Schedule', cronjob.spec.schedule),
            ('Suspend', cronjob.spec.suspend),
            ('Active', len(cronjob.status.active)),
            ('Last Schedule Time', cronjob.status.last_schedule_time),
            ('Labels', cronjob.metadata.labels),
            ('Annotations', cronjob.metadata.annotations),
            ('Creation Timestamp', cronjob.metadata.creation_timestamp),
        ])
        cronjob_list.append(cronjob_info)
    return jsonify(cronjob_list)


# Continue modificando as outras rotas da mesma forma...

if __name__ == '__main__':
    app.run(debug=True)