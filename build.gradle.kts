plugins {
    id("java")
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    //testImplementation(platform("org.junit:junit-bom:5.9.1"))
   // testImplementation("org.junit.jupiter:junit-jupiter")
    implementation ("org.mariadb.jdbc:mariadb-java-client:3.3.3")
    testImplementation("org.projectlombok:lombok:1.18.28")
    compileOnly("javax.servlet:javax.servlet-api:4.0.1")

    // ✅ Lombok (핵심)
    compileOnly("org.projectlombok:lombok:1.18.32")
    annotationProcessor("org.projectlombok:lombok:1.18.32")

    testImplementation("org.junit.jupiter:junit-jupiter-api:5.10.2")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.10.2")

    implementation("com.zaxxer:HikariCP:5.1.0")
}


tasks.test {
    useJUnitPlatform()
}