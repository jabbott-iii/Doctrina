---
paths:
  - "**/src/*Main/**"
  - "**/src/*Test/**"
  - "**/build.gradle.kts"
  - "**/composeResources/**"
  - "**/*.swift"
  - "**/Package.swift"
  - "**/*.podspec"
  - "iosApp/**"
---

# Kotlin Multiplatform standards

These rules cover Kotlin Multiplatform (KMP) code that runs on Android and iOS: the shared source
sets, the platform source sets that implement them, the framework that iOS imports, and the Swift
and Xcode code that meets it. They describe how a senior mobile developer shares code across
platforms. Kotlin itself follows `kotlin.md` in this folder, Android code follows `android.md`,
Swift code follows `swift.md`, and text follows `writing.md`.

Apply them to code you write or edit. Don't rewrite existing code only to make it conform; fix a
passage when you are already changing it, and mention anything else you notice.

## Project details

A repository fills in this section when it adopts the rule, and the rest of the rule refers to
each value by its bold name. If a value still reads `[FILL IN: …]`, the rule isn't set up here
yet. Work out that value from the repository itself, and tell the user which values are missing
so they can fill them in.

- **Modules:** [FILL IN: the shared modules, the app modules, and which module produces the iOS
  framework, for example `:shared` exported by `:shared` and used by `:androidApp` and `iosApp/`]
- **Targets:** [FILL IN: the targets each shared module builds today and those planned, for
  example Android, `iosArm64`, and `iosSimulatorArm64`, or Android only until the iOS phase]
- **What is shared:** [FILL IN: which layers live in common code and how code moves there, for
  example domain and data in `commonMain`, moved one reviewed step at a time, keeping packages]
- **UI strategy:** [FILL IN: how each platform's UI is built, for example Compose Multiplatform
  for both, or Jetpack Compose and SwiftUI over shared ViewModels]
- **Shared UI:** [FILL IN: where the shared Compose screens live and how each app shows them, for
  example `App()` in `:shared:ui`, called from `MainActivity` and from `MainViewController()` in
  `iosMain`, or "none"]
- **Common libraries:** [FILL IN: the multiplatform libraries common code may use, for example
  kotlinx-coroutines, kotlinx-datetime, kotlinx-serialization, Ktor, and Room or SQLDelight]
- **Platform APIs:** [FILL IN: how common code reaches platform features and where the
  implementations live, for example interfaces injected from each app, or `expect` declarations
  with `actual`s in `PlatformFormat.android.kt` and `PlatformFormat.ios.kt`]
- **Boundary check:** [FILL IN: what stops platform APIs from entering common code, for example
  "the compiler, because every target is built", or `SharedCodeBoundaryTest` while Android is the
  only target]
- **iOS framework:** [FILL IN: the framework's name, whether it is static, which modules it
  exports, and how Xcode gets it, for example an XCFramework through Swift Package Manager, or
  the `embedAndSignAppleFrameworkForXcode` build phase]
- **Swift interop:** [FILL IN: how Swift calls suspend functions, collects flows, and switches on
  sealed types, for example SKIE, KMP-NativeCoroutines, or hand-written wrappers, or "none yet"]
- **iOS project:** [FILL IN: where the Xcode project lives and its minimum iOS version, for
  example `iosApp/` with iOS 16]
- **Toolchain:** [FILL IN: the Kotlin, Compose Multiplatform, Xcode, and macOS versions, and where
  each is pinned]
- **Resources:** [FILL IN: where shared strings and images live, for example `composeResources/`
  read through `Res`, or each platform's own resources]
- **Check commands:** [FILL IN: the commands that must pass before you report done, for example
  `./gradlew :shared:allTests` and, on a Mac, `xcodebuild test` for `iosApp`]
- **Test layout:** [FILL IN: where common, platform, and Swift tests live and what they use, for
  example kotlin.test in `commonTest`, actual tests in `androidUnitTest` and `iosTest`, and
  XCTest in `iosApp/Tests`]
- **Release:** [FILL IN: how the iOS app is built, signed, and shipped, for example CD on a macOS
  runner uploading to TestFlight, and who triggers it]

## Decisions that are the user's

Stop and ask the user before you:

- move code into or out of common code, or add or remove a target;
- add a library to common code, or a platform library behind it;
- add an `expect class`, an `@OptIn`, or a `-X` compiler flag;
- change the API that Swift sees, which can break the iOS app's build;
- change the **iOS framework** setup, the Xcode project, or signing;
- change the **UI strategy**, or share UI that each platform builds natively today;
- or change a **Toolchain** version, including Xcode.

## Making a change

- **Read first.** Read the shared code around a change, its `actual`s or platform implementations on
  every target, and the Swift that calls it. Check the **Modules** and **What is shared** to find
  where new code belongs.
- **Check each step on every target.** Move or change one piece at a time, and build every target
  that it affects after each step. Moving a declaration into common code keeps its package, so
  imports don't change.
- **Fix the cause, not the symptom.** If Swift code is awkward to write against the shared API,
  change the Kotlin API; don't copy logic into Swift to work around it. If a platform API seems
  needed in common code, add a platform interface; don't suppress the error.

## What to share

- Follow **What is shared**. Share what must behave the same on both platforms: domain models and
  rules, validation, data access, networking, and formatting logic. Keep what each platform does
  its own way on that platform, or behind a platform interface: system UI, permissions,
  notifications, background work, and anything users expect to feel native. Keep code on each
  platform, too, when sharing it would cost more than writing it twice.
- Share UI only as the **UI strategy** says. Even with Compose Multiplatform, follow each
  platform's conventions where users notice them, such as Back on Android and the swipe from the
  edge on iOS.
- Share a ViewModel only through a multiplatform library (AndroidX Lifecycle's `ViewModel` is
  multiplatform from 2.8), and keep platform types out of it, as `android.md` requires.
- Write code that is shared once, not twice. If the same logic appears in Kotlin and Swift, move
  it into common code, or explain in a comment why it can't be.

## Source sets and targets

- Declare the **Targets** in the shared module's build script, and let Kotlin's default hierarchy
  template create the intermediate source sets (`appleMain`, `iosMain`, `nativeMain`). Don't wire
  `dependsOn` by hand unless the template can't express the structure.
- Build `iosArm64` for devices and `iosSimulatorArm64` for simulators on Apple silicon. Add
  `iosX64` only if someone still builds on an Intel Mac; each target adds compile time.
- Add the iOS targets as early as you can, even before iOS ships. While Android is the only
  target, the compiler accepts Java and Android APIs in `commonMain`, so only the
  **Boundary check** stops them.
- Keep each `actual` and platform implementation in the matching platform source set, in a file
  named for its platform (`PlatformFormat.android.kt`, `PlatformFormat.ios.kt`).

## Common code

- Use only the Kotlin standard library's common API and the **Common libraries** in
  `commonMain`. None of these exist there: `java.*`, `android.*`, `String.format`, `Charsets`,
  `::class.java`, `System`, `synchronized`, and `java.util.concurrent`.
- Use the multiplatform replacements:
  - text as bytes: `encodeToByteArray()` and `decodeToString()`, which use UTF-8;
  - time: kotlinx-datetime and `kotlin.time`, with an injected clock (`kotlin.md`);
  - shared mutable state: a `Mutex` or kotlinx-atomicfu;
  - files and streams: kotlinx-io or a platform interface.
- Add a library to common code only if it publishes every target in the **Targets**, and only
  after the user agrees (see "Decisions that are the user's"). Check its published targets on
  Maven Central or klibs.io, not only its README.
- Use `api` for a dependency whose types appear in the shared module's public API, and
  `implementation` for the rest, as `kotlin.md` describes.
- Format numbers, dates, and currency for the user's locale on the platform, behind the
  **Platform APIs**. Common Kotlin has no locale-aware formatter.

## Reaching the platform

- Follow the **Platform APIs** pattern. Prefer an interface in common code, implemented on each
  platform and passed in through dependency injection. It keeps common code testable with fakes
  and lets each platform implement it in its own idiom.
- Use `expect` and `actual` only for small things an interface can't do well, such as a factory
  function or a constant. Expect and actual classes, including an `actual typealias` that maps a
  common name to a platform type, are still Beta: the compiler warns about each one unless the
  module sets `-Xexpect-actual-classes`, so ask before you add one.
- Give every `expect` declaration KDoc that says what each platform must do, including what
  happens on errors, because each `actual` is written separately.
- Test every `actual` and platform implementation on its own platform.
- Keep secrets in each platform's secure storage behind an interface: the Keychain on iOS and the
  Android Keystore on Android. Never in `NSUserDefaults` or plain preferences. Use each
  platform's cryptography, or one vetted multiplatform library, and never write your own.

## The API that Swift sees

The shared module compiles to an Objective-C framework, so Swift sees Kotlin through
Objective-C. Design that API on purpose.

- Keep it small. Make declarations `internal` unless iOS calls them, and give iOS a few
  entry points, such as a facade or one factory for each feature.
- Export one framework for the app, from one module, listing the other shared modules it exposes
  with `export(...)`. Each Kotlin framework carries its own copy of the Kotlin runtime, and a
  type from one framework isn't the same type in another.
- Know what Swift loses:
  - Default arguments don't carry over, so Swift passes every argument.
  - Generics survive on classes but not on interfaces or functions.
  - Sealed types become class hierarchies, and Swift's `switch` can't check that every case is
    covered.
  - Suspend functions become completion handlers or `async` functions, and flows need the
    **Swift interop** setup to collect.
- Mark every function that Swift calls and that can throw with `@Throws`, listing the exceptions.
  An exception not listed there crashes the app when it reaches Swift, instead of arriving as an
  error that Swift can catch.
- Read the generated header, or use the API from Swift, after every change to it. A name that
  reads well in Kotlin can read badly in Swift.
- Release what Swift hands to Kotlin. A callback or closure that Kotlin keeps holds the Swift
  objects it captures, so clear it, or cancel the job that holds it, when the screen goes away.

## Coroutines and threads across platforms

- Follow `kotlin.md`, and inject dispatchers. On iOS, `Dispatchers.Main` is the main queue, and
  UIKit and SwiftUI must be called only from it.
- Start coroutines that iOS triggers in a scope that iOS can cancel, such as a ViewModel's scope
  or a scope the facade exposes and cancels when its screen closes.
- Expose state to Swift as a `StateFlow` (through the **Swift interop** setup), and deliver it on
  the main thread.

## Data and resources

- Use multiplatform persistence: Room with its multiplatform support or SQLDelight, and DataStore
  for settings. With Room, use the bundled SQLite driver, so both platforms run the same SQLite
  version.
- Give every schema change a migration tested on each platform, as `android.md` describes.
- Keep shared strings and images in the **Resources** location. Strings follow the translation
  rules in `android.md`, whichever platform shows them.

## Compose Multiplatform

These rules apply when the **UI strategy** draws UI with Compose Multiplatform. They add to
`android.md`'s Compose rules (the route and screen split, state hoisting, effects, and
performance), which apply on both platforms.

### Setup and entry points

- Follow the **Shared UI** setup. Keep shared screens in `commonMain`, under one root composable
  that both apps call: Android from an activity's `setContent { App() }`, and iOS from a function
  in `iosMain` that returns `ComposeUIViewController { App() }`, which SwiftUI wraps in a
  `UIViewControllerRepresentable`.
- Apply the Compose Multiplatform Gradle plugin and the Compose compiler Gradle plugin
  (`org.jetbrains.kotlin.plugin.compose`). Since Kotlin 2.0, the compiler plugin ships with
  Kotlin and takes Kotlin's version, so the **Toolchain** moves them together.
- Use multiplatform builds of the libraries that screens need, such as JetBrains' builds of
  AndroidX Lifecycle (`org.jetbrains.androidx.lifecycle`) and Navigation, which publish iOS
  targets. An Android-only artifact compiles in `androidMain` but not in common code.
- Keep the iOS host thin. The Swift side creates the view controller, passes in platform
  services, and owns only what Compose can't do (see "Native views in shared UI").

### What shared UI code can't use

- Keep Android-only Compose and AndroidX APIs out of `commonMain`: `LocalContext`, Android
  resources (`R` and `androidx.compose.ui.res.stringResource`), `hiltViewModel()`, activity
  result launchers, and `AndroidView`. Reach the platform through the **Platform APIs**, as all
  common code does.
- Build every target to check this. While Android is the only target, the compiler accepts these
  APIs in common code (see "Source sets and targets").

### Resources

- Keep shared resources in `src/commonMain/composeResources/`: images in `drawable/`, fonts in
  `font/`, strings in `values/strings.xml`, and other files in `files/`. Read them through the
  generated `Res` class, never by file path:
  - in composables, `stringResource(Res.string.title)`, `pluralStringResource(…)`, and
    `painterResource(Res.drawable.logo)`;
  - outside composition, the suspend functions `getString` and `getPluralString`;
  - raw files, with `Res.readBytes("files/…")`.
- Use qualified folders for languages, themes, and densities (`values-es`, `drawable-dark`,
  `drawable-xxhdpi`). Strings files use Android's format, `<plurals>` included, and follow
  `android.md`'s translation rules.
- Keep each string in one place. Don't copy one between an app's own resources and
  `composeResources/`.
- Check every shipped language on iOS as well as on Android, by switching the simulator's
  language. The two platforms choose an app's language in different ways.

### Platform behavior and look

- Decide through the **UI strategy** how native the shared UI should feel on iOS. Material 3
  components look like Android's there. Where iOS users expect a native control (date and time
  pickers, the share sheet, system alerts, context menus), show the native one through a
  platform interface or `UIKitViewController`.
- Keep Back working on both platforms. On iOS, the navigation library handles the edge-swipe
  back gesture by default. Leave it on: don't set `enableBackGesture = false` in
  `ComposeUIViewController(configure = { … })`. A custom `enterTransition` or `exitTransition`
  replaces the default iOS swipe animation, so check the gesture after you change one. Handle
  Android's Back as `android.md` describes.
- Apply window insets (`WindowInsets.safeDrawing`, `imePadding()`), so content stays clear of the
  notch, the home indicator, and the keyboard on iOS, as edge to edge does on Android.
- Add `CADisableMinimumFrameDurationOnPhone`, set to `true`, to the iOS app's `Info.plist`.
  JetBrains' iOS integration guides require it and warn that the app crashes at runtime without
  it; the key also lets iPhones with ProMotion displays draw above 60 Hz.
- Give every screen both a light and a dark theme. `isSystemInDarkTheme()` follows each
  platform's appearance setting.

### Native views in shared UI

- Embed a native iOS view with `UIKitView` (for example `UIKitView(factory = { MKMapView() })`)
  and a view controller with `UIKitViewController`. To embed a SwiftUI view, create a
  `UIHostingController` for it in `UIKitViewController`'s factory. Use them where native
  behavior matters: maps, the camera, video, web content, and text input that must behave like
  iOS's own.
- Create the native view once, in `factory`, and push state changes into it in `update`, which
  can run many times.
- Keep native embeds few. Each is a separate layer that scrolling, gestures, and focus must
  cross, so test each one inside the scrolling containers it appears in.

### Accessibility

- Compose semantics reach VoiceOver on iOS as they reach TalkBack on Android, so `android.md`'s
  semantics rules apply to both. Check every changed screen with both screen readers.
- Check text at each platform's largest size setting (Android's font scale and iOS's larger
  accessibility text sizes), and with iOS's Increase Contrast setting on.

### Performance on iOS

- Measure iOS performance only on a release build on a real device. A debug Kotlin/Native
  framework runs far more slowly, so its numbers say nothing about the app.
- Watch app size and startup time. The shared UI ships Compose's renderer inside the framework,
  so measure both before and after you add a dependency.
- Lazy lists, stable keys, and deferred state reads (see `android.md`) matter at least as much on
  iOS as on Android.

### Previews and tests

- Previews of common code need an Android target, because they run on Android libraries. Use the
  `androidx.compose.ui.tooling.preview.Preview` annotation, with the
  `org.jetbrains.compose.ui:ui-tooling-preview` dependency. The older
  `org.jetbrains.compose.ui.tooling.preview.Preview` is deprecated.
- Test shared screens in `commonTest` with `runComposeUiTest { … }` from
  `org.jetbrains.compose.ui:ui-test`, so one test runs on every target. The API is experimental
  and needs `@OptIn(ExperimentalTestApi::class)`; agree that opt-in with the user once, for the
  test source sets, as `kotlin.md` requires for any opt-in.
- Find nodes by text, content description, and role first, as `android.md` describes. Run the UI
  tests on an iOS simulator when a Mac is available, and say when one wasn't.

## Build and toolchain

- Keep the **Toolchain**. Each Kotlin release supports particular Xcode versions, so check
  Kotlin's compatibility table before you change either, and change one at a time as its own
  task.
- Building iOS frameworks, running iOS tests, and running the app on a simulator need a Mac with
  Xcode. On another OS, build and test the targets you can, and say which iOS checks you
  couldn't run.
- Kotlin/Native compiles slowly. Build only the target you are testing while you work (for
  example `iosSimulatorArm64`), and all of them before you report done.
- Follow the **iOS framework** setup to integrate with Xcode, and don't change it as part of
  another task. Prefer Swift Package Manager for a new setup.
- Keep the minimum iOS version in the **iOS project** unless the user asks to change it. Raising
  it drops users whose devices can't update.
- Follow the **Release** process. Signing happens only there: never commit a certificate, a
  provisioning profile, or an App Store Connect key.
- Declare in the app's privacy manifest (`PrivacyInfo.xcprivacy`) every required-reason API that
  the app and its frameworks use, the shared framework included. Apple requires it for apps that
  use those APIs.

## Tests

- Follow the **Test layout**. Put tests of shared logic in `commonTest` with `kotlin.test` and
  kotlinx-coroutines-test, so they run on every target. A test that passes on Android can fail on
  iOS, for example where floating-point formatting, string sorting, or time zones differ.
- Use hand-written fakes in common tests. Mocking libraries that work only on the JVM, such as
  MockK, don't run on iOS.
- Test each `actual` and platform implementation in its platform's test source set.
- Cover the API that Swift sees with Swift tests (XCTest) that call each entry point. They catch
  a missing `@Throws`, a crash at the boundary, and an API that compiles but reads badly.
- Run the iOS tests on a simulator from the **Check commands** when a Mac is available;
  otherwise say that they weren't run.

## Before finishing

1. Run every **Check commands** command you can on this machine, and read its output. Fix every
   warning, not only the errors.
2. Build every target in the **Targets** that your change affects. If you can't build the iOS
   targets here, say so, and name the commands to run on a Mac.
3. If you changed common code while Android is the only target, run the **Boundary check**.
4. If you changed the API that Swift sees, read the generated header or the Swift that uses it,
   and run the Swift tests where you can.
5. If you changed the UI, check it on both platforms: on Android as `android.md` describes, and
   on an iOS simulator with VoiceOver, the largest text size, dark appearance, the keyboard open,
   and the edge-swipe back gesture on every screen you pushed.
6. Review your diff as a reviewer would. Look for platform imports in common code, an `actual`
   missing on a target, a throwing function that Swift calls without `@Throws`, Kotlin types leaking
   into the exported API by accident, and a library that doesn't publish every target. Then report
   which targets you built and tested, what you couldn't run, and what remains.
