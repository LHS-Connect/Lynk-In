# The LHS Connect Rewrite - 2026 Edition

###### Please add as we find more important goals

Yeah, it seems like we do this every couple years, but we're hoping this one could be different

### The mission:

#### Making LHS Connect more accessible for the average student

Creating an acutal place where people can see what's going on at school, instead of a more well designed version of the SPS page.

#### Making LHS Connect more manageable on the daily.

#### Rewriting LHS Connect to make sense

---

## Setup & Development

This project uses [Node.js](https://nodejs.org/) only to manage a Git hook via [husky](https://typicode.github.io/husky/). All Node-related files (`package.json`, etc.) live in the repository root (`Lynk-In`).

### Installation

```bash
# install node dependencies (husky and dev-server)
npm install

# set up husky hooks (runs automatically thanks to "prepare" script)
npm run prepare
```

### Development server

Some JavaScript features (such as module imports or filesystem access) require a server context.  Run the built-in development server during development:

```bash
npm run dev
```

The command launches `http-server` serving the project folder at `http://localhost:8080` (cache disabled with `-c-1`).

A `pre-commit` hook has been configured to keep a `git-log.txt` file up to date; it rewrites the log every time you commit.

### Running

There is no build step – just open `index.html` in a browser. The only remaining script is `horiz-scroll-fix.js`, which enables vertical wheel motion on horizontal scrollers.

```bash
# open in default browser (Linux example)
xdg-open index.html
```

Feel free to extend these instructions as the project grows.
