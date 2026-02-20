![assignment](https://imgur.com/gF8uyZJ.png)

### Created cluster in my local linux using few docs:


1) ***I have deployed all pods in my cluster , and i found adservice pod is crashing due to unable to pull the specified image in yaml file ```"gcr.io/google-samples/microservices-demo/adservice:v0.3.1```***
    ```
    ==> So i have followed the below steps
	1. edited the ad-service yaml file and changed image version to adservice:v0.3.4 and did a rollout restart deployment .
	2. now pod is running state 
    ```
2) ***Using kubectl port-forward connected to the frontend service and i found i'm able to open the UI but not able to order.***
    ```
	1. few pods are not running due to readiness  probe and liveness probe issues.
	2. i resolved the rediness and liveness probe issues changing initialdelayseconds,timeout seconds and etc (reffered few documents) and resolved those issues.
	3. now all pods are running 1/1 state
    ```

3) ***Pod redis-cart also failing due to nodeSelector issue***
    ```
	1.i have changed kubernetes.io/hostname: test-worker-2 to kubernetes.io/hostname=**qa-cluster-worker**
	2. and did a rollout restart , and pod got started running 1/1
    ```
4) ***Uploaded ```loadgenerator-output.txt``` in test folder***
