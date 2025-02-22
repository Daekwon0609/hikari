# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

*This file was added at the beginning of the development of version 2.0.0.dev102, so nothing before that is documented.*

## [Unreleased]
### Added
 - Sticker methods to PartialGuild.
 - Helpful methods to Application object.
 - Missing Audit Log change keys.
 - Sticker Audit Log event types.
 - Retries for HTTP requests which fail with `5xx` status codes.

### Changed
 - Fix errors in rest sticker method docstrings.
 - Remove duplicate raise type in api and guilds docstrings.

### Fixed
 - Handling of interaction models passed to the webhook message endpoints as the "webhook" field.
