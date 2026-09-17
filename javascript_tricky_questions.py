"""JavaScript gotcha questions expanded into 100 concise interview prompts."""

from web_questions import build_library


JAVASCRIPT_TRICKY_TOPICS = [
    ('the == and === operators', '=== compares values without type coercion, while == coerces values before comparison. Prefer === except for deliberate nullish checks.', 'Loose equality can make values such as false, 0, and empty strings compare unexpectedly.'),
    ('NaN comparisons', 'NaN is not equal to itself, so use Number.isNaN(value) to test it.', 'Using value === NaN always returns false.'),
    ('the typeof null result', 'typeof null returns "object" because of a historical JavaScript bug. Test null directly with value === null.', 'Using typeof value === "object" also matches null.'),
    ('var in loops', 'var is function-scoped, so callbacks created in a loop share one binding. Use let for a new block-scoped binding each iteration.', 'Expecting var callbacks to remember each loop number gives the final value repeatedly.'),
    ('temporal dead zone', 'let and const exist from the start of their block but cannot be accessed before initialization.', 'Treating let exactly like var causes reference errors before declaration.'),
    ('closure capture', 'A closure retains access to variables from its lexical environment, often enabling private state and callbacks.', 'Closures retain bindings, so changing the outer value affects later calls.'),
    ('this binding', 'this depends on how a normal function is called; arrow functions capture lexical this instead.', 'Passing a method as a callback can lose its original receiver.'),
    ('arrow functions and this', 'Arrow functions do not have their own this, arguments, or constructability; they inherit this from the surrounding scope.', 'Using an arrow method when dynamic this is required can produce the wrong receiver.'),
    ('call, apply, and bind', 'call invokes with a chosen this and arguments, apply accepts an array-like argument list, and bind returns a permanently bound function.', 'bind does not call the function immediately; it creates a new function.'),
    ('event loop order', 'Synchronous code runs first, then microtasks such as promise callbacks, then later task queues such as timers.', 'Assuming setTimeout callback runs before a resolved promise gives incorrect ordering.'),
    ('promises', 'A promise represents an eventual result and settles once as fulfilled or rejected.', 'Creating a promise without returning or awaiting it can make errors escape the intended chain.'),
    ('async and await', 'async functions return promises; await pauses that async function until a promise settles.', 'Forgetting await can pass a Promise where a resolved value was expected.'),
    ('try catch with async code', 'try/catch catches a rejected promise only when it is awaited inside the try block.', 'A promise started but not awaited will not be caught by that local try/catch.'),
    ('optional chaining', 'Optional chaining stops property access and returns undefined when the left side is null or undefined.', 'It does not protect an undeclared variable or every later operation automatically.'),
    ('nullish coalescing', 'The ?? operator uses its fallback only for null or undefined, unlike || which also treats 0, false, and empty string as missing.', 'Using || for numeric or boolean defaults can replace valid false-like values.'),
    ('spread syntax', 'Spread expands an iterable into elements or enumerable object properties into a new object.', 'Object spread is shallow, so nested objects remain shared.'),
    ('object reference equality', 'Objects compare by reference, not structural content, so two separate equal-looking objects are not ===.', 'Comparing objects with === does not compare their properties.'),
    ('shallow copying objects', 'Object spread and Object.assign create shallow copies that share nested arrays and objects.', 'Changing a nested property in the copy can affect the original.'),
    ('JSON stringify limitations', 'JSON.stringify omits undefined object values, cannot serialize BigInt, and turns some values such as Date into strings.', 'Using JSON stringify as a universal deep clone loses important data types and cycles fail.'),
    ('map versus forEach', 'map returns a new array of transformed values; forEach is for side effects and returns undefined.', 'Using forEach when a transformed array is needed often leads to undefined results.'),
    ('filter versus find', 'filter returns all matching elements in an array; find returns the first matching element or undefined.', 'Treating filter output like a single object causes property access errors.'),
    ('reduce without an initial value', 'Without an initial value, reduce uses the first item as accumulator and fails on an empty array.', 'Provide an initial value when empty input is possible or the accumulator type differs.'),
    ('destructuring defaults', 'A destructuring default applies only when the extracted value is undefined, not when it is null.', 'Expecting a default to replace null leads to later null errors.'),
    ('prototypes', 'Objects inherit behavior through a prototype chain, which JavaScript searches when a property is not own.', 'Mutating shared prototype state can affect every object that inherits it.'),
    ('strict mode', 'Strict mode prevents several legacy silent behaviors and changes how plain-function this is handled.', 'Relying on accidental globals works differently or fails under strict mode and modules.'),
]

JAVASCRIPT_TRICKY_QUESTIONS = build_library(JAVASCRIPT_TRICKY_TOPICS)
