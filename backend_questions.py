"""Common backend developer interview topics expanded into 100 study prompts."""

from web_questions import build_library


BACKEND_TOPICS = [
    ('backend architecture', 'Backend architecture organizes services, data stores, integrations, and operational concerns around clear boundaries.', 'Creating tightly coupled services makes independent change and testing difficult.'),
    ('REST APIs', 'REST APIs expose resources with predictable URLs, HTTP methods, status codes, and stateless requests.', 'Returning HTTP 200 for every result makes client error handling unclear.'),
    ('API versioning', 'API versioning provides a safe path to evolve contracts without unexpectedly breaking clients.', 'Changing a widely used response field without a migration path breaks integrations.'),
    ('authentication', 'Authentication verifies who a caller is using credentials such as passwords, sessions, or tokens.', 'Trusting an identifier sent by the client without verification enables impersonation.'),
    ('authorization', 'Authorization decides whether an authenticated caller may perform a specific action on a resource.', 'Checking access only in the UI does not secure a backend endpoint.'),
    ('sessions and cookies', 'Sessions keep server-side user state while cookies commonly carry an opaque, protected session identifier.', 'Cookies need secure, HttpOnly, and appropriate SameSite settings.'),
    ('JSON Web Tokens', 'JWTs are signed tokens that carry claims and can support stateless authentication when validated carefully.', 'Putting sensitive data in a JWT is unsafe because its payload is readable by the holder.'),
    ('database normalization', 'Normalization organizes relational data to reduce duplication and update anomalies.', 'Over-normalizing every read path can create excessive joins without considering access patterns.'),
    ('database indexes', 'Indexes speed lookups and joins by maintaining an additional searchable structure for selected columns.', 'Adding indexes blindly slows writes and consumes storage.'),
    ('database transactions', 'Transactions make a group of operations succeed or fail together with isolation appropriate to the consistency need.', 'Leaving transactions open can block other work and exhaust connections.'),
    ('SQL injection prevention', 'Parameterized queries keep SQL code separate from untrusted values and prevent injection attacks.', 'Building SQL strings with user input allows malicious data to change the query.'),
    ('ORMs', 'An ORM maps application objects to database rows and can improve productivity for common operations.', 'Ignoring generated SQL can hide inefficient queries and N plus one problems.'),
    ('connection pooling', 'Connection pooling reuses a controlled number of database connections rather than opening one per request.', 'A pool that is too large can overwhelm the database under load.'),
    ('caching', 'Caching stores reusable results close to the caller to reduce latency and backend load.', 'Caching without invalidation or TTL strategy can return stale data indefinitely.'),
    ('cache invalidation', 'Cache invalidation updates or removes cached values when their source data changes.', 'Assuming a cache always updates itself leads to stale or inconsistent user experiences.'),
    ('message queues', 'Message queues decouple producers from asynchronous consumers and smooth bursts of work.', 'A queue consumer must handle duplicates because delivery is often at least once.'),
    ('background jobs', 'Background jobs run slow or retryable work outside the request path, such as email or report generation.', 'Doing long work synchronously can cause request timeouts and poor throughput.'),
    ('webhooks', 'Webhooks notify another system of an event by sending an HTTP request to its configured endpoint.', 'Webhook receivers must verify signatures, handle retries, and be idempotent.'),
    ('rate limiting', 'Rate limiting controls request volume to protect services and provide fair access.', 'Applying one global limit without considering identities or endpoints can block legitimate traffic.'),
    ('idempotency', 'Idempotency means repeating an operation has the same intended effect as performing it once.', 'Payment or creation endpoints without idempotency can duplicate side effects on retries.'),
    ('observability', 'Observability uses logs, metrics, traces, and alerts to understand production behavior.', 'Logging secrets or full personal data creates a security and privacy risk.'),
    ('health checks', 'Health checks signal whether a service can receive traffic and whether critical dependencies are available.', 'A shallow health check may report success while the application cannot serve real requests.'),
    ('Docker containers', 'Containers package an application and its dependencies into a reproducible runtime environment.', 'Storing configuration or secrets in an image makes them hard to rotate safely.'),
    ('CI/CD', 'Continuous integration validates changes automatically; continuous delivery or deployment promotes verified builds safely.', 'Deploying without automated checks or rollback planning makes incidents harder to recover from.'),
    ('backend testing', 'Backend testing covers business logic, API contracts, integration points, and failure conditions.', 'Tests that depend on shared mutable environments become flaky and unreliable.'),
]

BACKEND_QUESTIONS = build_library(BACKEND_TOPICS)
