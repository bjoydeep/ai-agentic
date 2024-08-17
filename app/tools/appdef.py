from langchain.agents import tool

# This business of detecting the application topology is 
# a very complex one. What is shown here now is deployment topology
# What is not shown is application internal dependencies between pods etc.
# Those are very valuable when available. They can be surfaced from different sources
# NetworkObservability, Traces, KnowledgeGraphs etc
@tool
def appdef(query: str) -> dict:
    """
    This tool can find out details of application given the application name. 
    Do not try to pass on anything else like container name, secret name etc. 
    Only Application name should be used.
    """
    
    data = {
    "appname": [
        "retailbanking"
      ], 
    "clustername": [
        "cluster-1"
      ],         
      "deployment_my-app-deployment": [
        "pod_my-app-deployment-abc123",
        "pod_my-app-deployment-xyz456"
      ],
      "pod_my-app-deployment-abc123": [
        "container_app-container",
        "configmap_my-app-config",
        "secret_my-app-secret",
        "pvc_my-app-pvc"
      ],
      "pod_my-app-deployment-xyz456": [
        "container_app-container",
        "configmap_my-app-config",
        "secret_my-app-secret",
        "pvc_my-app-pvc"
      ],
      "service_my-app-service": [
        "pod_my-app-deployment-abc123",
        "pod_my-app-deployment-xyz456"
      ],
      "ingress_my-app-ingress": [
        "service_my-app-service"
      ]
    }
    return data