# CRC College Application Course — source code

Export of published version 3, 30 September 2026.
Source commit: e36f1e271831558bfce6dc471468b6758b104535
Live course: https://crc.denis690942.chatgpt.site

## Architecture

This is a static HTML, CSS and JavaScript application. There is no application backend, database, server-side API, student login service or generative AI service in the current version. Everything needed to run the course is in `dist/`.

## Run locally

Extract this ZIP. In a terminal, open the CRC_Course folder and run:

```sh
python -m http.server 8000 --directory dist
```

On Windows, you can use `py` instead of `python`. Open http://localhost:8000 in your browser. Python is only a local development file server; it is not a course backend. Stop it with Ctrl+C. No npm installation or build command is needed.

## Deploy on your own hosting

Upload the CONTENTS of `dist/` to the website's public folder, keeping subfolders intact. `index.html` must be at the public root. A static host is sufficient. Navigation uses hash routes, so no application-route rewrite rules are needed. Use HTTPS for a public deployment.

Do not upload the whole source ZIP, the authoring scripts or tests as the public site. No API keys, database credentials or environment variables are required.

## Main frontend files

| File | Purpose |
| --- | --- |
| dist/index.html | Page shell, navigation and script loading |
| dist/style.css | Course layout, responsive styling and printing |
| dist/app.js | Lesson views, quizzes, progress and workbook export |
| dist/course-data.js | 13 modules, 53 lessons, 39 quiz questions and core resources |
| dist/extension-ui.js | EY–S6 pathways, roadmap and career-resource views |
| dist/extension-data.js | Index of 38 supplied career resource PDFs |
| dist/chat.js | Course chatbot: prepared answers, text retrieval and chat interface |
| dist/chat.css | Chatbot layout and styling |
| dist/assets/ | Companion Word/PDF guides, posters, graphics and career PDFs |

## Edit content

Edit the lesson/module data in `dist/course-data.js`. Keep existing lesson IDs and module IDs when revising content so stored student progress remains associated with the same lessons. Each module currently uses three quiz questions; the passing threshold is two correct answers. Changing quiz length requires corresponding updates to the UI and scoring rules in app.js.

Edit chatbot prepared responses in the `entries` array in `dist/chat.js`. The chatbot also searches lesson text from course-data.js. It has no live web access and does not generate new AI responses. Update answer guidance when course requirements change.

## Student data

Progress, notes and quiz responses use the browser's localStorage key `college-course-v1`. They are not sent to a backend or synchronised between devices. Changing the domain or browser creates a different storage context. Students should download their workbook before moving sites. The TXT workbook export is for reading; the current course does not import it.

Chat questions remain in memory in the current tab, and are cleared on reload or by Clear chat. No chatbot network requests are made. Shared-device users should download their work and clear course data before leaving.

## Verification

With Node.js installed, run from this folder:

```sh
node check-course.cjs
node check-chat.cjs
```

These are lightweight logic checks, not complete browser or accessibility tests. Check desktop/mobile layout and keyboard navigation in your target browser before a new deployment. Test count expectations need updating if lessons or quizzes are added.

## Authoring scripts

`authoring/` contains the original Python scripts used to produce and extend the course. They are historical authoring sources, not runtime dependencies. They contain paths from the original workspace and require adaptation before use elsewhere. The original source curriculum attachments are not all included; the internal-use curriculum is not distributed in this package. Some scripts overwrite generated files or apply edits that are not safe to repeat. Edit the ready-to-run dist files directly for normal maintenance.

## Included source materials

Third-party PDFs and images retain their original credits. Inclusion in this export does not grant new rights to those materials. The student activities and fictional examples are identified in the course. The 50-page Word/PDF guides cover the original ten modules; the added modules are available online.
