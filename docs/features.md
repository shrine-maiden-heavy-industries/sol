# Status & Support

The SOL library is a work in progress; but many of its features are usable enough for inclusion in your own designs.
More testing of our work -- and more feedback -- is always appreciated!

## Support for Device Mode

```{eval-rst}

+-------------------------------------+---------------------------------------+-----------------------------+
| Feature                                                                     | Status                      |
+=====================================+=======================================+=============================+
| **Control Transfers / Endpoints**   | CPU Interface                         | Working; Needs Testing      |
+-------------------------------------+---------------------------------------+-----------------------------+
| **Bulk Transfers / Endpoints**      | CPU Interface                         | Working; Needs Testing      |
+-------------------------------------+---------------------------------------+-----------------------------+
| **Interrupt Transfers / Endpoints** | CPU Interface                         | Working; Needs Testing      |
+-------------------------------------+---------------------------------------+-----------------------------+
|**Isochronous Transfers / Endpoints**| CPU Interface                         | Planned                     |
+-------------------------------------+---------------------------------------+-----------------------------+
| **USB Analysis**                    | Basic Analysis                        | Partially Implemented       |
+-------------------------------------+---------------------------------------+-----------------------------+
|                                     | Full Analysis                         | Planned                     |
+-------------------------------------+---------------------------------------+-----------------------------+


```

## Support for Host Mode

The SOL library currently does not provide any support for operating as a USB host; though the low-level USB
communications interfaces have been designed to allow for eventual host support. Host support is not currently
a priority, but contributions are welcome.
