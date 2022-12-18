# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Unreleased template stuff

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
-->


## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [0.2.0]

### Added

- Added preliminary type annotations.
- Added the `CHANGELOG.md`.

### Changed

- Changed the needed dependencies.
  - Removed all of the pure git url dependencies to allow us to be packaged for pypi.
- Altered the way the `lambdasoc` dependency was used for the `SimpleSoC` module.
- Changed the package name from `sol` to `sol_usb` to prevent pypi conflict.
- Changed the name of some documents to fall more in line with expected names.
- Changed from a poetry based build to purely using setup.py.
- Swapped out tox for nox.
- Replaced old Amaranth HDL deps with Torii.
- Replaced old python-usb-protocol with usb-construct.

### Removed

- Removed all of the 3rd party platform definitions except for the `LUNA` platforms.
- Removed the old `requirements.txt`
### Fixed

- Fixed a large chunk of code style and formatting.
- Fixed the documentation, it should now be more useful.

## [0.1.0]

No changelog is provided for this version as it is a hold-over / demarcation of the divergence from [LUNA](https://github.com/greatscottgadgets/luna/).

[Unreleased]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.2.0...main
[0.2.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/hw-r0.4...v0.1.0
