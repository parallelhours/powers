# Runbook: Deployment

## Pre-deployment Checklist

- [ ] All tests passing in CI
- [ ] Code review approved
- [ ] Deployment noted in the team's communication channel (e.g., #releases in Slack, a Teams channel, or equivalent)
- [ ] On-call engineer available for 30 minutes post-deploy

## Deployment Steps

### 1. Prepare Release

```bash
# Create release branch
git checkout main
git pull origin main
git checkout -b release/vX.Y.Z
```

### 2. Run Pre-deployment Checks

```bash
npm run test
npm run lint
npm run build
```

### 3. Deploy

**Staging**:
```bash
npm run deploy:staging
```

**Production**:
```bash
npm run deploy:production
```

### 4. Verify Deployment

- [ ] Health check passing
- [ ] Basic functionality smoke test
- [ ] No increase in error rates

## Rollback

If issues detected:

```bash
npm run rollback:production
```

Then notify the team in your incident response channel (e.g., #incidents in Slack, a Teams channel, or equivalent).
