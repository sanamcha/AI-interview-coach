"""HTML and CSS interview libraries expanded into 100 focused study prompts each."""


def build_library(topics):
    """Create definition, use, pitfall, and accessibility/performance prompts per topic."""
    questions = []
    for topic, answer, pitfall in topics:
        questions.extend([
            ('What is {}?'.format(topic), answer),
            ('When would you use {}?'.format(topic), 'Use it when its semantics match the content or behavior. Explain a small real example and why it is preferable to an alternative.'),
            ('What is a common mistake with {}?'.format(topic), pitfall),
            ('How would you explain {} in a code review?'.format(topic), 'Describe its purpose, the tradeoff, and how you would verify the result for users, including keyboard and mobile users where relevant.'),
        ])
    return questions


HTML_TOPICS = [
    ('the <!DOCTYPE html> declaration', 'It tells browsers to use standards mode for an HTML document.', 'Omitting it can trigger legacy quirks mode and inconsistent layout.'),
    ('semantic HTML', 'It uses elements such as main, nav, article, and button to express meaning, not only appearance.', 'Using generic div elements for controls removes useful meaning and behavior.'),
    ('the head element', 'It contains document metadata, title, linked resources, and other information not displayed as page content.', 'Putting visible page content in head creates invalid document structure.'),
    ('the viewport meta tag', 'It controls mobile viewport sizing; a common value is width=device-width, initial-scale=1.', 'Without it, mobile browsers may render the page at desktop width.'),
    ('heading hierarchy', 'Headings communicate document structure, starting with a clear h1 and nested levels.', 'Choosing headings only for font size creates confusing structure for assistive technology.'),
    ('the alt attribute', 'It provides a text alternative for meaningful images.', 'Decorative images should use empty alt text rather than repeating nearby text.'),
    ('accessible links', 'A link should have descriptive text that explains its destination or action.', 'Avoid vague text such as click here when the context is not clear.'),
    ('the button element', 'It represents an action performed on the current page.', 'Do not use a div or anchor as a button without implementing all button behavior.'),
    ('forms', 'Forms collect and submit user input through controls, labels, validation, and an action.', 'Relying only on placeholders leaves inputs without persistent accessible labels.'),
    ('label elements', 'A label gives an input an accessible name and enlarges its clickable target.', 'A visual label not associated with an input does not provide the same accessibility benefit.'),
    ('input types', 'Types such as email, password, date, and number communicate expected data and enable useful browser behavior.', 'Using text for every field misses validation and mobile keyboard benefits.'),
    ('native form validation', 'Attributes such as required, minlength, and type provide browser validation before submit.', 'Client validation improves UX but never replaces server-side validation.'),
    ('fieldset and legend', 'They group related form controls and give the group an accessible label.', 'A div heading does not always communicate a form group relationship.'),
    ('tables', 'Tables represent two-dimensional tabular data with rows and columns.', 'Do not use tables for page layout; use CSS layout tools instead.'),
    ('table headers', 'th and scope identify row or column headers so users can understand data relationships.', 'Using only td cells makes complex tables difficult to navigate with a screen reader.'),
    ('audio and video', 'HTML media elements provide native playback controls, tracks, and fallback content.', 'Autoplay with sound is disruptive; captions are needed for spoken content.'),
    ('the picture element', 'It selects responsive image sources based on media conditions or formats.', 'Use img inside picture and still provide meaningful alternative text.'),
    ('lazy loading images', 'loading="lazy" defers offscreen image loading to improve initial page performance.', 'Do not lazy-load the main above-the-fold image because it can delay the largest contentful paint.'),
    ('iframe elements', 'An iframe embeds another document, such as a map or third-party widget.', 'Use title and restrictive sandbox or permissions settings when appropriate.'),
    ('data attributes', 'data-* attributes store custom data for scripts without inventing invalid attributes.', 'Do not store sensitive information in the DOM because users can inspect it.'),
    ('ARIA', 'ARIA adds accessibility semantics when native HTML cannot express the needed behavior.', 'No ARIA is better than incorrect ARIA; prefer native semantic elements first.'),
    ('landmark elements', 'Elements such as header, nav, main, aside, and footer provide page regions for assistive navigation.', 'Multiple landmarks need clear labels when their purposes differ.'),
    ('the lang attribute', 'It identifies the document language so screen readers and browsers choose correct pronunciation and behavior.', 'Forgetting lang harms pronunciation and translation tools.'),
    ('script loading', 'defer runs scripts after parsing while preserving order; async runs independently when downloaded.', 'Blocking scripts in head can delay rendering when defer is more suitable.'),
    ('HTML document structure', 'A valid document has html, head, and body elements with correctly nested content.', 'Invalid nesting can cause browsers to repair markup in unexpected ways.'),
]

CSS_TOPICS = [
    ('the CSS cascade', 'The cascade resolves competing declarations using origin, importance, specificity, and source order.', 'Adding !important repeatedly makes future styling harder to maintain.'),
    ('specificity', 'Specificity is the selector weight used when competing rules have the same origin and importance.', 'Overly specific selectors make component overrides difficult.'),
    ('the box model', 'Every element has content, padding, border, and margin that determine its occupied space.', 'Forgetting padding and borders affect width causes layout surprises.'),
    ('box-sizing: border-box', 'It includes padding and border inside the declared width and height.', 'Mixing sizing assumptions across components leads to overflow bugs.'),
    ('display block and inline', 'Block elements start new lines; inline elements flow with text and have limited sizing behavior.', 'Trying to set width on a normal inline element often has no visible effect.'),
    ('Flexbox', 'Flexbox lays out items along one dimension with alignment, spacing, and flexible sizing controls.', 'Using fixed widths everywhere prevents responsive shrinking and wrapping.'),
    ('CSS Grid', 'Grid lays out items in rows and columns and is ideal for two-dimensional page structure.', 'Using Grid for a simple one-dimensional alignment problem can add unnecessary complexity.'),
    ('position relative', 'It keeps an element in normal flow while allowing offset positioning and an anchor for absolute children.', 'Offsets do not reserve new layout space, so overuse can create overlap.'),
    ('position absolute', 'It removes an element from normal flow and positions it relative to a positioned ancestor.', 'Without an intended positioned ancestor it may be placed relative to the page.'),
    ('position fixed', 'It positions an element relative to the viewport, commonly for persistent controls.', 'Fixed content can obscure page content unless spacing and accessibility are considered.'),
    ('position sticky', 'It behaves normally until a threshold, then sticks within its scrolling container.', 'Sticky can fail when an ancestor has unsuitable overflow or no threshold such as top.'),
    ('z-index', 'z-index controls stacking order within stacking contexts.', 'Increasing z-index blindly fails when elements belong to different stacking contexts.'),
    ('CSS units', 'px is fixed CSS pixels; rem follows root font size; em follows current font size; percent follows a containing value.', 'Using only fixed pixels can reduce zoom and responsive flexibility.'),
    ('responsive design', 'Responsive design adapts layout and content to available space, input type, and user preferences.', 'Designing only at one desktop width leaves mobile and zoom users behind.'),
    ('media queries', 'Media queries apply styles based on features such as width, motion preference, or color scheme.', 'Do not rely only on device names; target capabilities and layout breakpoints.'),
    ('container queries', 'Container queries style a component based on its container size rather than the viewport.', 'They require a declared query container and thoughtful component boundaries.'),
    ('CSS custom properties', 'Custom properties store reusable values and can be changed by scope or media queries.', 'They are not preprocessor variables; their runtime cascade is a feature to understand.'),
    ('inheritance', 'Some properties, such as color and font-family, inherit while most layout properties do not.', 'Assuming every property inherits causes confusing component styling.'),
    ('overflow', 'Overflow controls what happens when content exceeds its box: visible, hidden, scroll, or auto.', 'Hidden overflow can accidentally clip focus outlines or dropdown menus.'),
    ('transitions', 'Transitions animate property changes over a duration and timing function.', 'Avoid animating layout-heavy properties when transform or opacity can achieve the effect.'),
    ('animations', 'Keyframe animations define multiple stages of a visual change.', 'Respect prefers-reduced-motion for users who minimize motion.'),
    ('transforms', 'Transform changes visual position, scale, rotation, or skew without normal document reflow.', 'Transforms can create stacking contexts and make fixed-position descendants behave differently.'),
    ('CSS performance', 'Efficient CSS uses simple maintainable selectors and favors composited animations such as transform and opacity.', 'Premature micro-optimization is less useful than measuring actual rendering issues.'),
    ('BEM naming', 'BEM names blocks, elements, and modifiers to make component ownership and variants clear.', 'A naming convention helps only when the team applies it consistently.'),
    ('CSS reset', 'A reset or normalization stylesheet reduces inconsistent browser default styles.', 'Removing all defaults without restoring useful focus and semantic styles harms usability.'),
]

HTML_QUESTIONS = build_library(HTML_TOPICS)
CSS_QUESTIONS = build_library(CSS_TOPICS)

JAVASCRIPT_TOPICS = [
    ('JavaScript scope', 'Scope determines where a variable can be accessed; JavaScript has global, function, module, and block scope.', 'Using var unintentionally creates function-scoped variables where block scope was expected.'),
    ('var, let, and const', 'var is function-scoped; let and const are block-scoped; const prevents rebinding but not object mutation.', 'Using var in modern code can create surprising hoisting and scope behavior.'),
    ('hoisting', 'Declarations are processed before execution; var is initialized as undefined while let and const stay in a temporal dead zone.', 'Do not rely on hoisting for readability; declare values before using them.'),
    ('the temporal dead zone', 'It is the period before a let or const declaration is initialized when access throws an error.', 'Assuming let behaves like var leads to runtime reference errors.'),
    ('closures', 'A closure is a function that retains access to lexical variables after its outer function has returned.', 'Closures can retain unnecessary memory when long-lived callbacks capture large objects.'),
    ('this', 'this is determined by how a regular function is called; arrow functions capture lexical this.', 'Passing an unbound method as a callback can lose its intended this value.'),
    ('arrow functions', 'Arrow functions have concise syntax and lexical this, but cannot be used as constructors.', 'Do not use an arrow when you need a dynamic this, arguments object, or constructor.'),
    ('prototypes', 'Objects can inherit behavior through a prototype chain, which JavaScript searches for missing properties.', 'Mutating shared prototypes can affect unrelated objects and libraries.'),
    ('classes', 'Classes are syntax built on prototypes that provide constructors, methods, inheritance, and private fields.', 'Class syntax does not remove the need to understand this and prototype behavior.'),
    ('promises', 'A Promise represents an eventual asynchronous result with pending, fulfilled, or rejected states.', 'Always handle rejection paths to avoid unhandled promise errors.'),
    ('async and await', 'async functions return promises; await pauses that function until a promise settles.', 'Sequential awaits can be slower than Promise.all when independent work can run concurrently.'),
    ('the event loop', 'The event loop coordinates the call stack, task queue, and microtask queue for asynchronous JavaScript.', 'Long synchronous work blocks the UI and delays queued callbacks.'),
    ('microtasks and macrotasks', 'Promise callbacks are microtasks and generally run before the next task such as a setTimeout callback.', 'Misunderstanding queue order can cause timing bugs in async code.'),
    ('event delegation', 'A parent listener handles events from child elements through bubbling, reducing listeners for dynamic lists.', 'Check event.target carefully so unrelated nested elements do not trigger the wrong action.'),
    ('event bubbling', 'An event normally travels from its target through ancestor elements.', 'Calling stopPropagation too broadly can break parent behavior and analytics.'),
    ('DOM manipulation', 'The DOM API reads, creates, updates, and removes document elements from JavaScript.', 'Repeated direct DOM changes can cause layout work; batch updates when performance matters.'),
    ('destructuring', 'Destructuring extracts properties or array items into variables with concise syntax.', 'A missing nested object can throw unless defaults or optional chaining are used.'),
    ('spread syntax', 'Spread expands an iterable or object, commonly for copying and combining values.', 'It creates a shallow copy, so nested objects remain shared.'),
    ('rest parameters', 'Rest collects remaining function arguments into a real array.', 'Rest parameters are not the same as the older array-like arguments object.'),
    ('map, filter, and reduce', 'These array methods transform, select, and combine values without mutating the original array.', 'Use reduce only when it communicates intent more clearly than a loop or simpler method.'),
    ('strict equality', '=== compares value and type without coercion; it is usually safer than ==.', 'Loose equality has special coercion rules that make comparisons harder to predict.'),
    ('truthy and falsy values', 'Values such as false, 0, empty string, null, undefined, and NaN are falsy; most others are truthy.', 'Do not use a truthy check when zero or empty string is a valid value.'),
    ('JSON', 'JSON is a text data format; JSON.stringify serializes values and JSON.parse reads valid JSON text.', 'JSON cannot represent functions, undefined values, or circular references directly.'),
    ('modules', 'ES modules use import and export to create explicit file-level dependencies and private scope.', 'Circular imports and inconsistent default-versus-named exports complicate module design.'),
    ('error handling', 'Use try/catch around awaited operations or attach catch handlers to promises, then give users useful recovery states.', 'Catching errors silently hides failures and makes debugging difficult.'),
]

JAVASCRIPT_QUESTIONS = build_library(JAVASCRIPT_TOPICS)
