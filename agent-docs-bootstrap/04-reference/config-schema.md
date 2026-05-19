# Configuration Schema

Complete reference for configuration options.

## File Location

Default: `./config.json`  
Environment variable: `CONFIG_PATH`

## Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "optionName": {
      "type": "string",
      "description": "Description of this option",
      "default": "default-value",
      "examples": ["example1", "example2"]
    }
  }
}
```

## Options

### `optionName`

| Property | Value |
|----------|-------|
| Type | `string` |
| Default | `"default-value"` |
| Environment | `OPTION_NAME` |

Description of what this option controls and when to use it.

**Valid values**: `value1`, `value2`, `value3`

---

### `nested.object`

Nested configuration object.

| Property | Value |
|----------|-------|
| Type | `object` |
| Required | No |

```json
{
  "nested": {
    "object": {
      "key": "value"
    }
  }
}
```
