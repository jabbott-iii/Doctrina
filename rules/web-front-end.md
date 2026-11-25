---
paths:
  - "**/*.html"
  - "**/*.htm"
  - "**/*.css"
  - "**/*.scss"
  - "**/*.js"
  - "**/*.mjs"
  - "**/*.ts"
---

# Web front-end standards

These rules cover the HTML, CSS, and JavaScript of a website or web app in this repository, and the
templates that produce its pages. They describe how a senior front-end developer builds for the web.
Text on the pages follows `writing.md` in this folder.

Apply them to code you write or edit. Don't rewrite existing files only to make them conform; fix
a passage when you are already changing it, and mention anything else you notice.

## Project details

A repository fills in this section when it adopts the rule, and the rest of the rule refers to
each value by its bold name. If a value still reads `[FILL IN: …]`, the rule isn't set up here
yet. Work out that value from the repository itself, and tell the user which values are missing
so they can fill them in.

- **Page head:** [FILL IN: the layout or include that writes each page's doctype, `lang`,
  charset, viewport, and meta tags, for example `_layouts/default.html` and `_includes/seo.html`,
  or "none" if every page writes its own]
- **Templates:** [FILL IN: the template language and its helpers for URLs and escaping, for
  example Liquid with `relative_url`, `absolute_url`, `| escape`, and `| jsonify`, or "none" for
  plain HTML]
- **Languages:** [FILL IN: the languages the site ships, which are right to left, where each
  language's pages or strings live, for example a folder per language (`/es/`, `/ar/`) or JSON
  files for i18next, and who reviews translations, or "English only"]
- **Stylesheets:** [FILL IN: where styles live, for example `assets/css/style.css`]
- **Design tokens:** [FILL IN: where the CSS custom properties are defined, with a few of their
  names, for example `:root` in `assets/css/style.css` with `--teal`, `--text-2`, and `--gutter`]
- **Breakpoints:** [FILL IN: the widths the existing media queries use, for example `max-width`
  1080, 1024, 900, and 640 px]
- **Scripts:** [FILL IN: where behavior lives and how it's organized, for example
  `assets/js/site.js`, one strict-mode immediately invoked function expression (IIFE) with an
  `el()` helper that builds elements and a `session` helper that wraps `sessionStorage`]
- **JavaScript hook:** [FILL IN: the class that marks JavaScript as running, for example `js` on
  `<html>`, or "none"]
- **Build and dependencies:** [FILL IN: "none" if files are served exactly as written, with no
  framework, package, or build step; otherwise the toolchain and its build command]
- **Browser support:** [FILL IN: the browsers the site must work in, and how to check whether
  they support a feature, for example "Baseline widely available features, checked on MDN", or
  the last two versions of Chrome, Edge, Firefox, and Safari]
- **Cache busting:** [FILL IN: how stylesheet and script URLs change when the files change, for
  example `?v={{ site.time | date: '%s' }}`, or "none"]
- **Hosting:** [FILL IN: where the site is served and what that limits, for example GitHub Pages
  with the `github-pages` gem, which pins Jekyll 3.x and allows only a fixed list of plugins]
- **Page indexes:** [FILL IN: generated files that list the site's pages, for example
  `sitemap.xml`, `llms.txt`, and `llms-full.txt`, or "none"]
- **Preview command:** [FILL IN: how to serve the site locally, for example
  `bundle exec jekyll serve`, or "none" if you open the files directly]
- **Test tools:** [FILL IN: the automated front-end checks and their commands, for example the Nu
  HTML Checker, axe, Lighthouse, or Playwright tests, or "none"]

## Decisions that are the user's

Stop and ask the user before you:

- add a framework, package, third-party script, font, or tracker;
- change the design (colors, type, spacing, layout, or tokens) beyond what was asked;
- change or remove a published URL;
- collect any data from visitors, through a form, analytics, or a cookie;
- or weaken an accessibility requirement, a lint, or a check.

## Making a change

- **Read first.** Read the page's template, the components and tokens already in the
  **Stylesheets**, and how the **Scripts** are organized. Reuse an existing component or class
  before you add one.
- **Check each step in the browser.** Look at each step with the **Preview command**, not only in
  the source. Markup that looks right in an editor can still overflow on a phone or lose its focus
  outline.
- **Fix the cause, not the symptom.** Find the element that makes a page scroll sideways instead of
  hiding overflow on `body`. Lower the specificity that wins instead of adding `!important`, and fix
  the stacking context instead of raising a `z-index`.
- **Don't paper over problems.** Never add `!important`, a magic number, a `setTimeout` that waits
  for rendering, browser sniffing, or an ARIA attribute only to make a symptom or an audit warning
  go away. Work out why it happens, then fix that.

## HTML

- Every page gets its doctype, `lang`, charset, viewport, and metadata from the **Page head**.
  Don't hand-write a second `<head>`, and don't add per-page meta tags anywhere else. If the
  **Page head** is "none", give every page all of these itself.
- Give every page a unique `<title>`, with the page's name before the site's, and a meta
  description. Set `lang` on `<html>`, and on any passage in another language, so screen
  readers pronounce it correctly.
- Use semantic elements: `header`, `nav` (with an `aria-label` when there is more than one),
  exactly one `main`, `article`, `section` (always with a heading), `aside`, `footer`, `figure`
  with `figcaption`, `time datetime="…"`, and `ul` or `ol` for lists. Use `table` only for
  tabular data, with a `caption` and `th scope="col|row"`. Use `div` and `span` only as styling
  hooks.
- Use one `<h1>` per page, with headings in order. Choose a heading level for structure, not for
  its size.
- Start every page whose navigation comes before its content with a skip link to `main`, which
  appears when it receives focus (WCAG 2.4.1, Bypass Blocks).
- Use `<a href>` to go somewhere and `<button type="button">` to do something. Never make a `div`
  or `span` clickable. Always give a button a `type`.
- Use native elements before building your own: `<dialog>` opened with `showModal()` for a
  modal, which keeps the rest of the page out of reach and closes on Escape; `<details>` and
  `<summary>` for a disclosure; and `<select>` or radio buttons for a choice.
- Give every control an accessible name: visible text, an `aria-label`, or text inside a visually
  hidden class such as `.sr-only`. An icon-only menu button needs one of the last two.
- Accessible Rich Internet Applications (ARIA) attributes:
  - Don't use ARIA when a native element or attribute does the job. Use `hidden`, not
    `aria-hidden` plus CSS, to hide content from everyone.
  - When ARIA is used, keep it in sync from JavaScript (`aria-expanded`, `aria-controls`,
    `aria-current="page"`).
  - Give decorative SVG icons `aria-hidden="true"`.
- Images:
  - Always include `alt`, plus `width` and `height` so the layout doesn't shift as images load.
  - Offer several sizes with `srcset` and `sizes`, or several formats with `<picture>`, so each
    screen downloads only the pixels it shows.
  - Add `loading="lazy"` and `decoding="async"` to images below the fold, but never to the
    largest image on the first screen. Give that one `fetchpriority="high"`; browsers that don't
    support the attribute ignore it.
  - Use SVG for icons and compressed WebP, AVIF, or PNG for pictures.
- Links:
  - Build internal URLs with the URL helpers from **Templates**, not hard-coded paths. With no
    template language, use relative paths, which keep working when the site is served from a
    subfolder.
  - Open only external links in a new tab. Give them `rel="noopener"`, which older browsers
    need, keep `me` on identity links, and say in visible or visually hidden text that the link
    opens a new tab.
- Forms:
  - Give every input a `<label for>`, the right `type` (`search`, `email`, `url`), and
    `autocomplete` where it applies. A placeholder is never a label.
  - Use the browser's validation attributes (`required`, `type`, `min`, `max`, `pattern`)
    first.
  - Show each error as text beside its field, linked with `aria-describedby`, and set
    `aria-invalid="true"` on the field. Say what is wrong and how to fix it (WCAG 3.3.1 and
    3.3.3). When a submission fails, move focus to the first field with an error.
  - Validate again on the server when there is one. Checks in the browser help the user, but
    anyone can bypass them.
- Markup style:
  - Use lowercase element and attribute names, double-quoted attribute values, and boolean
    attributes without values (`hidden`, `defer`).
  - Don't use inline `style` attributes or `on*` handlers: styles belong in the **Stylesheets**
    and behavior in the **Scripts**.
  - Match the file's existing convention for void elements, such as whether `<meta …>` has a
    trailing slash.
- Escape template output for its context with the **Templates** helpers: HTML escaping inside
  attributes, JSON encoding inside `<script>` blocks such as JSON for Linked Data (JSON-LD), and
  stripped tags with normalized whitespace for descriptions. In Liquid these are `| escape`,
  `| jsonify`, and `| strip_html | normalize_whitespace`.

## CSS

- Keep all styles in the **Stylesheets**, and use the **Design tokens** instead of new
  hard-coded colors or sizes. Add a token when a value is new and will be reused.
- Name classes with block, element, modifier (BEM) syntax (`block__element--modifier`) and state
  classes with `is-` (`is-open`, `is-current`). JavaScript selects `data-*` hooks; CSS styles
  classes. Don't style by ID. If the stylesheets already follow another naming convention, match
  it instead.
- Keep specificity low: one class per selector where possible, no deep descendant chains, and no
  `!important` outside the visually hidden class, the reduced-motion block, and print styles.
  Wrap base and reset selectors in `:where()`, which adds no specificity, so one class overrides
  them.
- Use flexbox or grid with `gap` for layout. Use `rem`, `em`, `%`, and `clamp()` for type and
  spacing, so text follows the user's font size setting, and avoid fixed heights on anything that
  holds text.
- Reuse the **Breakpoints** instead of adding new ones. Use a container query (`@container`)
  when a component must adapt to the space it is placed in rather than to the viewport.
- Use logical properties (`margin-inline`, `padding-block`, `inset-inline-start`) where a layout
  must also work in a right-to-left language.
- If the site has a dark theme, redefine the **Design tokens** under
  `prefers-color-scheme: dark`, set the `color-scheme` property so form controls and scrollbars
  match, and check contrast in both themes.
- Don't put information or actions behind hover alone, because touch screens have no hover.
  Scope effects that only make sense with a mouse in `@media (hover: hover)`.
- Wrap a feature outside the **Browser support** in `@supports`, with a fallback that still
  works.
- Meet the Web Content Accessibility Guidelines (WCAG) 2.2 at level AA:
  - Contrast of at least 4.5:1 for body text and 3:1 for large text, icons, borders of controls,
    and focus indicators.
  - Targets of at least 24 × 24 px; 44 × 44 px is better for primary actions.
  - Pages that work from 320 px wide up with no horizontal scrolling, and with text zoomed to
    200%.
  - Never remove the `:focus-visible` outline without replacing it with something as visible,
    and never let a sticky header cover the focused element; `scroll-padding-top` keeps it
    clear.
  - Draw focus rings and control borders with `outline` or `border`, not `box-shadow` alone.
    Forced-colors mode (such as Windows contrast themes) removes box shadows, while a
    `transparent` outline becomes visible there.
  - Never use color alone to show state or meaning.
- Motion:
  - Animate only `transform` and `opacity`, which the browser can animate without recalculating
    layout.
  - Add every new animation to the `prefers-reduced-motion: reduce` block.
  - Give anything that moves on its own for more than five seconds, such as a carousel, a control
    to pause it (WCAG 2.2.2, Pause, Stop, Hide).
- Keep any `@media print` styles working.

## JavaScript

- Use progressive enhancement. Every page must work without its scripts: content and links are
  in the HTML, and the script adds behavior. Show UI that only works with JavaScript through the
  **JavaScript hook**, so it never appears broken without it.
- If **Build and dependencies** is "none", write plain JavaScript with no framework, package, or
  build step, because the host serves the files exactly as they are. Otherwise use the toolchain
  named there, and add no new package without a stated reason.
- Follow the structure in **Scripts**: add code inside the existing module or function rather
  than creating new globals. Use strict mode (modules have it by default), `const` (or `let` if
  the value changes), never `var`, and `===`.
- Load scripts with `defer` or as modules (`type="module"`, which defer by default), never as a
  blocking script in `<head>`.
- Build Document Object Model (DOM) nodes with `document.createElement` (or the helper named in
  **Scripts**) and `textContent`, as "Security and privacy" requires.
- Guard every lookup (`if (!node) return;`) so a missing element on one page can't break the
  others.
- Events:
  - Attach events with `addEventListener`, and use event delegation for lists.
  - Mark `touchstart`, `touchmove`, and `wheel` listeners that never call `preventDefault()`
    with `{ passive: true }`, so scrolling doesn't wait for them.
  - Debounce handlers for input that fires often, such as typing into a search box.
  - Remove listeners, observers, and timers when the element they serve goes away; passing an
    `AbortController`'s `signal` to `addEventListener` removes a group of listeners at once.
- Detect features (`'IntersectionObserver' in window`), never browsers. User-agent strings
  misreport and change.
- Read layout (sizes, positions) before you change the DOM, not between changes, so the browser
  calculates layout once. Make visual updates in `requestAnimationFrame`, and use
  `IntersectionObserver` instead of scroll handlers to react to elements coming into view.
- Wrap storage access (`localStorage`, `sessionStorage`) in `try`/`catch`, because it throws in
  some private browsing modes and when storage is full or blocked.
- Network calls:
  - `fetch` rejects only when the request can't complete (a network failure, a blocked
    cross-origin request, or an abort). An HTTP error such as 404 or 500 resolves normally, so
    check `response.ok`.
  - Time out every request with `AbortSignal.timeout()`, and abort a request that a newer one
    replaces, such as an earlier search.
  - Handle failure, rate limiting (HTTP 429, and 403 from APIs such as GitHub's), and offline
    use. Keep the static content as the fallback, and cache results in `sessionStorage`.
- When content changes without a page load:
  - Announce status messages, such as "3 results" or "Saved", through an `aria-live="polite"`
    region (WCAG 4.1.3, Status Messages).
  - When new content replaces the main view, move focus to its heading (give the heading
    `tabindex="-1"` so it can take focus).
  - Keep state worth sharing (filters, tabs, search terms) in the URL with `history.pushState`
    or `replaceState`, and handle `popstate`, so links and the Back button work.
- Keyboard:
  - A menu or panel that opens must be reachable with Tab, close on Escape, and return focus to
    the control that opened it.
  - A tooltip or other content that appears on hover or focus must stay while the pointer is
    over it, and close on Escape (WCAG 1.4.13, Content on Hover or Focus).
- Respect `prefers-reduced-motion` for scrolling and animation. Don't leave `console.log` calls
  behind.

## Languages

Follow this section when the **Languages** value lists more than one language. With "English
only", the first two points still apply, so the site can be translated later.

- Set `lang` and `dir` from the **Page head**: `lang` to the page's language tag (`es`,
  `zh-Hans`), and `dir="rtl"` on `<html>` for Arabic and Urdu. Browsers use `lang` to choose
  fonts and glyphs, and screen readers to choose a voice (WCAG 3.1.1, Language of Page).
- Lay out with logical properties and values, as the CSS section says: `margin-inline-start`,
  not `margin-left`, and `text-align: start`, not `left`. Flexbox and grid already follow the
  page's direction. On right-to-left pages, mirror icons that point forward or back, such as
  arrows and chevrons.
- Keep the text that scripts show, such as "3 results" or an error, out of the script's code. Put
  it in the page, for example in a `<script type="application/json">` block that the template
  fills for each language, or in the string files the **Languages** value names.
- Never build a sentence from pieces, and never choose a word form with `n === 1`. Count with
  `Intl.PluralRules`, which knows each language's forms: `new Intl.PluralRules("ar").select(3)`
  returns `"few"`. Format numbers, dates, and lists with `Intl.NumberFormat`,
  `Intl.DateTimeFormat`, and `Intl.ListFormat` in the page's language
  (`document.documentElement.lang`).
- Wrap text whose direction you can't know, such as a user's name inside a sentence, in
  `<bdi>`, and give free-text inputs `dir="auto"`. Otherwise an Arabic name in an English
  sentence, or a Latin one in an Arabic sentence, can reorder the words around it.
- Link each page's translations to each other in the **Page head**: every version lists every
  version, itself included, with `<link rel="alternate" hreflang="…" href="…">`, and
  `hreflang="x-default"` names the page for readers whose language the site doesn't have.
- Name each language in itself in the language menu ("Español", "العربية"), with `lang` and
  `hreflang` on each link. Don't use flags: a flag stands for a country, and Spanish, Arabic, and
  Portuguese are each spoken in many. Never choose the language from the reader's location. Once
  a reader picks one, keep them in it: each page links to the same language's other pages.
- Make sure the fonts cover every script the site ships, and ask before adding one, as
  "Decisions that are the user's" says. Give a script's font a `unicode-range` in `@font-face`,
  so browsers download it only for pages that use its characters. Check the line height, too:
  Urdu's Nastaliq style, and the marks above and below Devanagari and Bengali letters, often need
  more than Latin text.
- Leave room for longer text. Translations of labels up to 10 characters can run two to three
  times the English length, so let buttons and labels grow and wrap instead of setting their
  width.
- Treat translations you write as drafts, and list the pages and strings in your report for a
  native speaker to review.

## Security and privacy

- Never put outside data (API responses, URL parameters, user input) into `innerHTML`,
  `outerHTML`, `insertAdjacentHTML`, or `document.write`; any markup in it would run as part of
  the page. Set text with `textContent`.
- Before you put a URL from data into `href` or `src`, check that its protocol is `https:` or
  `http:`. A `javascript:` URL runs code when someone follows it.
- Never use `eval`, `new Function`, or a string passed to `setTimeout` or `setInterval`.
- Never put a secret (an API key, a token, or a password) in front-end code. Everything sent to
  the browser is public.
- Don't keep tokens or personal data in `localStorage` or `sessionStorage`: any script on the
  page can read them.
- Host third-party files yourself where you can. If one must load from another origin, pin its
  version and add an `integrity` hash (Subresource Integrity) with `crossorigin="anonymous"`, so
  the browser refuses a file that changed.
- Keep pages compatible with a strict Content Security Policy (CSP), the header or `<meta>` tag
  that limits where scripts and styles may come from: no inline scripts, inline styles, or `on*`
  handlers.
- Collect no data from visitors, and send none to a third party, without the user's approval
  (see "Decisions that are the user's").

## Performance

- Don't add third-party scripts, trackers, or font families without a stated reason. Load heavy
  embeds such as video players and maps only when a visitor asks for them, behind a static
  preview; that also keeps their tracking off the page until then.
- Fonts: use WOFF2 files, and load only the weights and styles the pages use. Keep
  `font-display: swap` (`display=swap` for Google Fonts) and a `preconnect` to a font host, and
  preload at most the one font file the first screen needs.
- Reserve space for everything that loads late (images, embeds, banners) with `width` and
  `height` or `aspect-ratio`, so content doesn't jump.
- Keep the **Cache busting** on every stylesheet and script link.
- Aim for the "good" range of Core Web Vitals, measured at the 75th percentile of page loads:
  Largest Contentful Paint (LCP) of 2.5 s or less, Interaction to Next Paint (INP) of 200 ms or
  less, and Cumulative Layout Shift (CLS) of 0.1 or less.
- Measure instead of guessing. Use field data from real visitors where it exists (the Chrome UX
  Report, shown in PageSpeed Insights), and lab tools such as Lighthouse with mobile throttling
  otherwise. A performance claim needs the numbers, the tool, and the device and network profile.

## Hosting and build

- Use only features the **Hosting** supports. On GitHub Pages with the `github-pages` gem, for
  example, that means no Jekyll 4-only features and no plugins outside its allowlist.
- When you add a top-level page, check that each of the **Page indexes** lists it.
- A YAML error in the site's config or data files can stop the whole build, so nothing deploys
  until it is fixed. Follow the YAML rules and the parse check in `writing.md`.

## Before finishing

1. Run the **Preview command** and read the rendered page, not only the source.
2. Check the layout at 320 px, at 375 px, and at desktop width, with no horizontal scrolling at
   any of them, and with text zoomed to 200%.
3. Use the page with only the keyboard. Every control is reachable in a logical order, focus is
   always visible and never hidden under a sticky header, and Escape closes what opened.
4. If you changed an interactive component, check it with a screen reader you can run
   (VoiceOver on macOS and iOS, NVDA on Windows, Orca on Linux, or TalkBack on Android). Each
   control's name, role, and state, and each status message, are announced.
5. If you changed styles, check the dark theme (if there is one), forced colors, and reduced
   motion; browser developer tools can emulate all three. If you changed a script, check the page
   with JavaScript turned off.
6. Run the **Test tools**. Automated accessibility checks find only some problems, so steps 3
   and 4 still matter. Check the browser console for errors, the network panel for failed
   requests, and the page for broken links.
7. Check the page in each browser engine the **Browser support** covers that you can run:
   Chromium (Chrome and Edge), Gecko (Firefox), and WebKit (Safari). Say which you couldn't.
8. If you changed a page that has translations, check it in each language the **Languages**
   value lists, a right-to-left one included, at the widths in step 2.
9. If you changed a config file, a data file, or front matter, check that it parses with the
   command in `writing.md`.
10. Check changed page text against `writing.md`, including its two-reader check.
11. Review your diff as a reviewer would. Look for inline styles, hard-coded colors or sizes,
    missing `alt` text or labels, controls without an accessible name, outside data in `innerHTML`,
    and leftover `console.log` calls. Then report what you checked, what you didn't, and what
    remains.
