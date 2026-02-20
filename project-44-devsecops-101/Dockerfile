FROM adoptopenjdk/openjdk11:alpine-slim as build
WORKDIR /app

COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY src src

RUN ./mvnw package
COPY target/*.jar app.jar

FROM adoptopenjdk/openjdk11:alpine-slim
VOLUME /tmp
RUN addgroup --system javauser && adduser -S -s /bin/false -G javauser javauser
WORKDIR /app
COPY --from=build /app/app.jar .
RUN chown -R javauser:javauser /app
USER javauser
ENTRYPOINT ["java","-jar","app.jar"]
