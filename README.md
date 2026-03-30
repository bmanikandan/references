“Moodyʼs Innovation Approach
Absolutely. So I don't want to throw out any products or anything like that. The basis is really about the work and the cerebral nature that goes behind.
A lot of the great ideas that we have, that's none to my credit, it's a lot to our data scientists and to our engineers. One of the things that's been innovative is getting into the area of models. So everyone's talking about AI right now, and what that means for work in general.
A lot of times, LLMs or large language models, for those who may not have a technical background, are utilized to do workflow management, make sure you can wrap your head around large amounts of data so that you're not overwhelmed as a human being. What we're more interested in, and maybe it's because we're a data company filled with nerds and looking more at the analysis side of things, and of course me being an intelligence analyst previously, so kind of double downing on the analysis piece, is all about the reasoning. So there's another kind of LLM out there called Large Reasoning Model.
And what that's a fancy word for is essentially baking[…]”

From Innovation Storytellers: How Moody's is Rethinking AI in Finance, Mar 3, 2026
https://podcasts.apple.com/us/podcast/innovation-storytellers/id1565304950?i=1000752822674&r=846
This material may be protected by copyright.


# Copilot Instructions — Java 21 Spring Boot Reactive API

## Language & Runtime
- Java 21 — use modern language features (records, sealed interfaces, pattern matching, switch expressions, text blocks)
- Never use `var` for method return types or field declarations; local variables are fine
- Prefer records for DTOs, request/response objects, and immutable value types

## Framework & Libraries
- Spring Boot 3.x with Spring WebFlux (reactive stack)
- Project Reactor (`Mono`, `Flux`) for all async/non-blocking operations — never use blocking calls
- Spring Data R2DBC for database access (not JPA/Hibernate)
- MapStruct for object mapping between entities and DTOs
- Bean Validation (`jakarta.validation`) for input validation
- SpringDoc OpenAPI for API documentation
- Lombok is NOT used — use records and explicit constructors instead

## Architecture & Package Structure
- Follow hexagonal (ports & adapters) architecture:
  - `domain/` — entities, value objects, domain services, port interfaces
  - `application/` — use cases / application services
  - `adapter/in/web/` — REST controllers, request/response DTOs
  - `adapter/out/persistence/` — R2DBC repositories, persistence entities, mappers
  - `config/` — Spring configuration classes
- Keep domain layer free of Spring and framework annotations

## Reactive Patterns
- Return `Mono<T>` for single results, `Flux<T>` for collections
- Use `switchIfEmpty()` with deferred error signals instead of `.block()` or `.toFuture()`
- Chain operators — avoid deeply nested `flatMap` calls; extract to private methods
- Use `Mono.defer()` for lazy evaluation where needed
- Handle backpressure explicitly in `Flux` pipelines when consuming external sources
- Never call `.block()`, `.subscribe()`, or `.toFuture().get()` in production code

## REST API Conventions
- Use `@RestController` with `RouterFunction<ServerResponse>` only when routing logic is complex; otherwise prefer annotated controllers
- Return `ResponseEntity<Mono<T>>` or let Spring resolve `Mono<T>` / `Flux<T>` directly
- Use HTTP status codes correctly:
  - 201 Created for POST that creates a resource (include Location header)
  - 204 No Content for successful DELETE
  - 404 Not Found when resource doesn't exist
  - 409 Conflict for duplicate / constraint violations
  - 422 Unprocessable Entity for validation failures
- API paths: lowercase kebab-case, plural nouns (`/api/v1/order-items`)
- Version APIs via path prefix (`/api/v1/`)

## Error Handling
- Use a global `@ControllerAdvice` with `@ExceptionHandler` methods
- Define custom exception hierarchy extending a sealed `DomainException`:
```java
  public sealed class DomainException extends RuntimeException
      permits ResourceNotFoundException, DuplicateResourceException, ValidationException {}
```
- Return a consistent error response body:
```json
  {
    "status": 404,
    "error": "NOT_FOUND",
    "message": "Order with id 42 not found",
    "timestamp": "2025-01-15T10:30:00Z",
    "path": "/api/v1/orders/42"
  }
```
- Never expose stack traces or internal details in error responses

## Database & Persistence
- R2DBC with PostgreSQL
- Use `@Table` and `@Id` from Spring Data R2DBC (not JPA annotations)
- Entity classes are mutable POJOs in the persistence adapter — map to/from domain records
- Use Flyway for database migrations (`db/migration/V{number}__{description}.sql`)
- Repository interfaces extend `ReactiveCrudRepository` or `ReactiveSortingRepository`
- Write custom queries with `@Query` using native SQL, not JPQL

## Testing
- JUnit 5 for all tests
- Use `@WebFluxTest` for controller slice tests with `WebTestClient`
- Use `@DataR2dbcTest` with Testcontainers (PostgreSQL) for repository tests
- Use `StepVerifier` to assert reactive pipelines:
```java
  StepVerifier.create(orderService.findById(id))
      .expectNextMatches(order -> order.status() == Status.ACTIVE)
      .verifyComplete();
```
- Unit test domain logic with plain JUnit — no Spring context
- Use `Mockito` for mocking; prefer constructor injection for testability
- Test naming: `shouldReturnOrder_whenOrderExists()`

## Logging & Observability
- Use SLF4J (`LoggerFactory.getLogger(ClassName.class)`)
- Log at appropriate levels: ERROR for failures, WARN for recoverable issues, INFO for business events, DEBUG for flow tracing
- Add contextual info with Reactor Context and MDC propagation using `MdcContextLifter` or Micrometer context propagation
- Never log sensitive data (tokens, passwords, PII)

## Security
- Use Spring Security reactive (`SecurityWebFilterChain`)
- JWT-based authentication with stateless sessions
- Validate and sanitize all input at the controller layer
- Use `@PreAuthorize` or method-level security for authorization

## Code Style
- Max line length: 120 characters
- Prefer method references over lambdas when readable (`Order::id` over `o -> o.id()`)
- One class per file
- Order members: static fields, instance fields, constructors, public methods, private methods
- Write Javadoc on all public API classes and methods
