# Web Services and Cloud-Based Systems - Assignment 3.2 (Kubernetes deployment of web services)
## Group 16 (Neeraj, Prashanth, Vignesh)

Deployment of both URL shortner web service and Login web service on kube cluster. As a bonus we implemented the ngnix proxy where
only one entry point can be used to access both services.

To deploy the serivces we need to push the docker containers from Assignment 3.1 to the docker hub. We created all three images for the
services url-shortner, Login web service and One entry point service.

`url-shortner -> neerajs1995/url-shortner:tagname`

 https://hub.docker.com/repository/docker/neerajs1995/url-shortner

`login-web-service -> neerajs1995/authenticator`

https://hub.docker.com/repository/docker/neerajs1995/authenticator

`ngnix-one-entry-point -> neerajs1995/assignment2`

https://hub.docker.com/repository/docker/neerajs1995/assignment2

This is the architechture of kubernetes deployment we deployed

![Kubernetes architechture](https://raw.githubusercontent.com/cymtrick/url-shortner-python/master/kube-deployment/photo_2020-05-12%2014.52.09.jpeg)

          [1] client connects to the load balancer via a public IP address
          
Kubeadm is used to manage the clusters. We have One master node(145.100.131.111) and two worker nodes(145.100.131.141,145.100.131.148).

For iptables to see the bridged traffic we need to set `net.bridge.bridge-nf-call-iptables` is set to `1` in sysctl config

````bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
````

Refernces:

[1] https://medium.com/google-cloud/understanding-kubernetes-networking-ingress-1bc341c84078




