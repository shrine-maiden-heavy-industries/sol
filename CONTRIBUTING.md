# Contribution Guidelines

## Contributing

Contributions to SOL are released under the following licenses depending on the component:

* [CERN-OHL-P] - Hardware
* [BSD-3-Clause] - Software
* [CC-BY-4.0] - Documentation

Please note that SOL is released with a [Contributor Code of Conduct]. By participating in this project you agree to abide by its terms.

## Development and Testing

Prior working on SOL, ensure you understand have have followed the general [Installation] guide, when installing SOL make sure to add `[dev]` do the package name to ensure the needed development tools are installed along with SOL.

Alternatively, use `pip` to install [nox], like so:

```shell
$ pip install nox
```

General testing and linting of SOL is done with nox, as such there are some session names to know about:

* `test` - Run the test suite
* `lint` - Run the linter
* `typecheck` - Run the type-checker

Bye default these are configured to run one right after another when invoking `nox` with no arguments, to run a single check, you can run it with passing `-s <session>` to nox, like so:

```shell
$ nox -s lint
```

## Use of Generative AI

This project explicitly does not allow any contributions that were generated in whole or in-part by large language models (LLMs), chatbots, or image generation systems. This ban includes tools, including but not limited to Copilot, ChatGPT, Claude, DeepSeek, Stable Diffusion, DALL-E, Midjourney, or Devin AI.

This policy covers all parts of the project, including, but not limited to code, documentation, issues, artworks, comments, discussions, pull requests, and any other contributions to SOL, without exception.

> [!NOTE]
> It is also recommended to avoid any and all AI tools when asking questions about SOL,
> prefer the documentation when available, as well as things such as the discussion forum, or IRC channel.
> These tools often fabricate plausible sounding information that is entirely incorrect, or often subtly
> incorrect and pass it off with confidence, thus misleading.

[CERN-OHL-P]: ./LICENSE.hardware
[CC-BY-4.0]: ./LICENSE.docs
[BSD-3-Clause]: ./LICENSE.software
[Contributor Code of Conduct]: ./CODE_OF_CONDUCT.md
[Installation]: https://sol.shmdn.link/install.html
[nox]: https://nox.thea.codes/
