plugins {
    id("java")

    id("war")
}

group = "org.workbook"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    compileOnly("javax.servlet:javax.servlet-api:4.0.1")

    implementation("javax.servlet:jstl:1.2")
}


tasks.test {
    useJUnitPlatform()
}
