<!-- markdownlint-disable MD024 -->
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

## [0.8.0] - 2025-06-26

> [!IMPORTANT]
> This release is post to the split into [torii-usb] for the core gateware.
> For information on migrating please see the [migration guide](https://torii-usb.shmdn.link/migration.html)

This is a maintenance release, syncs the minimum [Torii] and [torii-usb] versions to `0.8.0` in preparation for
the Torii `1.0.0` release in the future.

### Changed

- Bumped [Torii] minimum version from `0.7.7` to `0.8.0`
- Bumped [torii-usb] minimum version from `0.7.1` to `0.8.0`

### Deprecated

- All of the core USB gateware has been deprecated in favor of [torii-usb]. The following modules have been deprecated.
  - `sol_usb.gateware.architecture.car.PHYResetController`
  - `sol_usb.gateware.interface.pipe`
  - `sol_usb.gateware.interface.ulpi`
  - `sol_usb.gateware.interface.utmi`
  - `sol_usb.gateware.interface.gateware_phy`
    - `sol_usb.gateware.interface.gateware_phy.phy`
    - `sol_usb.gateware.interface.gateware_phy.receiver`
    - `sol_usb.gateware.interface.gateware_phy.transmitter`
  - `sol_usb.gateware.interface.serdes_phy`
    - `sol_usb.gateware.interface.serdes_phy.ecp5`
    - `sol_usb.gateware.interface.serdes_phy.lfps`
    - `sol_usb.gateware.interface.serdes_phy.xc7_gtp`
    - `sol_usb.gateware.interface.serdes_phy.xc7_gtx`
    - `sol_usb.gateware.interface.serdes_phy.xc7`
  - `sol_usb.gateware.stream`
    - `sol_usb.gateware.stream.generator`
  - `sol_usb.gateware.usb`
    - `sol_usb.gateware.usb.devices`
      - `sol_usb.gateware.usb.devices.acm`
    - `sol_usb.gateware.usb.request`
      - `sol_usb.gateware.usb.request.windows`
        - `sol_usb.gateware.usb.request.windows.descriptorSet`
      - `sol_usb.gateware.usb.request.control`
      - `sol_usb.gateware.usb.request.interface`
      - `sol_usb.gateware.usb.request.standard`
    - `sol_usb.gateware.usb.usb2`
      - `sol_usb.gateware.usb.usb2.endpoints`
        - `sol_usb.gateware.usb.usb2.endpoints.isochronous`
        - `sol_usb.gateware.usb.usb2.endpoints.status`
        - `sol_usb.gateware.usb.usb2.endpoints.stream`
      - `sol_usb.gateware.usb.usb2.control`
      - `sol_usb.gateware.usb.usb2.descriptor`
      - `sol_usb.gateware.usb.usb2.deserializer`
      - `sol_usb.gateware.usb.usb2.device`
      - `sol_usb.gateware.usb.usb2.endpoint`
      - `sol_usb.gateware.usb.usb2.packet`
      - `sol_usb.gateware.usb.usb2.request`
      - `sol_usb.gateware.usb.usb2.reset`
      - `sol_usb.gateware.usb.usb2.transfer`
    - `sol_usb.gateware.usb.usb3`
      - `sol_usb.gateware.usb.usb3.application`
        - `sol_usb.gateware.usb.usb3.application.descriptor`
        - `sol_usb.gateware.usb.usb3.application.request`
      - `sol_usb.gateware.usb.usb3.endpoints`
        - `sol_usb.gateware.usb.usb3.endpoints.control`
        - `sol_usb.gateware.usb.usb3.endpoints.stream`
      - `sol_usb.gateware.usb.usb3.link`
        - `sol_usb.gateware.usb.usb3.link.command`
        - `sol_usb.gateware.usb.usb3.link.crc`
        - `sol_usb.gateware.usb.usb3.link.data`
        - `sol_usb.gateware.usb.usb3.link.header`
        - `sol_usb.gateware.usb.usb3.link.idle`
        - `sol_usb.gateware.usb.usb3.link.layer`
        - `sol_usb.gateware.usb.usb3.link.ltssm`
        - `sol_usb.gateware.usb.usb3.link.ordered_sets`
        - `sol_usb.gateware.usb.usb3.link.receiver`
        - `sol_usb.gateware.usb.usb3.link.timers`
        - `sol_usb.gateware.usb.usb3.link.transmitter`
      - `sol_usb.gateware.usb.usb3.physical`
        - `sol_usb.gateware.usb.usb3.physical.alignment`
        - `sol_usb.gateware.usb.usb3.physical.coding`
        - `sol_usb.gateware.usb.usb3.physical.ctc`
        - `sol_usb.gateware.usb.usb3.physical.layer`
        - `sol_usb.gateware.usb.usb3.physical.lpfs`
        - `sol_usb.gateware.usb.usb3.physical.power`
        - `sol_usb.gateware.usb.usb3.physical.scrambling`
      - `sol_usb.gateware.usb.usb3.protocol`
        - `sol_usb.gateware.usb.usb3.protocol.data`
        - `sol_usb.gateware.usb.usb3.protocol.endpoint`
        - `sol_usb.gateware.usb.usb3.protocol.layer`
        - `sol_usb.gateware.usb.usb3.protocol.link_management`
        - `sol_usb.gateware.usb.usb3.protocol.timestamp`
        - `sol_usb.gateware.usb.usb3.protocol.transaction`
      - `sol_usb.gateware.usb.usb3.request`
        - `sol_usb.gateware.usb.usb3.request.standard`
      - `sol_usb.gateware.usb.usb3.device`
    - `sol_usb.gateware.usb.device`
    - `sol_usb.gateware.usb.stream`
  - `sol_usb.gateware.utils`
    - `sol_usb.gateware.utils.bus`
    - `sol_usb.gateware.utils.cdc`
  - `sol_usb.gateware.memory`
  - `sol_usb.usb3`
  - `sol_usb.usb2`
  - `sol_usb.full_devices`

- The `sol_usb.gateware.stream` module has been absorbed into Torii's `torii.lib.streams.simple` module for `StreamInterface` and `StreamArbiter`.

## [0.5.0] - 2025-03-07

> [!IMPORTANT]
> This release is prior to the split into [torii-usb] for the core gateware.

### Changed

- The `gateware.usb.request.standard` is now restricted to only handle requests targeting the device.
- Bumped minimum [Torii] version from
  [0.7.1](https://github.com/shrine-maiden-heavy-industries/torii-hdl/releases/tag/v0.7.1)
  to [0.7.5](https://github.com/shrine-maiden-heavy-industries/torii-hdl/releases/tag/v0.7.5)
- Bumped minimum [pyvcd] version from
  [0.2.2](https://github.com/SanDisk-Open-Source/pyvcd/releases/tag/0.2.2)
  to [0.4.0](https://github.com/SanDisk-Open-Source/pyvcd/releases/tag/0.4.0)
- Bumped minimum [luminary] version from
  [0.0.5](https://github.com/shrine-maiden-heavy-industries/luminary/releases/tag/v0.0.5)
  to [0.0.6](https://github.com/shrine-maiden-heavy-industries/luminary/releases/tag/v0.0.6)

### Fixed

- Handful of little typing fixes.
- Fixed miss-using some of the IO resources, they happened to work, if only by accident.

## [0.4.1] - 2025-01-06

### Changed

- Bumped minimum [usb-construct]
  version from [0.2.0](https://github.com/shrine-maiden-heavy-industries/usb-construct/releases/tag/v0.2.0)
  to [0.2.1](https://github.com/shrine-maiden-heavy-industries/usb-construct/releases/tag/v0.2.1)
- Bumped minimum [Torii] version from
  [0.6.0](https://github.com/shrine-maiden-heavy-industries/torii-hdl/releases/tag/v0.6.0)
  to [0.7.1](https://github.com/shrine-maiden-heavy-industries/torii-hdl/releases/tag/v0.7.1)
- Converted a handful of Records to use the new "Structured Record" format in Torii.

### Fixed

- Fixed a deprecation warning from Python where we used a `~` on a boolean value.
- Fixed a typo in the `gateware.interface.ulpi` module (`s/UPLI/ULPI/g`)
- Fixed the `USBStandardRequestHandler` handling requests directed to things other than the device.
- Fixed a bug in the `GatewarePHY` where we used the Record value itself rather than the appropriate
  subsignal.

## [0.4.0] - 2024-07-10

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

## [0.3.0] - 2023-10-19

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

## [0.2.0] - 2022-12-18

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

[Unreleased]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.8.0...main
[0.8.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.5.0...v0.8.0
[0.5.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/shrine-maiden-heavy-industries/sol/compare/hw-r0.4...v0.1.0
[Torii]: https://github.com/shrine-maiden-heavy-industries/torii-hdl
[torii-usb]: https://github.com/shrine-maiden-heavy-industries/torii-usb
[usb-construct]: https://github.com/shrine-maiden-heavy-industries/usb-construct
[luminary]: https://github.com/shrine-maiden-heavy-industries/luminary
[pyvcd]: https://github.com/SanDisk-Open-Source/pyvcd
