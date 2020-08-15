# KnowledgeHub

an attempt to make a lightweight QA service for using inside corporate infrastructures

This is a work-in-progress project. It's built on top of [python glasskit framework](https://pypi.org/project/glasskit/),
the UI is a vue.js SPA.

## Bootstrap

1. Clone the repository
2. Copy `app/config/development.py.example` to `app/config/development.py` and make changes mentioned in comment on top of the file. Basically you need to fill up settings for at least one OAuth provider and disable those you don't need (i.e. remove them from configuration completely). The same thing should be done to the `bot` section of configuration file to enable/disable particular messenger bots.
3. Run `docker-compose up --build`. This will build and run containers for database, elasticsearch, memcached, backend and the task server. The backend is exposed on port 5000 to your localhost.
   
   3a. If you're running the dev server for the first time you have to prepare indexes in elasticsearch. You're going to need to run a command in your backend container:
   `docker exec -it ask_backend /opt/app/glass.py elastic index -a -d`.
   
4. Open another terminal and cd into `ui` directory.
5. Run `yarn` or `npm i` to install dependencies
6. Run `yarn serve` or `npm run serve` to build and serve the UI.
7. Open `http://localhost:8080` to see the result
