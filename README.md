# KnowledgeHub

an attempt to make a lightweight QA service for using inside corporate infrastructures

This is a work-in-progress project. It's built on top of [python glasskit framework](https://pypi.org/project/glasskit/),
the UI is a vue.js SPA.

## Bootstrap

1. Clone the repository
2. Create a virtualenv
3. Install dependencies with `pip install -r requirements.txt`
4. Run the backend dev server with `./glass.py run`
5. Open another terminal and run background task server with `./glass.py tasks`
6. To make search engine work install elasticsearch and run it with a default configuration. Then you have to run `./glass.py elastic index -a -d` at least once to create indexes. New posts are re-indexed automatically with the background task server.
7. Open another terminal and cd to `ui` directory.
8. Run `yarn` or `npm i` to install dependencies
9. Run `yarn serve` or `npm run serve` to build and serve the UI.
10. Open `http://localhost:8080` to see the result
