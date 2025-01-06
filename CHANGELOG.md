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

## [0.4.1]

### Changed

- Bumped minimum [usb-construct](https://github.com/shrine-maiden-heavy-industries/usb-construct)
  version from [0.2.0](https://github.com/shrine-maiden-heavy-industries/usb-construct/releases/tag/v0.2.0)
  to [0.2.1](https://github.com/shrine-maiden-heavy-industries/usb-construct/releases/tag/v0.2.1)
- Bumped minimum [Torii](https://github.com/shrine-maiden-heavy-industries/torii-hdl) version from
  [0.6.0](https://github.com/shrine-maiden-heavy-industries/torii-hdl/releases/tag/v0.6.0)
  to [0.7.1](https://github.com/shrine-maiden-heavy-industries/torii-hdl/releases/tag/v0.7.1)
- Converted a handful of Records to use the new "Structured Record" format in Torii.

### Fixed

- Fixed a deprecation warning from Python where we used a `~` on a boolean value.
- Fixed a typo in the `gateware.interface.ulpi` module (`s/UPLI/ULPI/g`)
- Fixed the `USBStandardRequestHandler` handling requests directed to things other than the device.
- Fixed a bug in the `GatewarePHY` where we used the Record value itself rather than the appropriate
  subsignal.

## [0.4.0]

### Added

- Added test USB data from a real capture to fully test analyzer buffering.
- Added fast USB traffic test.
- Added type annotations for `SetupPacket`
- Added test for emptying the packet buffer once every `SOF` (Start Of Frame) in tandem with the data input simulation.
- Added missing dependency `luminary-fpga` for platform functionality.

### Changed

- Finished extracting tests into their own tree out of the implementation files.
- Updated minimum python version to match with Torii, it is now 3.10.
- Improved analyzer applet overrun handling on the secondary packet buffer side.

### Fixed

- Fixed warnings coming from the CDC tests.
- Fixed missing type annotations from the UTMI interface types.
- Fixed missing type annotations from the stream interface type.
- Fixed missing type annotations for the FIFOs and UTMI interfaces in the analyzer.
- Fixed an exception getting thrown in the analyzer when the platform doesn't support the `power_a_port` and `pass_through_vbus` signals.
- Fixed missing type annotations for the DUT and UTMI interfaces in the analyzer tests.
- Fixed missing type annotations in the test utilities and cleaned up the implementation of `SolGatewareTestCase.wait()`
- Fixed USB analyzer polling interval requested by the exfiltration endpoint.
- Fixed missing type annotations on the UTMI translator type in the ULPI interface.
- Fixed missing type annotations on the ULPI interface type.
- Fixed missing type annotations for `USBAnalyzerStackTest`.
- Fixed the check to see if the bus translator was in use or not.
- Fixed improper use of empty Torii `Case()` elements as stricter enforcement of using `Default()` has been implemented.
- Fixed UDEV rules.

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

[Unreleased]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.4.1...main
[0.4.1]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/hw-r0.4...v0.1.0
