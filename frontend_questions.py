"""Common frontend developer interview topics expanded into 100 study prompts."""

from web_questions import build_library


FRONTEND_TOPICS = [
    ('frontend architecture', 'Frontend architecture organizes UI code into clear components, modules, state boundaries, and shared utilities.', 'Putting all UI, data fetching, and state in one component makes changes hard to test.'),
    ('component design', 'A component should have one clear responsibility, a predictable interface, and reusable behavior.', 'Making components overly generic too early can obscure their actual purpose.'),
    ('state management', 'State management defines where changing data lives and how UI updates consistently from it.', 'Duplicating the same state in several places creates synchronization bugs.'),
    ('client-side routing', 'Client-side routing maps URLs to views without a full document reload in a single-page application.', 'Routes still need server support for refreshes and deep links in production.'),
    ('data fetching', 'Data fetching handles loading, success, empty, and error states when requesting remote data.', 'Rendering only the success state leaves users without feedback during failures.'),
    ('HTTP APIs in the browser', 'Browser clients use fetch or an HTTP library to send requests, headers, credentials, and payloads to APIs.', 'Treating every non-200 response as the same error hides useful recovery actions.'),
    ('browser rendering', 'Browsers parse HTML and CSS, build rendering structures, lay out elements, then paint and composite pixels.', 'Forcing repeated layout reads and writes in a loop can make interfaces sluggish.'),
    ('the DOM', 'The DOM is the object representation of a document that JavaScript can query and update.', 'Directly mutating many nodes without a clear ownership model becomes difficult to reason about.'),
    ('event delegation', 'Event delegation places one handler on an ancestor and handles events from matching descendants.', 'Do not assume every event bubbles; choose event types and targets carefully.'),
    ('forms and validation', 'Good forms use labels, client-side hints, accessible errors, and server-side validation.', 'Client validation alone cannot protect data or enforce business rules.'),
    ('web accessibility', 'Accessibility makes interfaces usable with keyboards, screen readers, zoom, and different user needs.', 'Replacing native controls with divs often removes behavior users rely on.'),
    ('responsive design', 'Responsive design adapts layout and interaction to available space and device capabilities.', 'Testing only one desktop size misses mobile, zoom, and landscape problems.'),
    ('CSS layout', 'Flexbox is useful for one-dimensional alignment and Grid for two-dimensional layout.', 'Using fixed pixel sizes everywhere creates overflow on smaller screens.'),
    ('CSS specificity', 'Specificity determines which competing CSS selector wins when origin and importance are equal.', 'Using !important as a default makes future styling harder to maintain.'),
    ('design systems', 'A design system combines reusable components, design tokens, documentation, and usage standards.', 'A component library without shared guidance quickly becomes inconsistent.'),
    ('frontend performance', 'Performance work measures user experience and reduces unnecessary JavaScript, rendering work, and network cost.', 'Optimizing without measurement can miss the real bottleneck.'),
    ('code splitting', 'Code splitting loads JavaScript in smaller chunks, often by route or feature, to reduce initial work.', 'Splitting too aggressively can create many network requests and loading boundaries.'),
    ('image optimization', 'Image optimization selects appropriate dimensions, modern formats, compression, and lazy loading for noncritical images.', 'Lazy-loading a hero image can delay the largest contentful paint.'),
    ('web caching', 'Browser and CDN caching reuse safe responses according to cache headers and validation rules.', 'Caching personalized data without correct variation can expose one user data to another.'),
    ('frontend testing', 'Frontend testing combines unit, component, integration, and end-to-end tests around user-visible behavior.', 'Testing implementation details makes refactoring unnecessarily painful.'),
    ('cross-browser testing', 'Cross-browser testing verifies key journeys across supported browsers, devices, and assistive technologies.', 'Assuming a feature behaves identically everywhere causes production-only defects.'),
    ('web security', 'Frontend security includes preventing XSS, protecting tokens, using HTTPS, and treating external data as untrusted.', 'Rendering unsanitized user-provided HTML can enable cross-site scripting.'),
    ('content security policy', 'A Content Security Policy restricts where scripts, styles, and other resources may load from.', 'A policy that allows unsafe inline scripts provides much less protection.'),
    ('progressive enhancement', 'Progressive enhancement starts with a functional baseline and adds richer behavior when supported.', 'Making core actions depend entirely on JavaScript can exclude users during failures.'),
    ('error boundaries and recovery', 'Error boundaries and recovery states prevent one UI failure from breaking an entire user journey.', 'Hiding errors silently makes defects impossible for users and developers to understand.'),
]

FRONTEND_QUESTIONS = build_library(FRONTEND_TOPICS)
