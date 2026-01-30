plugins {
    java
    id("org.springframework.boot") version "3.4.1"
    id("io.spring.dependency-management") version "1.1.7"
}

group = "com.example"
version = "1.0.0"

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

configurations {
    compileOnly {
        extendsFrom(configurations.annotationProcessor.get())
    }
}

repositories {
    mavenCentral()
}

dependencies {
    // Spring Boot Batch
    implementation("org.springframework.boot:spring-boot-starter-batch")
    
    // Spring Boot JDBC for Oracle connection
    implementation("org.springframework.boot:spring-boot-starter-jdbc")
    
    // Spring Boot Web (for REST API mode)
    implementation("org.springframework.boot:spring-boot-starter-web")
    
    // Oracle JDBC Driver
    implementation("com.oracle.database.jdbc:ojdbc11:23.4.0.24.05")
    
    // H2 for in-memory JobRepository
    runtimeOnly("com.h2database:h2")
    
    // Validation
    implementation("org.springframework.boot:spring-boot-starter-validation")
    
    // Lombok
    compileOnly("org.projectlombok:lombok")
    annotationProcessor("org.projectlombok:lombok")
    
    // Testing
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("org.springframework.batch:spring-batch-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.withType<Test> {
    useJUnitPlatform()
}

tasks.bootJar {
    archiveFileName.set("oracle-to-oracle-batch.jar")
}
