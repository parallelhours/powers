# Common Errors

Solutions for frequently encountered errors.

## Error: `MODULE_NOT_FOUND`

**Problem**: Required module cannot be found.

**Cause**: Dependencies not installed or path issue.

**Solution**:
```bash
npm install
```

If that doesn't work:
```bash
rm -rf node_modules
npm install
```

---

## Error: `ECONNREFUSED`

**Problem**: Cannot connect to service.

**Cause**: Service not running or wrong port.

**Solution**:
1. Check service is running:
   ```bash
   npm run status
   ```
2. Verify port in config matches running service
3. Check firewall rules

---

## Error: `PERMISSION_DENIED`

**Problem**: Insufficient permissions.

**Solution**:
```bash
# Fix file permissions
chmod +x ./bin/command

# Or for directory
chmod 755 ./data
```
