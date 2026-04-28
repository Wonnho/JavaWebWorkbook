plugins {
    id("java")
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    implementation ("org.mariadb.jdbc:mariadb-java-client:3.3.3")
    compileOnly("javax.servlet:javax.servlet-api:4.0.1")
}


tasks.test {
    useJUnitPlatform()
}