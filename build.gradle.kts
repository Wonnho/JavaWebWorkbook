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

//log4j2 under test env
    testCompileOnly("org.projectlombok:lombok:1.18.24")
    testAnnotationProcessor("org.projectlombok:lombok:1.18.24")

    implementation("com.zaxxer:HikariCP:5.1.0")

    implementation("org.modelmapper:modelmapper:3.2.0")

    //log4j2
    implementation("org.apache.logging.log4j:log4j-api:2.22.1")
    implementation("org.apache.logging.log4j:log4j-core:2.22.1")
    implementation("org.apache.logging.log4j:log4j-slf4j2-impl:2.22.1")


}


tasks.test {
    useJUnitPlatform()
}