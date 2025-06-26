During today’s call, Tanveer primarily focused on building components for the header elements, such as the logo and utility menu items. He mentioned that his focus this week will shift to developing the navigation components.

If the header section is completed and ready for integration, the backend team can proceed without any interruptions. In the meantime, while waiting for Whisgy to finalize the navigation components, is there any existing menu component we can begin working with as a placeholder or starting point?


Subject: Migration to JDK 21, Spring Boot 3.5.3, and Gradle 8.14

Hello Team,

As of today, it is advisable to migrate all APP repositories to the following updated technology stack to ensure long-term compatibility, improved performance, and access to the latest security and feature enhancements:
	•	JDK 21
	•	Spring Boot v3.5.3
	•	Gradle 8.14

All deployments should utilize the JDK 21 CI/CD pipeline moving forward.

⸻

Required Changes

To support this migration, the following updates are required:
	1.	Update JDK Version
	•	Modify build.gradle or .tool-versions to use JDK 21
	•	Ensure the CI/CD pipeline (e.g., GitHub Actions, GitLab CI, Jenkins) is configured to run with JDK 21
	2.	Upgrade Spring Boot
	•	Update spring-boot dependencies in build.gradle.kts or pom.xml to 3.5.3
	•	Verify compatibility of existing code with Spring Boot 3.x (noting that 3.x is based on Jakarta EE 10)
	3.	Update Gradle
	•	Upgrade to Gradle 8.14 in gradle-wrapper.properties
	•	Run ./gradlew wrapper --gradle-version 8.14 to regenerate wrapper files
	4.	Dependency Review
	•	Review all external dependencies for compatibility with JDK 21 and Spring Boot 3.5.3
	•	Update or replace deprecated or incompatible libraries
	5.	Refactor Deprecated APIs
	•	Identify and refactor usages of deprecated APIs as per new JDK or Spring Boot changes
	6.	Re-run Tests
	•	Execute unit, integration, and regression tests to ensure compatibility and stability
	•	Address any test failures arising due to migration
	7.	CI/CD Pipeline Alignment
	•	Ensure the pipeline builds and deploys using JDK 21 runtime
	•	Update Dockerfiles or runtime images to base on JDK 21 if applicable
	8.	Documentation
	•	Update internal documentation and README files to reflect new versions
	•	Inform stakeholders of potential impacts during the upgrade window

⸻

Please begin planning the migration in coordination with your respective teams. If you encounter blockers or need assistance, feel free to reach out.

Best regards,
[Your Name]
