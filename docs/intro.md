# Introduction

```{todo}
flesh this out.
```

```{note}
SOL is still a work in progress; and while much of the technology is in a usable state,
much of its feature-set is still being built. Consider SOL an 'unstable' library, for the time being.
```

Welcome to the SOL project! SOL is a full toolkit for working with USB using FPGAs, it provides a gateware library to implement USB in your own Torii based designs.


Some things you can use SOL for, currently:

- **Creating your own Low, Full or High speed USB device.** SOL provides a collection of Torii gateware that
  allows you to easily create USB devices in gateware, software, or a combination of the two.
- **Building USB functionality into a new or existing System-on-a-Chip (SoC).** SOL is capable of generating custom
  peripherals targeting the common Wishbone bus; allowing it to easily be integrated into SoC designs; and the library
  provides simple automation for developing simple SoC designs.

More detail on these features is covered in [the source](https://github.com/shrine-maiden-heavy-industries/sol), and in the remainder of this documentation.
