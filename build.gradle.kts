plugins {
    id("java")
    id("org.gretty") version "4.1.1"
}

group = "org.workbook"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.9.1"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    compileOnly("javax.servlet:javax.servlet-api:4.0.1")
    implementation("jakarta.servlet:jakarta.servlet-api:5.0.0") // Use 5.0.0 for Jetty 11

}

tasks.test {
    useJUnitPlatform()
}