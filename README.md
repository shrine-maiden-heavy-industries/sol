# SOL: Torii USB Analyzer

> [!IMPORTANT]
> The core USB gateware functionality has been moved to [Torii-USB], please see the
> SOL to Torii-USB [migration guide] for information on migrating your code.

SOL is a fork of [Luna] USB platform and Analyzer, it was ported from [Amaranth] to [Torii] and split into the core USB gateware library [Torii-USB] and SOL which contains the hardware platforms, SoC toolkit, and USB analyzer frontend.

SOL itself is at the moment purely a fork of the software, however the original LUNA hardware has been preserved in the repository under the [`hardware`] subdirectory.

## Installation

Please see the [installation instructions] on the [online documentation].

## License

The SOL gateware is released under the [BSD-3-Clause], the full text of which can be found in the [`LICENSE.software`]file.

The SOL hardware is released under the [CERN-OHL-P], the full text of which can be found in the [`LICENSE.hardware`] file.

The SOL documentation is released under the [CC-BY-4.0], the full text of which can be found in the [`LICENSE.docs`] file.

[migration guide]: https://torii-usb.shmdn.link/migration.html
[Luna]: https://github.com/greatscottgadgets/luna/
[Amaranth]: https://github.com/amaranth-lang
[Torii]: https://github.com/shrine-maiden-heavy-industries/torii-hdl
[Torii-USB]: https://github.com/shrine-maiden-heavy-industries/torii-usb
[`hardware`]: ./hardware/
[installation instructions]: https://sol.shmdn.link/install.html
[online documentation]: https://sol.shmdn.link/
[BSD-3-Clause]: https://spdx.org/licenses/BSD-3-Clause.html
[`LICENSE.software`]: ./LICENSE.software
[CERN-OHL-P]: https://ohwr.org/cern_ohl_p_v2.txt
[`LICENSE.hardware`]: ./LICENSE.hardware
[CC-BY-4.0]: https://creativecommons.org/licenses/by/4.0/
[`LICENSE.docs`]: ./LICENSE.docs
