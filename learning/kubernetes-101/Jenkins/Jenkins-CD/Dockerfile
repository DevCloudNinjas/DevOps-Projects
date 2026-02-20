# Dynamic build Jenkins Agent Pod to execute deployment steps
FROM amazonlinux
RUN yum install git -y && \
    yum install wget -y && \
    yum install tar -y && \
    yum install gzip -y 

RUN mkdir /root/.ssh && \
    mkdir -p /opt/java && \
    mkdir /opt/app
COPY ./id_rsa /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh && \
    chmod 600 /root/.ssh/id_rsa && \
    chown -R root:root /root/.ssh && \
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

RUN curl -LO https://dl.k8s.io/release/v1.22.0/bin/linux/amd64/kubectl && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/
RUN wget  https://get.helm.sh/helm-v3.7.0-linux-amd64.tar.gz && \
    tar xzf helm-v3.7.0-linux-amd64.tar.gz -C /tmp && \
    mv /tmp/linux-amd64/helm /usr/local/bin/ && \
    rm helm-v3.7.0-linux-amd64.tar.gz
RUN /usr/local/bin/helm plugin install https://github.com/belitre/helm-push-artifactory-plugin --version v0.3.0