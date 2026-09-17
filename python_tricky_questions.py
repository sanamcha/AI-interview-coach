"""Python gotcha questions expanded into 100 concise interview prompts."""

from web_questions import build_library


PYTHON_TRICKY_TOPICS = [
    ('mutable default arguments', 'Default argument values are evaluated once when the function is defined, so a mutable default is shared across calls. Use None and create a new list or dict inside the function.', 'Using [] or {} as a default can leak data from one call into another.'),
    ('late binding in closures', 'Closures look up free variables when called, so loop-created functions often see the final loop value. Bind the value with a default argument or functools.partial.', 'Assuming each closure automatically captures a separate loop value causes surprising results.'),
    ('the difference between is and ==', '== compares values using equality; is compares object identity. Use is mainly for singletons such as None.', 'Using is for strings or integers relies on implementation details such as interning.'),
    ('shallow versus deep copy', 'A shallow copy creates a new outer container but shares nested objects; deepcopy recursively copies nested objects.', 'Changing a nested list after a shallow copy also changes what the other container sees.'),
    ('list multiplication with nested lists', 'Multiplying a list of lists repeats references to the same inner list. Use a comprehension to create independent rows.', '[[0] * 3] * 3 makes three aliases of one row, not three independent rows.'),
    ('iterator exhaustion', 'An iterator yields values once; after it is consumed, another loop normally has no values left.', 'Calling list or sum on a generator before reusing it silently exhausts it.'),
    ('generator expressions', 'A generator expression computes values lazily and uses little memory until values are requested.', 'Expecting a generator to support indexing or repeated passes leads to errors or empty results.'),
    ('the global keyword', 'global assigns to a name in the module scope; reading a global name does not require it.', 'Using global broadly makes functions hard to test and reason about.'),
    ('the nonlocal keyword', 'nonlocal assigns to a name in the nearest enclosing function scope, not the module scope.', 'Using nonlocal when no enclosing binding exists raises a SyntaxError.'),
    ('exception variable scope', 'In modern Python, the name bound by except is cleared after the handler to avoid reference cycles.', 'Trying to use an exception variable outside its except block can raise a NameError.'),
    ('bare except clauses', 'A bare except catches BaseException, including KeyboardInterrupt and SystemExit. Catch expected exception types instead.', 'A bare except can make a program impossible to interrupt and hide real defects.'),
    ('dictionary key equality', 'Dictionary keys use both hash values and equality. Equal immutable values such as 1 and True can refer to the same key.', 'Assuming values of different types always create different dictionary keys is incorrect.'),
    ('hashability', 'A value is hashable when its hash does not change during its lifetime, allowing use as a dict key or set member.', 'Lists and dictionaries are unhashable because they are mutable.'),
    ('set ordering', 'Sets are unordered collections; their iteration order is not a semantic guarantee to depend on.', 'Writing logic that expects a set to preserve insertion order is fragile.'),
    ('list sort versus sorted', 'list.sort mutates a list and returns None; sorted returns a new sorted list from any iterable.', 'Assigning result = values.sort() makes result None.'),
    ('tuple commas', 'A comma creates a tuple; parentheses only group expressions. For example, value = 1, is a one-item tuple.', 'Writing (1) creates an integer, while (1,) creates a tuple.'),
    ('string immutability', 'Strings are immutable, so operations create new strings rather than changing the original object.', 'Repeated concatenation in a large loop can be inefficient compared with collecting pieces and joining.'),
    ('integer caching', 'Some Python implementations cache small integers, but identity of numeric literals is an implementation detail.', 'Using is to compare numbers can appear to work in a small test and fail elsewhere.'),
    ('function annotations', 'Annotations are metadata stored on a function; Python does not enforce their types at runtime by default.', 'Assuming type hints automatically validate inputs leads to false confidence.'),
    ('dataclass mutable fields', 'Dataclasses should use default_factory for mutable fields so each instance gets its own container.', 'Using a shared mutable default causes instances to share data.'),
    ('class attributes and instance attributes', 'A class attribute is shared unless an instance assignment shadows it; instance attributes belong to one object.', 'Mutating a shared class-level list unexpectedly affects every instance.'),
    ('method resolution order', 'The MRO determines the order Python searches base classes, using C3 linearization for cooperative multiple inheritance.', 'Calling base methods directly instead of super can skip classes in a multiple-inheritance chain.'),
    ('truthiness', 'Objects are false when they define false __bool__, zero __len__, or are built-in false-like values such as None and empty containers.', 'Using if value when distinguishing 0, empty string, and None matters can lose information.'),
    ('async functions', 'Calling an async function creates a coroutine object; it runs only when awaited or scheduled by an event loop.', 'Forgetting await often produces an unexecuted coroutine warning and wrong behavior.'),
    ('the GIL', 'In CPython, the Global Interpreter Lock allows one thread to execute Python bytecode at a time, though threads still help with I/O.', 'Assuming threads speed up CPU-bound CPython code ignores the GIL.'),
]

PYTHON_TRICKY_QUESTIONS = build_library(PYTHON_TRICKY_TOPICS)
