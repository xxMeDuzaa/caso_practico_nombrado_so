# Ejercicio 13 – Kubernetes

`inventory.yaml` define un Deployment (3 Pods) y un Service `inventory-service`; `orders.yaml` un Pod cliente que usa el nombre.

```powershell
kubectl apply -f inventory.yaml -f orders.yaml
kubectl get pods -o wide                       # IP de cada Pod
kubectl get svc inventory-service
kubectl exec orders -- nslookup inventory-service
kubectl exec orders -- wget -qO- http://inventory-service:8080/api/inventory/P001

kubectl delete pod -l app=inventory            # reemplaza los Pods (nuevas IP)
kubectl get pods -o wide
kubectl exec orders -- wget -qO- http://inventory-service:8080/api/inventory/P001   # el cliente no cambia

kubectl delete -f orders.yaml -f inventory.yaml
```

Requiere un clúster (Docker Desktop con Kubernetes, minikube o kind) y haber construido la imagen:

```powershell
docker build -f "..\Ejercicio 8\Dockerfile.inventory" -t inventory-service "..\Ejercicio 6\InventoryService"
# minikube: minikube image load inventory-service
```
