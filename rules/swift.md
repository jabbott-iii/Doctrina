---
paths:
  - "**/*.swift"
  - "**/Package.swift"
  - "**/Package.resolved"
  - "**/*.xcstrings"
  - "**/*.xcprivacy"
  - "**/*.entitlements"
  - "**/Info.plist"
  - "**/*.xcodeproj/**"
  - "**/.swiftlint.yml"
  - "**/.swift-format"
---

# Swift and SwiftUI standards

These rules cover Swift code and SwiftUI interfaces for Apple platforms in this repository: app
targets, extensions, Swift packages, tests, and the project files around them. They describe how a
senior mobile developer writes Swift. Doc comments, user-facing strings, and other text follow
`writing.md` in this folder. Code that uses a Kotlin Multiplatform framework also follows
`kotlin-multiplatform.md`.

Apply them to code you write or edit. Don't rewrite existing code only to make it conform; fix a
passage when you are already changing it, and mention anything else you notice.

## Project details

A repository fills in this section when it adopts the rule, and the rest of the rule refers to
each value by its bold name. If a value still reads `[FILL IN: …]`, the rule isn't set up here
yet. Work out that value from the repository itself, and tell the user which values are missing
so they can fill them in.

- **Targets and modules:** [FILL IN: the app, extension, and test targets and the local Swift
  packages, with what each holds, for example `App`, `Widgets`, and `Packages/Core`]
- **Toolchain:** [FILL IN: the Xcode and Swift versions, the Swift language mode, the strict
  concurrency level, the default actor isolation, and the minimum OS versions, for example
  Xcode 26, Swift 6 mode, complete checking, main-actor default, and iOS 17]
- **Check commands:** [FILL IN: the commands that must pass before you report done, for example
  `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 17'` and
  `swift format lint --recursive .`]
- **Style and lint configuration:** [FILL IN: the formatter and linter and their configuration
  files, for example swift-format with `.swift-format`, or SwiftLint with `.swiftlint.yml`]
- **Dependency policy:** [FILL IN: how a Swift package gets approved and where versions are
  pinned, for example "ask first; versions pinned in the committed `Package.resolved`"]
- **Architecture:** [FILL IN: the UI layer's pattern and how dependencies arrive, for example one
  `@Observable` model per screen, given its services through its initializer]
- **Navigation:** [FILL IN: how screens are reached, for example a `NavigationStack` whose path
  is an array of `Route` values owned by a router]
- **Design system:** [FILL IN: the shared components, colors, and type styles, for example
  `Packages/DesignSystem` with semantic colors in the asset catalog and SF Symbols for icons]
- **Languages:** [FILL IN: the localizations the app ships, which are right to left, where the
  String Catalogs live, and who reviews translations, or "English only"]
- **Persistence:** [FILL IN: how data is stored and migrated, for example SwiftData with a
  `VersionedSchema` per release, or Core Data, or files in the app container]
- **Networking:** [FILL IN: the network layer and where it lives, for example an `APIClient`
  over `URLSession` in `Packages/Networking`, or "none"]
- **Security controls:** [FILL IN: where the threat model and security decisions are written
  down, for example Keychain access classes, App Transport Security exceptions, and hiding
  content in the app switcher, or "none"]
- **Kotlin interop:** [FILL IN: the Kotlin Multiplatform framework the app uses and the Swift
  types that wrap it, or "none"]
- **Test layout:** [FILL IN: where unit, UI, and snapshot tests live and what they use, for
  example Swift Testing in `AppTests`, XCTest UI tests in `AppUITests`, and a test plan]
- **Release:** [FILL IN: how builds are signed and shipped, for example Xcode Cloud uploading to
  TestFlight, and who submits to App Review]

## Decisions that are the user's

Stop and ask the user before you:

- add a Swift package or a binary framework;
- raise a minimum OS version, or change the Swift language mode, the concurrency checking, or the
  Xcode version;
- add a capability, an entitlement, a background mode, a permission's usage description, or an App
  Transport Security exception;
- change a persisted model, which needs a migration;
- change signing, provisioning, or anything App Store Connect shows;
- change the design beyond what was asked;
- or weaken a lint rule, a test, or a check.

## Making a change

- **Read first.** Read the code around a change, the model and views of the screen it touches, and
  the tests that cover it, and reuse the **Design system** components. Check the
  **Targets and modules** to find where new code belongs.
- **Check each step.** Build after each step. After a UI change, run the app in a simulator and use
  the changed screen; a preview isn't the app.
- **Fix the cause, not the symptom.** If a view doesn't update, fix who owns and observes the state;
  don't force a redraw with `.id(UUID())`. If a layout is off, fix the layout; don't add a magic
  offset. If a test is flaky, wait for the real condition; don't add a sleep.
- **Don't silence the compiler.** Never add `!`, `try!`, `as!`, `@unchecked Sendable`,
  `nonisolated(unsafe)`, `@preconcurrency`, `MainActor.assumeIsolated`, a hop to
  `DispatchQueue.main`, or a lint-disable comment only to make an error or a warning go away. Work
  out what the compiler is saying, then fix the types, the isolation, or the design.

## Design with types

- Use value types (`struct`, `enum`) by default. Use a `final class` when the thing has an
  identity that several places share, and an `actor` when it holds mutable state that concurrent
  code shares.
- Model states with an `enum` that carries associated values, instead of several optionals that
  are only valid together.
- Switch over your own enums without `default`, so adding a case makes the compiler list every
  place that must handle it. For an enum from a system framework that may gain cases, add
  `@unknown default`.
- Wrap IDs and validated values in their own types (`struct UserID: Hashable { let raw: String }`),
  so the compiler rejects a `UserID` passed where an `OrderID` belongs. Parse input into them
  once, where it enters the app.
- Use the smallest access level that works: `private`, then `fileprivate`, `internal` (the
  default), `package`, and `public`. Mark classes `final` unless they are designed for
  subclassing, and prefer protocols and composition to inheritance.
- Prefer generics and opaque types (`some Protocol`). Use an existential (`any Protocol`) when
  one collection must hold different types, and write the `any` explicitly.
- Follow the Swift API Design Guidelines:
  - Name for clarity at the point of use, and omit needless words.
  - Name mutating methods as verbs (`sort()`) and their non-mutating versions as nouns or past
    participles (`sorted()`).
  - Make Boolean properties read as assertions (`isEmpty`, `canSubmit`).
  - Use `UpperCamelCase` for types and `lowerCamelCase` for everything else, and keep acronyms
    in one case (`url`, `URLSession`, `userID`).
- Organize a type's conformances in extensions, one per protocol. Organize files by feature, not
  by kind (`Utilities`, `Helpers`).

## Optionals and errors

- Never force unwrap (`!`), force try (`try!`), or force cast (`as!`) in production code. Use
  `guard let` for an early exit, `if let x`, `??`, and `as?`. Don't declare implicitly unwrapped
  optionals.
- Throw errors for failures a caller should handle, and give each error type cases a caller can
  act on. Typed throws (`throws(ParseError)`) suit a closed set of errors inside a module; prefer
  plain `throws` in public APIs, which may need new errors later.
- Use `try?` only where failure doesn't matter, with a comment that says why.
- Map errors to user-facing messages in the UI layer, from localized strings. Never show an
  error's debug description.
- Use `precondition` for programmer errors that must stop the app, and `fatalError` only for
  code that can't be reached, with a message that says why. `assert` runs only in debug builds.

## Memory

- Swift frees objects by reference counting, so two objects that hold each other strongly are
  never freed. Capture `[weak self]` in an escaping closure that `self` stores, directly or
  through something it owns, and declare delegates `weak`.
- Use `unowned` only when the other object certainly outlives this one; using it after the
  object is gone crashes the app.
- A stored `Task` keeps everything it captures alive until it ends. Cancel it when its owner
  goes away, or start the work with SwiftUI's `.task` modifier instead.

## Numbers, money, and time

- Integer overflow stops the app in every build: Swift traps on overflow unless the code is
  compiled with `-Ounchecked`. Where input decides the values, check first, or use
  `addingReportingOverflow`, or the wrapping operators (`&+`, `&*`) when wrapping is what you
  mean.
- Converting a number that doesn't fit also traps: `Int(someDouble)` with `NaN` or infinity, and
  `Int8(someInt)` with a value out of range. Use `Int(exactly:)`, `Int8(clamping:)`, or
  `Int8(truncatingIfNeeded:)` to say what should happen instead.
- Never use `Double` or `Float` for money. Use `Decimal`, or an integer count of the smallest
  unit, and format it with `.formatted(.currency(code:))`.
- Inject the current date (a `() -> Date`, or a small protocol) and, for delays, an
  `any Clock<Duration>`, so tests can control time. Pass a `TimeZone` and `Calendar` explicitly
  to date math, store dates in ISO 8601, and format them with `FormatStyle` at the edge.
- A `String` counts characters as users see them, so `count` walks the whole string. Don't index
  strings by integer offsets.

## Concurrency

- Follow the **Toolchain** settings: Swift 6 language mode with complete checking makes data
  races compile errors. Fix each diagnostic; don't opt out of the check.
- Keep UI types on the main actor. SwiftUI's `View` is main-actor-isolated, and models that views
  observe are `@MainActor`. If the module isolates code to the main actor by default (Swift 6.2),
  mark work that must leave it `nonisolated`, or `@concurrent` for async functions.
- Use structured concurrency: `async let` and task groups for parallel work, and SwiftUI's
  `.task` for work tied to a view, which SwiftUI cancels when the view goes away. Start an
  unstructured `Task { }` only at a boundary, such as a button action, and `Task.detached` almost
  never.
- Cancellation is cooperative. Long work calls `try Task.checkCancellation()` or checks
  `Task.isCancelled` between steps.
- Protect shared mutable state with an actor, or, for a small critical section, with `Mutex` from
  the Synchronization framework (iOS 18 and later; `OSAllocatedUnfairLock` before that). An
  actor can run other calls while one awaits, so check its state again after every `await`
  inside it.
- Make types that cross actors `Sendable`: value types of `Sendable` parts, or final classes with
  only immutable properties. Never add `@unchecked Sendable` without a lock that makes it true, a
  comment that explains it, and the user's agreement.
- Never block a thread waiting for async work, for example with a semaphore; it can deadlock.
  Don't mix `DispatchQueue` code into new async code.
- Use `@preconcurrency import` only for a module that hasn't adopted Swift concurrency yet, with
  a comment that names the module and says when to remove it.

## SwiftUI

### State and data flow

- Follow the **Architecture**. Keep `body` cheap and free of side effects: no I/O, sorting, or
  heavy formatting. SwiftUI calls `body` often, so compute in the model.
- Choose the property wrapper by who owns the data:
  - `@State` for values the view owns, and to own an `@Observable` model the view creates. Mark
    it `private`.
  - `@Binding` for a child that edits a value its parent owns.
  - `@Bindable` to bind to the properties of an `@Observable` model passed in.
  - `@Environment` for dependencies shared across a part of the app.
- Use the Observation framework (`@Observable`) rather than `ObservableObject`, `@Published`, and
  `@StateObject` in new code, when the minimum OS is iOS 17 or later. Views then update only for
  the properties they read.
- Don't initialize `@State` from an initializer parameter and expect it to follow that
  parameter: SwiftUI uses the initial value only the first time the view appears.

### Identity and structure

- Extract parts of a view into separate `View` structs, not computed properties, so SwiftUI can
  compare and skip them separately.
- Give `ForEach` stable identities: `Identifiable` values, or `\.self` only for unique values that
  never change. Never use array indices for data that can change.
- Prefer a modifier with a conditional value (`.opacity(isVisible ? 1 : 0)`) to an `if` that
  swaps views when the view should stay the same view. An `if` gives each branch its own
  identity, which resets its state and animations.
- Avoid `AnyView`, which hides the view's type from SwiftUI's comparison.

### Side effects and navigation

- Start async work with `.task`, and use `.task(id:)` to restart it when a value changes. Don't
  write `.onAppear { Task { … } }`, which isn't canceled when the view goes away.
- React to changes with `.onChange(of:)`, keeping the effect small.
- Follow the **Navigation** setup. Use `NavigationStack` with `navigationDestination(for:)` and
  a path of `Hashable` values, and `NavigationSplitView` for wide layouts. Pass IDs between
  screens, not models, and let deep links build the path.
- Embed UIKit with `UIViewRepresentable` or `UIViewControllerRepresentable`, with a coordinator
  for delegates, and make `updateUIView` safe to call any number of times.

### Performance and previews

- Measure before optimizing, with Instruments' SwiftUI, Time Profiler, and Hangs tools, on a
  release build and a real device where you can. `Self._printChanges()` in a debug build shows
  why a `body` ran again; remove it afterward.
- Use `List` or a lazy stack (`LazyVStack`) for long content.
- Give every screen `#Preview`s with sample data, in light and dark appearance, at a large
  Dynamic Type size, and right to left if the app ships a right-to-left language. Previews never
  touch the network or real data.

## Layout, design, and accessibility

- Use the **Design system** and Apple's Human Interface Guidelines. Use semantic colors and text
  styles (`.font(.body)`) so Dark Mode and Dynamic Type work, SF Symbols for icons, and no
  hard-coded colors, font sizes, or one-off spacing.
- Lay out with stacks, `Grid`, `ViewThatFits`, and custom `Layout`s, never fixed frames around
  text. Respect the safe area (`.safeAreaInset` for bars you add), and support every size the app
  runs at: rotation, iPad multitasking, and Stage Manager.
- Support Dynamic Type at every size, including the accessibility sizes. Scale custom
  measurements with `@ScaledMetric`, and switch a horizontal layout to vertical at accessibility
  sizes.
- VoiceOver:
  - Give every icon-only control an `accessibilityLabel`, and hide decorative images with
    `accessibilityHidden(true)`.
  - Combine a row's parts into one element (`accessibilityElement(children: .combine)`), and
    describe state with `accessibilityValue`.
  - Mark section titles with `.accessibilityAddTraits(.isHeader)`.
  - Announce changes that happen without a screen change with
    `AccessibilityNotification.Announcement`.
- Keep tap targets at least 44 × 44 points, honor Reduce Motion
  (`accessibilityReduceMotion`), and never use color alone to show state.
- Localization:
  - Keep every user-facing string in a String Catalog (`.xcstrings`), in every language the
    **Languages** value lists, with a comment for translators. `Text("key")` looks up the
    string; use `String(localized:)` outside views.
  - Use the catalog's plural variations for counts, and never build a sentence from separately
    translated fragments.
  - Format numbers, dates, and measurements with `FormatStyle` (`.formatted()`), for the user's
    locale.
  - Use `leading` and `trailing`, never `left` and `right`, and check layouts with the
    double-length and right-to-left pseudolanguages in the scheme's options.
  - Treat translations you write as drafts, and list their keys in your report for a native
    speaker to review.

## Data and networking

- Follow the **Persistence** setup. With SwiftData, add a `VersionedSchema` for each released
  version of the model and a `SchemaMigrationPlan` between them; with Core Data, a new model
  version. Never delete the store to get past a migration error, because that deletes the user's
  data, and test every migration.
- Keep small, non-sensitive settings in `UserDefaults` or `@AppStorage`, and everything else in
  the persistence layer.
- Write sensitive files with data protection (`.completeFileProtection`).
- Follow the **Networking** setup. `URLSession` doesn't throw for an HTTP error status such as
  404 or 500, so check the `HTTPURLResponse`'s `statusCode`. Set timeouts, let task cancellation
  cancel requests, and decode with `Codable` using explicit strategies, then validate the result.

## Security and privacy

- Never weaken an item in the **Security controls**. Name every control your change touches in
  your report, and say why it still holds.
- Keep secrets and tokens in the Keychain, with the strictest accessibility that works (for
  example `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`). Never in `UserDefaults`, the source
  code, or `Info.plist`: anything in the app bundle can be extracted.
- Bind biometric sign-in to a Keychain item protected by `SecAccessControl` (for example
  `.biometryCurrentSet`), not to a Boolean result from LocalAuthentication, which a modified app
  can fake.
- Keep App Transport Security on: HTTPS only, with no exceptions unless the user agrees.
- Permissions:
  - Add a usage description (`NS…UsageDescription`) for each permission, in words that tell the
    user why.
  - Ask at the moment the feature needs it, and give the feature a fallback for when the user
    says no.
  - Declare in the privacy manifest (`PrivacyInfo.xcprivacy`) every required-reason API the app
    and its packages use, and whether the app tracks users.
- Log with `Logger`. Interpolated strings are redacted in release logs by default; mark a value
  `privacy: .public` only when it is safe for anyone to read. Never log personal data or secrets.
- Treat deep links and universal links as input from outside the app, and validate them.

## Kotlin Multiplatform interop

When the **Kotlin interop** value names a framework:

- Wrap it behind Swift protocols and types at the app's boundary, so the rest of the Swift code
  doesn't depend on Kotlin types.
- Catch the errors that Kotlin's `@Throws` functions report, collect its flows on the main actor
  through the interop setup, and cancel what you start when the screen goes away.
- When the Kotlin API is awkward from Swift, ask for the Kotlin side to change, as
  `kotlin-multiplatform.md` describes, instead of working around it in Swift.

## Documentation

- Give every public declaration of a Swift package a doc comment (`///`) whose first sentence is
  a summary that stands alone. Add `- Parameters:`, `- Returns:`, and `- Throws:` where they
  apply.
- Link to other symbols with double backticks (` ``Parser/parse(_:)`` `), and explain a term once,
  where it is defined. Build the documentation with DocC and fix its warnings.
- State only what the code does, and describe planned behavior as planned. Write code comments
  that explain why, not what, and delete commented-out code.

## Tests

- Follow the **Test layout**. Write new unit tests with Swift Testing (`@Test`, `#expect`, and
  `#require`), using arguments (`@Test(arguments:)`) for cases that share a test. Use XCTest for
  UI tests and performance tests, which Swift Testing doesn't cover.
- Give every behavior change a test, and start every bug fix with a test that fails before the
  fix.
- Test models and other logic, not view structure. Inject fakes through protocols, and control
  the date, the clock, the network (with a `URLProtocol` stub), the locale, and the time zone.
- Never sleep in a test. Await the async work; in UI tests, wait with
  `waitForExistence(timeout:)`.
- Run `performAccessibilityAudit()` in UI tests of changed screens.
- Run the tests with Thread Sanitizer from time to time, and keep the Main Thread Checker on.

## Style, lints, and the toolchain

- Format and lint with the tools in the **Style and lint configuration**, by running them rather
  than formatting by hand.
- Add no new warnings, and keep warnings as errors (`SWIFT_TREAT_WARNINGS_AS_ERRORS`) wherever it
  is on.
- Keep the **Toolchain**. Don't change the Xcode version, the Swift language mode, the
  concurrency settings, or a minimum OS version as a side effect of another task; each is a
  change of its own. Before you use an API, check that the minimum OS has it, or guard it with
  `if #available`.
- Don't hand-edit `project.pbxproj` beyond what a change needs; it conflicts easily. In folders
  that Xcode keeps in sync with the disk (Xcode 16 and later), a new file joins its target
  without editing the project file.
- Don't leave `print` calls, debugging code, or `_printChanges()` behind.

## Dependencies and release

- Follow the **Dependency policy**. Never add a Swift package or a binary framework without
  asking. When you propose one, say what it does that the system frameworks can't, and give its
  license, how well it is maintained, what it pulls in, and whether it ships its privacy
  manifest (and signature, for SDKs on Apple's list).
- Commit `Package.resolved` for apps, so every build uses the same versions.
- Follow the **Release** process. Increase the build number for every upload, and never commit a
  certificate, a provisioning profile, or an App Store Connect key.

## Before finishing

1. Run every **Check commands** command you can on this machine, and read its output. Fix every
   warning, not only the errors. Xcode builds need a Mac; on another OS, build and test only the
   Swift packages the Swift toolchain can, and say what you couldn't run.
2. If you changed the UI, run the app in a simulator and use the changed screen:
   1. in light and dark appearance, at the largest accessibility Dynamic Type size, and in the
      right-to-left pseudolanguage if the app ships a right-to-left language;
   2. with VoiceOver, if you changed interactive elements;
   3. after rotating it, and on an iPad size if the app supports one;
   4. after sending it to the background and back.
3. If you changed a persisted model, run its migration test against data from the previous
   version.
4. If you changed `Info.plist`, entitlements, capabilities, or the privacy manifest, list each
   change in your report.
5. Review your diff as a reviewer would. Look for force unwraps, strong reference cycles, work in
   `body`, hard-coded strings, colors, and sizes, controls without an accessibility label, `print`
   calls, and new warnings. Then report what you checked, what you didn't, and what remains.
