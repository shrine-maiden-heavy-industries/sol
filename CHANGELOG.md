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

## [0.3.0]

### Added

  - Added `handler_condition` to USB Requests
  - Added automatic construction of `StallOnlyRequestHandler`
  - Added pcapng support for capture applet
  - Added a `CONTRIBUTING.md` file
  - Added support for dynamic capture speed selection in analyzer
  - Added ability to request supported speeds from analyzer
  - Added ability to discard invalid/unknown data in the analyzer and restart the capture
  - Added an `rx_invalid` signal for `RequestHandlerInterface` to indicate invalid reception


### Changed

  - Updated from rich `12.6.0` to `13.0.0`
  - Improved Analyzer speed
  - Updated `SimpleSoC` to bring it up to date with `torii.soc` and `lambdasoc`
  - Updated torii minimum version to >=0.5.0
  - Moved the speed test device gateware into the applet gateware library

### Deprecated

### Removed

### Fixed

 - Various code formatting cleanups.
 - Fixed Analyzer capture engine overflow problem
 - Fixed UTMI/ULPI typo
 - Fixed Analyzer overflow handling
 - Fixed overflow handling on the primary analyzer FIFO
 - Fixed an issue with the return type of USBPacketID.byte()
 - Fixed signed/unsigned conversion error in USB2 descriptor handling
 - Implemented missing `.shape()` method for `ECP5DebugSPIBridge`
 - Fixed using `Pin` objects as if they were raw `Signals`
 - Fixed missing `**kwargs` in the `toolchain_prepare` method of `LUNAApolloPlatform`

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

[Unreleased]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.3.0...main
[0.3.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/hw-r0.4...v0.1.0
