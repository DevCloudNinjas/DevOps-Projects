# Microservices

#### - The good, the bad and the ugly

---
## About me
### Frederik Mogensen

<div class="left-col-big">
Software Pilot at Trifork
<br>
<i>Focus on Docker, orchestration and ci/cd</i>
</div>
<div class="right-col-small">
![image](assets/images/me.jpeg)
</div>

---
## Clear definition of a microservice


- A small service that does one thing well
- Independent
- Owner of its own data

<small>https://blog.codeship.com/microservices-best-practices/</small>

---
## By Example

<div class="clearfix">
<div class="left-col">
![image](assets/images/musicshop.jpeg)
</div>
<div class="right-col">
![image](assets/images/microservice_architecture.png)
</div>
</div>

<small>https://martinfowler.com/articles/microservices.html</small>g 
<small>https://www.slideshare.net/spnewman/appsec-and-microservices</small>

---
# Microservices benefits

---
## Strong Module Boundaries

Microservices reinforce modular structure, which is particularly important for larger teams.


<small>https://martinfowler.com/microservices/</small>

---
## Independent Deployment

Simple services are easier to deploy, and since they are autonomous, are less likely to cause system failures when they go wrong.

<small>https://martinfowler.com/microservices/</small>

---
## Technology Diversity

With microservices you can mix multiple languages, development frameworks and data-storage technologies.


![image](assets/images/go.jpg)
![image](assets/images/java.jpg)
![image](assets/images/php.jpg)
![image](assets/images/cpp.jpg)
![image](assets/images/r.jpg)
![image](assets/images/dotnet.jpg)
![image](assets/images/python.jpg)

<small>https://martinfowler.com/microservices/</small>

---
# Microservices costs

---
## Distribution

- Distributed systems are harder to program
  - Calls between services are 
    - Slower 
    - Always at risk of failure.
    - Hard to follow through services


https://martinfowler.com/microservices/

---
## Eventual Consistency

Maintaining strong consistency is extremely difficult for a distributed system, which means everyone has to manage eventual consistency.

<small>https://martinfowler.com/microservices/</small>

---
## Operational Complexity

You need a mature operations team to manage lots of services.

![image](assets/images/microservice_graph.png)

<small>https://martinfowler.com/microservices/</small>

---
# Best Practices

---
## Helpful documentation

You no longer write the whole system and so you need to make it easy to integrate with the services.

<small>https://blog.codeship.com/microservices-best-practices/</small>

![image](assets/images/swagger.jpg)
![image](assets/images/appagi.jpg)

---
## Built with monitoring and troubleshooting in mind

Distributed systems easily becomes very complex and following requests is no longer just following stack traces.

<small>https://blog.codeship.com/microservices-best-practices/</small>


---
## Easily deployable and scalable

Deploying often and scaling the services when needed is a big benefit of using microservices.

![image](assets/images/swarm.png)
![image](assets/images/kubernetes.png)
![image](assets/images/mesos.png)

<small>https://blog.codeship.com/microservices-best-practices/</small>

---
## Easy to consume

Make sure your consumers can hit the API directly in a nonproduction environment.

- Develop
- Test
- Stable
- Production

<small>https://blog.codeship.com/microservices-best-practices/</small>

---
## Coexists with established conventions

- Make sure the microservices API is consistent and follow predefined conventions
  - Content format
  - Date format
  - Error responses
  - Etc…

<small>https://blog.codeship.com/microservices-best-practices/</small>

---
# Bad Practices

---
## Dictating the architecture

This interferes with product team’s responsibility which is one of the more important aspects of microservices and breaks the feedback loop from the actual code back to the design

<small>https://www.infoq.com/news/2015/01/bad-practices-microservices</small>

---
## A dedicated DBA or shared database

- A Prevents a team from 
  - optimizing their database structures
  - choosing the storage engine that best fits the for the specific service
- Approval needed - creates confusion about who owns the different tables
- Reluctance of removing anything in fear of destroying products for other teams.


<small>https://www.infoq.com/news/2015/01/bad-practices-microservices</small>

---
## A shared code base that is not owned by the teams

- The code must be shared by all teams with each developer able to send a pull request.
- Only utility logic should be shared
  - Sharing domain logic breaks the boundaries between contexts


<small>https://www.infoq.com/news/2015/01/bad-practices-microservices</small>

---
## Preferring SDKs over APIs

- Leads to one platform enforced on all teams
- SDKs introduces another level of complexity
  - Forcing a team to support both a service’ public API as well as the client code that uses the API.

<small>https://www.infoq.com/news/2015/01/bad-practices-microservices</small>

---
## Questions



