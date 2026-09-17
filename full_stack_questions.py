"""Common full-stack developer interview topics expanded into 100 prompts."""

from web_questions import build_library


FULL_STACK_TOPICS = [
    ('full-stack development', 'Full-stack development spans frontend UI, backend services, databases, APIs, testing, and deployment.', 'Claiming equal depth in every layer instead of describing real strengths and tradeoffs sounds unconvincing.'),
    ('REST APIs', 'REST APIs model resources with HTTP methods, status codes, stateless requests, and predictable URLs.', 'Using HTTP 200 for every outcome makes client error handling unclear.'),
    ('HTTP methods', 'GET reads, POST creates, PUT replaces, PATCH partially updates, and DELETE removes a resource.', 'Using a destructive action behind GET breaks caching and user expectations.'),
    ('HTTP status codes', 'Status codes communicate outcomes such as 200 success, 201 created, 400 bad request, 401 unauthenticated, and 404 missing.', 'Returning vague server errors for invalid client input makes debugging harder.'),
    ('authentication', 'Authentication verifies identity using sessions, tokens, OAuth, or similar mechanisms.', 'Storing secrets or long-lived tokens in unsafe client-side locations creates security risk.'),
    ('authorization', 'Authorization decides which authenticated user may perform an action or access a resource.', 'Checking authorization only in the UI does not protect the backend endpoint.'),
    ('JWTs', 'JSON Web Tokens are signed claims often used for stateless authentication.', 'Treating a JWT payload as secret or failing to validate signature and expiry is unsafe.'),
    ('cookies and sessions', 'Cookies can hold a session identifier while server-side storage keeps session state.', 'Missing secure, HttpOnly, and SameSite cookie settings can expose sessions to attacks.'),
    ('CORS', 'Cross-Origin Resource Sharing controls which origins may access browser-protected resources.', 'Using a wildcard origin with credentials is insecure and often invalid.'),
    ('SQL databases', 'Relational databases use tables, constraints, transactions, joins, and indexes for structured data.', 'Building queries through string concatenation enables SQL injection.'),
    ('NoSQL databases', 'NoSQL databases use flexible models such as documents, key-value records, or graphs for certain access patterns.', 'Choosing NoSQL only because schemas can change ignores consistency and query needs.'),
    ('database indexes', 'Indexes speed selected reads but consume storage and slow writes.', 'Adding indexes without reading query plans can waste resources or miss the real bottleneck.'),
    ('database transactions', 'Transactions group operations so they commit together or roll back together under defined isolation rules.', 'Updating related records without a transaction can leave inconsistent data after failures.'),
    ('caching', 'Caching stores reusable results closer to consumers to reduce latency and backend load.', 'Caching without invalidation or TTL strategy can serve incorrect stale data.'),
    ('message queues', 'Queues decouple producers from asynchronous workers for background jobs and resilient processing.', 'Assuming exactly-once delivery without idempotent consumers can cause duplicate effects.'),
    ('webhooks', 'Webhooks notify another service by sending HTTP requests when events occur.', 'Not verifying signatures or handling retries makes webhook integrations unsafe and unreliable.'),
    ('file uploads', 'File upload systems validate type and size, store files safely, and serve them through controlled URLs.', 'Trusting a filename or client-provided MIME type can enable dangerous uploads.'),
    ('environment variables', 'Environment variables keep deployment-specific configuration and secrets outside source code.', 'Committing .env files or secrets to Git exposes credentials.'),
    ('Docker containers', 'Containers package an app and its dependencies into a consistent deployable unit.', 'Putting secrets into an image or running as root creates avoidable production risk.'),
    ('CI/CD', 'Continuous integration tests changes automatically; continuous delivery or deployment releases validated changes.', 'Deploying without tests, rollback plans, or environment checks makes failures costly.'),
    ('logging and monitoring', 'Logging records events while monitoring tracks health, errors, performance, and alerts.', 'Logging passwords, API keys, or personal data creates a security and privacy issue.'),
    ('testing pyramid', 'A balanced test suite emphasizes fast unit tests, targeted integration tests, and fewer end-to-end tests.', 'Relying only on brittle end-to-end tests makes feedback slow and debugging difficult.'),
    ('frontend state management', 'State management coordinates local UI state, server data, and shared application state.', 'Putting all state in one global store creates unnecessary coupling and re-renders.'),
    ('responsive web design', 'Responsive design adapts layout and interaction to varied screen sizes and capabilities.', 'Testing only a desktop viewport misses mobile, zoom, and accessibility needs.'),
    ('web security', 'Web security includes input validation, parameterized queries, output encoding, CSRF protection, and least privilege.', 'Treating client validation as a security boundary leaves APIs vulnerable.'),
]

FULL_STACK_QUESTIONS = build_library(FULL_STACK_TOPICS)
