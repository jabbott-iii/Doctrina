---
paths:
  - "**/*.java"
  - "**/pom.xml"
  - "**/*.gradle"
  - "**/*.gradle.kts"
  - "gradle/libs.versions.toml"
  - "gradle.properties"
  - "gradle/wrapper/gradle-wrapper.properties"
  - "gradle/verification-metadata.xml"
  - ".mvn/**"
  - "build-logic/**"
  - ".java-version"
  - ".sdkmanrc"
---

# Java standards

These rules cover the Java in this repository: modules, packages, tests, and the Gradle or Maven
builds around them. They describe how a senior engineer writes Java. Javadoc, error messages, and
other text follow `writing.md` in this folder. Kotlin code in the same build follows `kotlin.md`,
and Android apps also follow `android.md`.

Apply them to code you write or edit. Don't rewrite existing code only to make it conform; fix a
passage when you are already changing it, and mention anything else you notice.

## Project details

A repository fills in this section when it adopts the rule, and the rest of the rule refers to
each value by its bold name. If a value still reads `[FILL IN: …]`, the rule isn't set up here
yet. Work out that value from the repository itself, and tell the user which values are missing
so they can fill them in.

- **Modules:** [FILL IN: the build's modules (Gradle subprojects or Maven modules) and what each is
  for, with the Java Platform Module System (JPMS) name where a module has a `module-info.java`, or
  where a map of them lives]
- **Toolchain:** [FILL IN: the Java release the code is compiled for, the JDK that builds it, and
  the build tool and where each is pinned, for example `--release 25` with a Gradle toolchain for
  JDK 25 and Gradle 9.9 through the wrapper, or Maven 3.9 through `mvnw` with
  `maven.compiler.release` set to 25]
- **Check commands:** [FILL IN: the commands that must pass before you report done, for example
  `./gradlew check` or `./mvnw -B verify`]
- **Lint configuration:** [FILL IN: the formatter, the compiler warnings, and the static analysis,
  and where they are set, for example Spotless with google-java-format, `-Xlint:all -Werror`, and
  Error Prone, in a convention plugin in `build-logic/`]
- **Null policy:** [FILL IN: how the code says what may be `null`, and what checks it, for example
  JSpecify's `@NullMarked` on every package and `@Nullable` where `null` is allowed, checked by
  NullAway; or `Objects.requireNonNull` on every public parameter]
- **Dependency policy:** [FILL IN: "none" if no third-party libraries are allowed, or how a library
  or plugin gets approved and where approved ones are listed, for example
  `docs/dependency-policy.md`]
- **Errors:** [FILL IN: the exception design, for example checked exceptions for failures a caller
  must handle at module boundaries, unchecked exceptions that extend one `AppException` for the
  rest, mapped to HTTP status codes in the web layer]
- **Concurrency:** [FILL IN: how work runs at the same time, for example a virtual thread for each
  request, a fixed pool for CPU-bound work, and no shared mutable state outside `ConcurrentHashMap`,
  or "none"]
- **Time:** [FILL IN: how code gets the current time, for example an injected `java.time.Clock`]
- **Logging:** [FILL IN: the logging facade and where its back end is chosen, for example the SLF4J
  API in every module and Logback only in the application, or `System.Logger`]
- **Languages:** [FILL IN: the languages users see the program's text in, which are right to left,
  where that text lives, for example `messages_<tag>.properties` bundles in `src/main/resources`,
  and who reviews translations, or "English only"]
- **Untrusted input:** [FILL IN: the modules that read data from outside the program (requests,
  files, messages, users), and where their limits are defined, or "none"]
- **Native code:** [FILL IN: code that leaves Java, for example calls through the Foreign Function
  and Memory (FFM) API or the Java Native Interface (JNI), and what approval new native code needs,
  or "none"]
- **Public API:** [FILL IN: the modules whose API other code depends on, and how binary
  compatibility is checked, for example japicmp against the last release, or "none"]
- **Published modules:** [FILL IN: the modules published to Maven Central or another repository,
  each of which needs its own README, a sources JAR, and a Javadoc JAR, or "none"]
- **Design docs:** [FILL IN: where each module's design is written up, for example
  `docs/modules/<module>.md`, or "none"]
- **Test layout:** [FILL IN: the test frameworks, folders, and naming, for example JUnit Jupiter
  tests in `src/test/java` named `*Test`, and integration tests named `*IT` that need Docker]

## Decisions that are the user's

Stop and ask the user before you:

- add a dependency, including a build plugin, an annotation processor, or a Java agent;
- change a public API, a serialized format, a database schema, or the packages a module exports;
- change the **Toolchain**: the Java release, the JDK, or the build tool's version;
- use a preview feature or an incubator module;
- add native code, or a `--enable-native-access`, `--add-opens`, or `--add-exports` option;
- load code the program didn't ship, with a plugin loader, a script engine, or Java deserialization
  of outside data;
- or weaken the **Lint configuration**, the **Null policy**, a test, or a check.

## Making a change

- **Read first.** Read the code around a change and the tests that cover it. Check the **Modules**
  to find which module a new piece of code belongs in.
- **Check each step.** Compile the module you changed and run its tests after each step, for example
  with `./gradlew :parser:test` or `./mvnw -pl parser test`; that is much faster than a full build.
- **Fix the cause, not the symptom.** For a bug, first write a test that fails, then fix the bug and
  show the test passing. Don't add an `if (x == null) return` that quietly skips a value that should
  never be `null`, and never catch `NullPointerException`; find out why it is `null`.
- **Don't silence the compiler.** Never add `@SuppressWarnings`, a raw type, an unchecked cast, an
  empty `catch`, a `@Nullable` that only quiets the null checker, or an `--add-opens` option only to
  make an error or a warning go away. Work out what it is saying, then fix the types or the design.

## Know your Java release

- Write for the Java release in the **Toolchain**, with the features that are final in it. For
  example, Java 17 has records and sealed classes; 21 adds pattern matching in `switch`, record
  patterns, virtual threads, and sequenced collections such as `List.reversed()`; 22 adds `_` for
  unused variables and the FFM API; 24 adds stream gatherers; and 25, the current long-term support
  (LTS) release, adds flexible constructor bodies, `import module`, and scoped values.
- Compile with `--release`, not `-source` and `-target`. `--release 17` rejects a call to an API
  that Java 17 lacks, such as `List.reversed()`; `-source 17 -target 17` compiles the call, which
  then fails when it runs on Java 17.
- Use a preview feature only after the user agrees (see "Decisions that are the user's"). Class
  files compiled with `--enable-preview` run only on the exact JDK release that compiled them. In
  JDK 25, structured concurrency, primitive types in patterns, and `StableValue` are still previews.
- For a short tool kept in one file, Java 25 runs the source directly (`java Tool.java`), and
  accepts a `void main()` with no class around it.

## Design with types

- Use a record for a value that is only its data. Validate the components in a compact constructor,
  and copy mutable ones there (`List.copyOf(items)`), so the record can't change after it is made.
- Don't put an array in a record: a record compares arrays by reference, so two records holding
  equal arrays aren't `equals`. Use a `List`.
- Model a closed set of cases as a sealed interface with a record for each case, and handle them in
  a `switch` with no `default`. Adding a case then makes the compiler report every `switch` that
  misses it ("does not cover all possible input values").
- Use an `enum` for a fixed set of constants, and `EnumMap` and `EnumSet` for collections keyed by
  one.
- Make fields `private final`, and classes `final` unless they are designed to be extended. Return
  `List.copyOf(…)` or an unmodifiable view, never a mutable internal collection.
- Follow the **Null policy**. Return an empty collection, never `null`, for "nothing". Use
  `Optional` only as a return type for a value that may be absent, never as a field, a parameter, or
  a collection element, and read it with `orElseThrow()` or `orElse(…)`, never a bare `get()`.
- Never use raw types (`List` without its type argument). In parameters, accept the widest type that
  works (`Collection<? extends Shape>` to read from, `Consumer<? super Shape>` to write to), and
  declare variables by their interface (`List`, `Map`).
- Replace `boolean` parameters with an enum, and long parameter lists with a builder or a parameter
  record: `open(path, Mode.READ_ONLY)` says what `open(path, true)` hides.
- Organize packages by what they do (`parser`, `cache`), not by kind (`util`, `helpers`). Keep
  methods short enough that none needs comments to separate its parts.

## Values and common traps

- Compare objects with `equals`, never `==`. `==` on boxed numbers compares identity, and only the
  values -128 to 127 are cached: two `Integer`s of 127 are `==`, but two of 128 aren't. `==` on two
  strings is true only when they are the same object, not whenever their text matches.
- Override `equals` and `hashCode` together, or not at all; records do both for you.
- `BigDecimal.equals` compares the scale too, so `1.0` doesn't equal `1.00`. Compare amounts with
  `compareTo`. Build a `BigDecimal` from a string (`new BigDecimal("0.10")`), because
  `new BigDecimal(0.1)` keeps the double's error:
  0.1000000000000000055511151231257827021181583404541015625.
- Integer arithmetic wraps silently: `Integer.MAX_VALUE + 1` is -2147483648,
  `Math.abs(Integer.MIN_VALUE)` is still negative, and `(int) 3_000_000_000L` is -1294967296. Where
  input decides the values, use `Math.addExact`, `Math.multiplyExact`, and `Math.toIntExact`, which
  throw `ArithmeticException` on overflow.
- `List.of`, `Set.of`, and `Map.of` reject `null` and can't be changed. `Arrays.asList` can't grow.
  `Set.of` and `Map.of` iterate in an order that changes from one run to the next, and a `HashMap`'s
  order can change as it grows. Use `LinkedHashMap` or `TreeMap`, or sort, before the order reaches
  output, files, or test expectations.
- `toUpperCase()`, `toLowerCase()`, and `String.format` use the machine's default locale: in
  Turkish, `"title".toUpperCase()` is `"TİTLE"`, and in German, `String.format("%.2f", 1234.5)` is
  `"1234,50"`. Pass `Locale.ROOT` for text that programs read, such as identifiers, keys, and file
  formats.

## Errors and exceptions

- Follow the **Errors** design.
- Throw a checked exception for a failure the caller can handle and must think about, such as a
  missing file, and an unchecked one for a bug, such as a broken precondition. Check arguments at
  public methods with `Objects.requireNonNull` and `IllegalArgumentException`.
- Keep the cause: `throw new ParseException("bad header in " + path, e)`. Add context where an
  exception crosses a layer, such as the path, the operation, or the position in the input.
- Catch the narrowest exception you can handle. Catch `Exception` only at a boundary that reports
  the failure, such as a request handler or a worker's loop, and never catch `Throwable` or `Error`
  except to log them and exit.
- Never swallow an exception. An empty `catch` hides the failure, and `e.printStackTrace()` sends it
  to standard error, outside the logs.
- When you catch `InterruptedException`, either let it propagate, declared in `throws`, or restore
  the flag with `Thread.currentThread().interrupt()`, so the code that asked for the interrupt sees
  it.
- Close every resource with try-with-resources, which also closes it when an exception is thrown.
  Never rely on `finalize`, which is deprecated for removal.
- Say in each message what failed, with the identifying context (the path, the ID), and never a
  secret.

## Logging and output

- Follow the **Logging** setup. Library code never prints to `System.out` or `System.err`: it throws
  exceptions, and logs through the facade.
- A library depends only on the logging facade's API, never on a logging back end, so the
  application chooses where logs go.
- Pass values as arguments, not by concatenation: `log.info("loaded {} rows from {}", count, path)`.
  The message is then built only when the level is on, and tools that group log messages see one
  message.
- Log an exception you handle by passing it as the last argument, which adds its stack trace.
- Never log secrets, tokens, or personal data.

## Time, numbers, and money

- Get the current time from the **Time** source, never from `Instant.now()` or
  `System.currentTimeMillis()` inside the logic, so tests can fix it.
- Use `java.time`: `Instant` for a moment, `ZonedDateTime` or `OffsetDateTime` for a moment in a
  place, `LocalDate` for a date with no time, and `Duration` for an amount of time. Never use
  `Date`, `Calendar`, or `SimpleDateFormat`, which can be changed after they are made and aren't
  safe to share between threads.
- Store and compare instants in UTC, and convert to the user's zone (`ZoneId`) only to show them.
  `LocalDateTime` has no zone, so never use it for a moment.
- Measure elapsed time with `System.nanoTime()`, not the clock, which jumps when the system time is
  set.
- Keep money in `BigDecimal`, or in a `long` count of the smallest unit, never in `double`. Round
  with `setScale(2, RoundingMode.HALF_EVEN)` or the rounding mode the domain requires.

## Files and processes

- Use `java.nio.file` (`Path` and `Files`), not `java.io.File`.
- Since JDK 18, Java reads and writes text as UTF-8 by default, whatever the machine's locale. Still
  pass a `Charset` when a format requires another encoding.
- Make temporary files with `Files.createTempFile` or `@TempDir` in tests, and delete them when you
  finish.
- To replace a file that must never be left half written, write a temporary file in the same folder,
  then move it into place with `Files.move` and `StandardCopyOption.ATOMIC_MOVE`.
- Run other programs with `ProcessBuilder` and a list of arguments, never `Runtime.exec(String)`,
  which splits the string on spaces and is deprecated. Read the program's output while it runs, or
  redirect it, so a full pipe can't stall it, and wait with a timeout.

## Concurrency

- Follow the **Concurrency** model. Don't add threads, pools, or asynchronous frameworks it doesn't
  include.
- Prefer immutable objects, and pass data between threads instead of sharing it. Guard shared
  mutable state with one lock, held for as short a time as possible, and document the order when
  code takes more than one.
- Use the `java.util.concurrent` classes: `ConcurrentHashMap` (and its atomic `compute` and `merge`
  methods), the atomic classes, and executors. Never start a `Thread` by hand in application code.
- Close an `ExecutorService` with try-with-resources (it is `AutoCloseable` since JDK 19), which
  waits for its tasks, so none is left running.
- For work that mostly waits, such as I/O, use virtual threads (Java 21):
  `Executors.newVirtualThreadPerTaskExecutor()`. Don't pool them, because they are cheap to make;
  limit how many run at once with a `Semaphore` instead.
- Before JDK 24, a virtual thread that blocks inside a `synchronized` block keeps its carrier thread
  (the platform thread it runs on), so no other virtual thread can use that carrier. On those
  releases, guard blocking calls in virtual threads with a `ReentrantLock` instead.
- Don't keep large or many values in `ThreadLocal` with virtual threads, which each get their own
  copy. Pass context explicitly, or use `ScopedValue` (Java 25).
- `CompletableFuture.join()` wraps a failure in `CompletionException`; unwrap its cause before you
  handle it. Give every asynchronous chain an `exceptionally` or `handle` step, or a caller that
  joins it.
- Put a timeout on every wait: `Future.get(timeout, unit)`, `awaitTermination`, and every network
  call.

## Text for users and languages

This section covers the text a program shows people: its output, its help, and its errors as the
user sees them. With "English only" as the **Languages** value, the first two points still apply, so
the program can be translated later.

- Keep user-facing text in the **Languages** bundles, and load it with `ResourceBundle` by key.
  Since Java 9, `.properties` bundles are read as UTF-8. Logs and the messages of exceptions a
  library throws are for developers: keep them in English and out of the bundles.
- Never build a sentence from pieces, and never choose a word form with `n == 1`. The JDK's
  `MessageFormat` and `ChoiceFormat` can't express the plural rules of every language, so use
  ICU4J's `MessageFormat` with `plural` messages, if the **Dependency policy** allows it.
- Format numbers, dates, and currency for the user's `Locale` with `NumberFormat`,
  `DateTimeFormatter.ofLocalizedDate(…).withLocale(…)`, and `NumberFormat.getCurrencyInstance(…)`.
  Pass the locale explicitly; never rely on the default.
- `String.length()` counts UTF-16 code units, not characters: the family emoji 👨‍👩‍👧 has a length of
  8 and 5 code points, but is one character on screen. Count and cut text with
  `BreakIterator.getCharacterInstance()`.
- Sort text people read with a `Collator` for their locale, and compare text after
  `Normalizer.normalize(text, Normalizer.Form.NFC)`.
- When you insert a name or a number into a sentence in a right-to-left language, wrap it in the
  invisible isolation marks FSI and PDI (U+2068 and U+2069), so it doesn't reorder the text around
  it.
- Treat translations you write as drafts, and list their keys in your report for a native speaker to
  review.

## Untrusted input

Treat every byte from outside the program as possibly malformed or hostile, especially in the
**Untrusted input** modules.

- Never use Java serialization (`ObjectInputStream`) on outside data: reading an object can run
  code. Read JSON or another data format into records, and validate them. Where existing code must
  deserialize, set an `ObjectInputFilter` that allows only the classes it expects.
- Turn off document type declarations in every XML parser before it reads outside data. JDK 25's
  default `DocumentBuilderFactory` reads a local file named in an external entity. Set
  `http://apache.org/xml/features/disallow-doctype-decl` to `true` on `DocumentBuilderFactory` and
  `SAXParserFactory`, and `XMLInputFactory.SUPPORT_DTD` to `false` for StAX.
- Never build a query or a command from strings. Use `PreparedStatement` with `?` parameters for
  SQL, and `ProcessBuilder` with a list of arguments for programs.
- Never load a class, a method, or a resource by a name from outside (`Class.forName(input)`), which
  lets the input choose what code runs.
- Treat paths from input as hostile. Resolve them against the target folder, `normalize()` the
  result, and reject it unless it still `startsWith` that folder. A zip entry named `../../x`
  otherwise writes outside it. Check each entry's size and the number of entries, too.
- Check every claimed size against a limit before you allocate, and read large input in chunks.
  Bound recursion with an explicit depth limit.
- Don't run a regular expression with nested repetition, such as `(a+)+`, over outside text: Java's
  regular expressions backtrack, so some inputs take exponential time. Limit the text's length, or
  use possessive quantifiers (`a*+`).
- Use `SecureRandom` for tokens and keys, never `Random` or `Math.random()`. Compare secrets with
  `MessageDigest.isEqual`, whose timing doesn't reveal where two values differ. Keep secrets in a
  `char[]` or `byte[]` and clear it when you finish, because a `String` can't be cleared.
- Hash passwords with a slow, salted function, such as `PBKDF2WithHmacSHA256` from
  `SecretKeyFactory`, or a library the **Dependency policy** allows.
- Keep certificate checks on. Never install a `TrustManager` that trusts every certificate or a
  `HostnameVerifier` that accepts every host.

## Native code

- Follow the **Native code** value. Prefer Java or the FFM API (Java 22) to JNI: the FFM API needs
  no C glue code, and it checks bounds on the memory it hands out.
- The JVM warns when code calls a restricted method of the FFM API, or loads a JNI library, unless
  `--enable-native-access` names its module (or `ALL-UNNAMED`). Add that option only where the
  **Native code** allows native access.
- Don't use `sun.misc.Unsafe`. Its memory-access methods are deprecated for removal; the FFM API and
  `VarHandle` replace them.

## Public APIs

- Keep every API small. In a module with a `module-info.java`, export only the packages that callers
  use, and use `requires transitive` for a dependency whose types appear in the API. A library
  without one sets `Automatic-Module-Name` in its JAR's manifest, so callers can still name it as a
  module.
- Make classes, methods, and fields package-private unless other packages need them. Make public
  classes `final`, or document how to extend them.
- Evolve interfaces with `default` methods, so implementations elsewhere keep compiling.
- Deprecate before you remove: mark the old member `@Deprecated(since = "2.3", forRemoval = true)`,
  and say what replaces it in a `@deprecated` Javadoc tag.
- In the **Public API** modules, each of these breaks callers, either when they compile against the
  new version or when code compiled against the old one runs:
  - removing or renaming a public or protected member, or changing its parameter types or return
    type;
  - adding an abstract method to an interface or an abstract class that callers implement;
  - adding a case to a public sealed type, or a constant to a public enum, which breaks callers'
    exhaustive `switch`;
  - changing a record's components, which changes its constructor and accessors;
  - making a class `final`, or adding a checked exception to a method's `throws` clause.

  Ask before you make one of these changes, and mark it as `commits.md` requires.

## Documentation

Three kinds of docs describe a module, and each has its own reader:

- Javadoc comments, which build each class's page in the API reference, and which editors show.
- The package docs (`package-info.java`) and the module docs (the comment on `module-info.java`),
  which are the reference's front pages.
- A published module's `README.md`, which is its page in the repository and often the first thing a
  new user reads.

Keep all three true. A change to behavior, a signature, an exception, or a limit updates every one
of them that describes it, in the same change.

### Javadoc

- Give every public class and member in the **Public API** modules a Javadoc comment, in `/** … */`
  or, from JDK 23, Markdown in `///` lines, as the project already does. Its first sentence is the
  summary that the reference shows in lists, so make it stand alone.
- Add each tag that applies: `@param` for each parameter, `@return`, `@throws` for each exception
  and when, and `@see`.
- Show examples with `{@snippet file="ParserExample.java" region="parse"}`, which copies a marked
  region from a source file that the build compiles. An example kept that way can't stop compiling
  unnoticed.
- State only what the code does. A claim about cost, ordering, thread safety, or a limit must match
  the code, so check it there or in a test before you write it. Describe planned behavior as
  planned, never in the present tense.
- Explain a term once, on the class that defines it or in the package docs, and link to it from
  everywhere else with `{@link Parser#parse}`. Build the docs with `-Xdoclint:all -Werror`, so a
  missing comment or a broken link fails the build.
- Write code comments that explain why, not what, and keep them true when the code changes. Delete
  commented-out code instead of leaving it.

### Package and module docs

Give each exported package a `package-info.java` with a comment that says what the package holds and
why it is a package of its own. On `module-info.java`, or the main package of a module without one,
say:

1. What the module is, in one or two sentences.
2. Where it fits: what it depends on, what uses it, and how a user reaches it. Link to its write-up
   in the **Design docs**, if there is one.
3. The main classes, grouped by purpose, each named with a link.
4. What a caller must know to use it well: its threading rules, exceptions, and limits.

### Module READMEs

Give each of the **Published modules** a `README.md` of its own, in this shape:

1. `# <artifact-name>`, then one short paragraph on what the module is and does.
2. How it fits: the project it belongs to, and how users reach it, with a link to the project.
3. `## Status`: the version and how stable the API is. Then, kept apart, what is built today, what
   is left out by design, and what is planned.
4. `## Usage`: the Maven and Gradle dependency lines, then examples, then what a user must know to
   avoid errors.
5. `## Documentation`: links to the API reference, the module's write-up in the **Design docs**, and
   the project.
6. `## License`: the license, with links to the license files.

- Keep every README example in a test or a snippet file that the build compiles, and copy it from
  there, so you know it works.
- Use absolute URLs for links that leave the module's folder; sites that republish the README
  resolve relative links differently, or not at all.
- Reread the README whenever the module's behavior or API changes.

### Publication metadata

For each of the **Published modules**, fill in the POM fields that Maven Central requires: `name`,
`description`, `url`, `licenses`, `developers`, and `scm`. Publish a sources JAR and a Javadoc JAR
beside the main one, and sign every file, as Central requires. Inherit the shared fields from one
convention plugin or parent POM rather than repeating them in each module.

## Tests

- Follow the **Test layout**. Where `testing.md` is adopted, it sets how strict and complete the
  tests must be.
- Give every behavior change a test. Start every bug fix with a test that fails before the fix.
- Name each test for the behavior it checks: `rejectsArchiveWhoseEntriesEscapeTheTarget`, not
  `test3`.
- Use JUnit Jupiter's tools: `@ParameterizedTest` for cases that differ only in their data,
  `@TempDir` for files, and `assertThrows`, which returns the exception so the test can check its
  type and code.
- Keep tests deterministic: inject a fixed `Clock`, seed every `Random`, and never wait with
  `Thread.sleep`; wait for the real condition, with a timeout.
- Prefer hand-written fakes to mocks. Mock only at boundaries you don't own, and only with a library
  the **Dependency policy** allows.
- Test the edges: empty, one, the maximum, one past the maximum, and malformed. For a parser,
  include truncated and oversized input.
- Assert on exception types, error codes, and returned values, not on message text, so rewording a
  message doesn't break a test.
- Keep tests independent of each other and of their order, so they can run in parallel.

## Style, lints, and the toolchain

- Format with the formatter in the **Lint configuration**, by running its task rather than
  formatting by hand.
- Follow the Java naming conventions: `PascalCase` for types, `camelCase` for methods, fields, and
  variables, `UPPER_SNAKE_CASE` for `static final` constants, and lowercase package names that start
  with a domain the project owns, reversed (`org.example.parser`).
- Compile with `-Xlint:all -Werror` where the **Lint configuration** sets it, and add no new
  warnings. Treat static-analysis findings as design feedback, and refactor instead of suppressing
  them.
- When a warning is wrong in one place, suppress it on the smallest declaration, with its exact name
  and a reason: `@SuppressWarnings("unchecked") // The array holds only E values, written by add().`
  Never suppress a whole class or a warning family such as `"all"`.
- Mark every overriding method `@Override`, so a signature that stops matching fails to compile.
- Don't leave `System.out` calls, `printStackTrace`, or debugging logs behind.
- Keep the **Toolchain**. Don't change the Java release, the JDK, or the build tool's version as a
  side effect of another task; each is a change of its own. Set the JDK with a toolchain or the
  wrapper's settings rather than relying on the one installed.

## Builds and dependencies

- Follow the **Dependency policy**. Never add a library or a plugin without asking. When you propose
  one, say what it does that the JDK or existing code can't, and give its license, how well it is
  maintained, and how many libraries it brings in (from `./gradlew dependencies` or
  `./mvnw dependency:tree`).
- Build with the wrapper (`./gradlew` or `./mvnw`), and keep the wrapper's `distributionSha256Sum`,
  which makes it check what it downloads. Don't change the wrapper as part of another task.
- Declare every version once: in `gradle/libs.versions.toml` for Gradle, or in
  `<dependencyManagement>` for Maven, importing a bill of materials (BOM) where a library family
  publishes one. Use no version ranges, dynamic versions (`+`, `latest.release`), or `-SNAPSHOT`
  dependencies in a release, and add no repositories.
- With Gradle's `java-library` plugin, use `implementation` rather than `api` unless a dependency's
  types appear in the module's public API. With Maven, give each dependency the narrowest scope:
  `test` for test libraries, and `provided` for what the runtime supplies.
- Keep Gradle build logic in convention plugins (for example in `build-logic/`), not in
  `allprojects` or `subprojects` blocks, and compatible with the configuration cache. In Maven, keep
  shared configuration in one parent POM.
- Where the project keeps `gradle/verification-metadata.xml`, update it in the same change as a new
  or updated dependency, so Gradle checks the checksums of what it downloads.

## Before finishing

1. Run every **Check commands** command and read its output. Fix every warning, not only the errors.
2. If you changed public classes, Javadoc, package docs, or a README:
   1. Build the Javadoc with `-Xdoclint:all -Werror`, so a missing comment or a broken link fails.
   2. Build the tests and snippet files that the docs and the README copy their examples from.
   3. Reread the changed prose against the code.
3. If you changed a **Public API** module, run its binary compatibility check, and explain every
   change it reports.
4. If you changed what a published module ships, publish it locally (`./gradlew publishToMavenLocal`
   or `./mvnw install`), list each JAR with `jar --list --file <file>.jar`, and check the POM, the
   sources JAR, and the Javadoc JAR.
5. If the code runs on more than one JDK release, run the tests on each one the **Toolchain** names,
   and say which you couldn't.
6. Review your diff as a reviewer would. Look for raw types, unchecked casts, `@SuppressWarnings`
   without a reason, a `catch` that swallows an exception, `printStackTrace`, `System.out`,
   `Optional.get()`, `==` on boxed values or strings, `new BigDecimal(double)`, `Date` or
   `SimpleDateFormat`, `ObjectInputStream`, `toUpperCase()` or `String.format` without a locale, and
   missing docs or tests. Then report what you ran, what you didn't, and what remains.
