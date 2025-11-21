# Changelog

All notable changes to the Notion Sync project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Verbose Logging System**
  - Configurable logging levels with `--verbose` or `-v` flag
  - Debug-level logging for detailed troubleshooting
  - Timestamped log messages with severity levels
  - Environment variable `VERBOSE` for persistent configuration

- **Retry Logic with Exponential Backoff**
  - Automatic retry for failed API calls
  - Configurable retry attempts via `MAX_RETRIES` (default: 3)
  - Configurable retry delay via `RETRY_DELAY` (default: 2 seconds)
  - Exponential backoff strategy to handle rate limiting
  - Detailed logging of retry attempts

- **Dry-Run Mode**
  - Preview changes without modifying files with `--dry-run` flag
  - Shows what would be created, updated, or deleted
  - Safe testing of sync configuration
  - Useful for validating Notion content before publishing

- **Comprehensive Health Check System**
  - Pre-sync validation of API connectivity
  - Authentication verification with user information
  - Database access confirmation with title display
  - Schema validation for required properties
  - Specific error messages for common issues (401, 403, 404)

- **Sync Statistics Tracking**
  - Tracks posts created, updated, and deleted
  - Error counting and reporting
  - Duration measurement
  - Detailed summary at end of each sync
  - Statistics object for programmatic access

- **Enhanced Error Handling**
  - Graceful error recovery with try-catch blocks
  - Specific error messages for different failure types
  - Non-zero exit codes on failure
  - Continues processing remaining posts on individual failures
  - HTTP status code interpretation

- **Command-Line Interface**
  - Argument parsing with `argparse`
  - Help documentation with examples
  - Support for multiple flags simultaneously
  - Environment variable documentation in help text

- **Configurable Sync Frequency**
  - GitHub Actions workflow with customizable cron schedule
  - Commented examples for common frequencies
  - Manual workflow trigger support
  - Workflow inputs for verbose and dry-run modes

- **Comprehensive Troubleshooting Documentation**
  - Detailed troubleshooting guide in `notion-sync.md`
  - Common synchronization issues with solutions
  - Diagnostic steps for each problem
  - Usage examples for new features
  - Best practices section
  - Frequency adjustment guide

- **Type Hints**
  - Added type annotations throughout the codebase
  - Improved code clarity and IDE support
  - Better error detection

### Changed
- **Script Architecture**
  - Refactored from 228 to 489 lines
  - Modular function design
  - Improved separation of concerns
  - Better code organization

- **API Calls**
  - Added timeout parameters (30s) to all requests
  - Wrapped database queries with retry decorator
  - Enhanced error handling for API failures

- **File Operations**
  - Differentiates between creating and updating posts
  - Better tracking of synced files
  - Improved deletion logic

- **Logging Output**
  - Replaced `print()` statements with `logger` calls
  - Consistent formatting across all messages
  - Better progress indication
  - More informative error messages

- **GitHub Actions Workflow**
  - Enhanced with manual trigger options
  - Added verbose and dry-run input parameters
  - Better documentation with inline comments
  - Conditional flag handling in run command

### Fixed
- Environment variable validation now happens before any operations
- Health check catches configuration issues early
- Better error messages help identify root causes
- Retry logic handles transient network failures

### Documentation
- Added `NOTION_SYNC_ENHANCEMENTS.md` with feature summary
- Expanded `notion-sync.md` with troubleshooting section
- Added this `CHANGELOG.md` for tracking changes
- Improved inline code documentation
- Added comprehensive help text

### Infrastructure
- Enhanced GitHub Actions workflow
- Added manual trigger capabilities
- Improved error reporting in CI/CD

## [1.0.0] - 2025-11-07 (Previous Version)

### Initial Features
- Basic Notion to Hugo sync functionality
- Markdown conversion from Notion blocks
- Front matter generation
- File creation in content/posts directory
- Removal of unpublished posts
- GitHub Actions automation
- Hourly scheduled sync

---

## Migration Guide

### For Existing Users

The enhanced version is **fully backward compatible**. No changes are required to continue using the script as before.

### Optional Enhancements

To take advantage of new features:

1. **Enable Verbose Logging** (for troubleshooting):
   ```bash
   export VERBOSE=true
   python scripts/notion-sync.py
   # Or use flag:
   python scripts/notion-sync.py --verbose
   ```

2. **Test Safely with Dry-Run**:
   ```bash
   python scripts/notion-sync.py --dry-run
   ```

3. **Customize Sync Frequency**:
   - Edit `.github/workflows/notion-sync.yml`
   - Update the cron expression
   - See examples in workflow comments

4. **Use Manual Triggers**:
   - Go to Actions → "Sync Notion to Hugo"
   - Click "Run workflow"
   - Enable verbose or dry-run as needed

5. **Configure Retry Behavior**:
   ```bash
   export MAX_RETRIES=5
   export RETRY_DELAY=3
   ```

### Testing Recommendations

1. Run with dry-run first: `python scripts/notion-sync.py --dry-run --verbose`
2. Review the health check output
3. Verify statistics match expectations
4. Run actual sync and monitor results
5. Check GitHub Actions logs for any issues

---

## Support

For issues or questions:
- Review the troubleshooting guide in `notion-sync.md`
- Enable verbose logging for detailed diagnostics
- Use dry-run mode to test safely
- Check GitHub Actions logs for workflow issues
- Open an issue on GitHub with detailed information

## Credits

Enhancements developed in November 2025 to improve reliability, debuggability, and user experience of the Notion to Hugo sync system.
