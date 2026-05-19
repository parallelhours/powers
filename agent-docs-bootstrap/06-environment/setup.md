# Environment Setup

Complete guide to setting up your development environment.

## Requirements

| Tool | Version | Install |
|------|---------|---------|
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| npm | 9+ | Included with Node.js |
| Git | 2.30+ | [git-scm.com](https://git-scm.com) |

## Setup Steps

### 1. Install Node.js

Using [nvm](https://github.com/nvm-sh/nvm) (recommended):

```bash
nvm install 18
nvm use 18
```

### 2. Clone and Install

```bash
git clone https://github.com/user/repo.git
cd repo
npm install
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Verify Setup

```bash
npm run doctor
```

## IDE Setup

### VS Code

Recommended extensions:

- ESLint
- Prettier
- [Language Server]

Workspace settings are in `.vscode/settings.json`.

### IntelliJ IDEA

Import settings from `.idea/`.
