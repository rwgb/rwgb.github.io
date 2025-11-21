# Notion Sync Enhancements

## Summary of Improvements

All requested enhancements have been successfully implemented:

### 1. ✅ Verbose Logging
- **Added comprehensive logging system** with configurable verbosity
- **Detailed progress tracking** at each step of the sync process
- **Color-coded output** with emojis for easy scanning
- **Debug mode** showing API calls, property extraction, and file operations

**Usage:**
```bash
# Enable via environment variable
export VERBOSE=true
python scripts/notion-sync.py

# Or use command line flag
python scripts/notion-sync.py --verbose
```

### 2. ✅ Configurable Sync Frequency
- **Flexible cron scheduling** in GitHub Actions workflow
- **Commented examples** for common frequencies (30min, hourly, daily, etc.)
- **Manual trigger support** with workflow_dispatch
- **Easy customization** via workflow file

**Common Frequencies:**
- Every 30 minutes: `*/30 * * * *`
- Every 2 hours: `0 */2 * * *`
- Every 6 hours: `0 */6 * * *`
- Daily at midnight: `0 0 * * *`
- Weekdays at 9am: `0 9 * * 1-5`

### 3. ✅ Retry Logic with Exponential Backoff
- **Automatic retry** for failed API calls
- **Configurable retry attempts** (default: 3)
- **Exponential backoff** strategy to handle rate limiting
- **Detailed retry logging** showing attempt numbers

**Configuration:**
```bash
export MAX_RETRIES=5      # Default: 3
export RETRY_DELAY=2      # Default: 2 seconds
```

### 4. ✅ Dry-Run Mode
- **Preview changes** without making any modifications
- **Safe testing** of sync configuration
- **Shows what would be created/updated/deleted**
- **No actual file operations** performed

**Usage:**
```bash
# Preview sync without changes
python scripts/notion-sync.py --dry-run

# Combine with verbose for detailed preview
python scripts/notion-sync.py --dry-run --verbose
```

### 5. ✅ Sync Statistics
- **Comprehensive metrics** tracked for each sync
- **Detailed breakdown** of operations:
  - Posts created
  - Posts updated
  - Posts deleted
  - Errors encountered
  - Total duration
- **Summary output** at end of each sync

**Example Output:**
```
📊 Statistics:
   Created: 2
   Updated: 1
   Deleted: 0
   Errors:  0
   Duration: 3.5s
```

### 6. ✅ Health Check System
- **Pre-sync validation** of configuration
- **Authentication verification** with user info
- **Database access confirmation** with title
- **Schema validation** checking required properties
- **Detailed error messages** for common issues

**Checks Performed:**
- ✓ Authentication successful
- ✓ Database accessible
- ✓ Required properties present
- ⚠️ Warnings for missing optional properties

### 7. ✅ Enhanced Error Handling
- **Graceful error recovery** with try-catch blocks
- **Specific error messages** for common issues:
  - 401: Invalid token
  - 403: Insufficient permissions
  - 404: Database not found
- **Non-zero exit codes** on failure
- **Continues processing** other posts on individual failures

## New Features

### Command Line Arguments

```bash
python scripts/notion-sync.py [OPTIONS]

Options:
  --dry-run      Preview changes without applying them
  -v, --verbose  Enable verbose logging
  -h, --help     Show help message
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NOTION_TOKEN` | Integration token | Required |
| `NOTION_DATABASE_ID` | Database ID | Required |
| `VERBOSE` | Enable verbose logging | `false` |
| `MAX_RETRIES` | Max retry attempts | `3` |
| `RETRY_DELAY` | Initial retry delay (seconds) | `2` |

### GitHub Actions Workflow Inputs

Manual trigger now supports:
- **Verbose logging**: Enable detailed output
- **Dry run**: Preview changes without applying

Access via: Repository → Actions → "Sync Notion to Hugo" → "Run workflow"

## Troubleshooting Section

Added comprehensive troubleshooting guide to `notion-sync.md` covering:

### Common Issues
1. **Post status set to "Published" but not syncing**
   - Integration not connected
   - Wrong database ID
   - GitHub Actions not running
   - Missing required properties

2. **Posts not syncing at all**
   - Authentication failures
   - Permission issues
   - Database not found

3. **Some posts sync, others don't**
   - Status property case-sensitivity
   - Property name mismatches
   - Unsupported content formats

### Diagnostic Tools
- Verbose logging for detailed output
- Dry-run mode for safe testing
- Health checks for configuration validation
- Sync statistics for monitoring

### Configuration Guides
- Adjusting sync frequency
- Customizing retry behavior
- Interpreting sync statistics
- Database schema verification

## Usage Examples

### Basic Sync
```bash
python scripts/notion-sync.py
```

### Diagnostic Sync
```bash
# Full diagnostic run with no changes
python scripts/notion-sync.py --verbose --dry-run
```

### Testing Configuration
```bash
# Test with custom retry settings
export MAX_RETRIES=5
export RETRY_DELAY=3
python scripts/notion-sync.py --verbose
```

### Manual Workflow Trigger
1. Go to GitHub repository
2. Navigate to Actions tab
3. Select "Sync Notion to Hugo"
4. Click "Run workflow"
5. Enable options as needed:
   - ☑️ Enable verbose logging
   - ☑️ Dry run

## Benefits

1. **Easier Debugging**: Verbose logging helps identify issues quickly
2. **Safer Testing**: Dry-run mode prevents accidental changes
3. **Better Reliability**: Retry logic handles transient failures
4. **More Visibility**: Statistics show exactly what happened
5. **Faster Diagnosis**: Health checks catch configuration issues early
6. **Flexible Scheduling**: Customize frequency to your needs
7. **Comprehensive Documentation**: Troubleshooting guide for common issues

## Migration Notes

### For Existing Users

The enhanced script is **fully backward compatible**:
- Default behavior unchanged when run without flags
- Environment variables remain the same
- GitHub Actions workflow continues working as before
- No breaking changes to output files

### Recommended Steps

1. **Test locally first**:
   ```bash
   python scripts/notion-sync.py --dry-run --verbose
   ```

2. **Review health check output** to verify configuration

3. **Run actual sync** and review statistics

4. **Update workflow file** to customize frequency if desired

5. **Add manual trigger inputs** for easier debugging

## Future Enhancements

Potential additions based on this foundation:

1. **Slack/Discord notifications** on sync completion
2. **Metrics dashboard** tracking sync history
3. **Content validation** rules before publishing
4. **Multi-database support** for different content types
5. **Incremental syncs** using lastEditedTime
6. **Image optimization** and CDN upload
7. **Custom block type handlers** for specialized content

## Support

For issues or questions:
- Review the troubleshooting guide in `notion-sync.md`
- Enable verbose logging for detailed diagnostics
- Use dry-run mode to test safely
- Check GitHub Actions logs for workflow issues
