# Backend status

There is no separate backend source in this deployed version.

- Hosting serves static files from dist/.
- Quizzes are scored in dist/app.js.
- Student notes and progress are stored in the browser, not a database.
- The chatbot runs in dist/chat.js using prepared guidance and course-text retrieval.
- No server-side routes, authentication service, API keys or generative AI model are configured.

A future backend would be new development, for example to add student accounts, cross-device progress, teacher dashboards or an AI API. This package contains the actual existing implementation, not placeholder backend code.
