
![coverage badge](https://gitlab.com/frederic.zinelli/mkdocs-addresses/badges/main/pipeline.svg) ![coverage badge](https://gitlab.com/frederic.zinelli/mkdocs-addresses/badges/main/coverage.svg)


## Links

* [Full online documentation](http://frederic.zinelli.gitlab.io/mkdocs-addresses/)
* [The project on PyPI](https://pypi.org/project/mkdocs-addresses/)



## Dependencies

* Python 3.8+
* mkdocs 1.4+
* BeautifulSoup 4+


## Overview

### About

The [`mkdocs-addresses`](https://pypi.org/project/mkdocs-addresses/) is a plugin for `mkdocs` which offers:

* Abstraction of the concrete tree hierarchy of pages and the anchors within those, when writing a link, utilizing unique identifiers:

    Make a strong separation between logic and content, avoiding all addresses rewrite steps when some files are modified, split, merged or moved.

* Verification of numerous links and addresses to ensure the absence of dead links or images within the documentation (including verifications beyond mkdocs 1.5+ capabilities):

    Get a tool that warns you when something becomes wrong.

* Convenient helpers to facilitate the usage of those identifiers within the docs pages. For users working with compatible IDEs, this translates to the availability of auto-completion features:

    Don't lose time searching for the exact name of the anchor in the file that is... where is it again? Let the autocompletion tool find them for you.



### Identifiers: separating structure from content

Relying on the `attr_list` markdown extension, use identifiers instead of actual paths to point to specific anchors in the documentation:

```code
## Very important title with anchor and id {: #point-here }
```

```code
In another file: navigate to [this very important title](--point-here).
```


### Reduce dependencies on the files hierarchy

Identifiers still work after:
- Changing header content
- Renaming files
- Moving files

![move-deeper](docs/assets/move-deeper.png)


### Provide autocompletion helpers

_(Currently only available for VSC-like IDEs)_

![autocomplete](docs/assets/auto-completion-point-here.png)

* All snippets are automatically kept up to date while working on the documentation.
* They provide various markdown snippets, like:

    | Kind | Example of included snippet |
    |:-|:-|
    | Links | `[this is a link](--point-here)` |
    | Images | `![alt content](!!image_in_assets_firectory_jpg)` |
    | External references | `[mkdocs][mkdocs]` |
    | Code inclusions | `--<8-- "include/that_file.md"` |
    | ...|  |




### Tracking dead links or addresses in the docs

The plugin also explore the documentation and warns you if it finds invalid addresses or identifiers. This works for:

- Addresses in links
- Addresses of images
- Identifiers used by the plugin

![errors-example](docs/assets/errors-summary.png)


### User handed configuration

A lot of [options](http://frederic.zinelli.gitlab.io/mkdocs-addresses/configuration/) are available for the user to fine tune the plugin's behavior.





## Installation

Install the package on your machine (or in your project if you use a virtual env):

```
pip install mkdocs-addresses
```

Register the plugin in the `mkdocs.yml` file:

```yaml
plugins:
    - search            # To redeclare when plugins are added to mkdocs.yml
    - mkdocs-addresses
```

Configure the plugin (see below).




### Recommended `mkdocs.yml` configuration

See the [online documentation](http://frederic.zinelli.gitlab.io/mkdocs-addresses/#installation) for more details.

#### Markdown extensions

```yaml title="Recommended markdown extensions"
markdown_extensions:
    - attr_list             # To define the identifiers in the markdown content
    - pymdownx.snippets:    # If you need inclusions code snippets
        check_paths: true
        auto_append: ["path_to_external_links_definition.md"]
        #               ^ see plugin's external_link_file configuration
```

#### Plugin configuration

```yaml title="Register the plugin"
plugins:
    - search
    - mkdocs-addresses:
        - external_links_file: path_to_links_definition_if_any.md
        - inclusions:
            - location1_if_any
            - location2...
```

Note that the default configuration also implies the following choices:

```yaml
        - dump_snippets_file: .vscode/links.code-snippets
        - fail_fast: false
        - ignore_auto_headers: true
        - use_vsc: true
```
So, if VSC isn't the utilized IDE, the [`use_vsc`](http://frederic.zinelli.gitlab.io/mkdocs-addresses/configuration/#mkdocs_addresses.config_plugin.PluginOptions.use_vsc) option should at the very least be modified.


#### When using mkdocs 1.5+ {: .goals #mkdocs-1-5-config }

Significant enhancements in address verification logic (which was notoriously lacking in earlier versions...) have been added in `mkdocs 1.5+`.

But the plugin does more work, and the identifiers it is utilizing are generating warnings in the console. So you will have to deactivate mkdocs verification tools:

```yaml title="Deactivate the default verification logic for mkdocs 1.5+"
validation:
    absolute_links: ignore
    unrecognized_links: ignore
```


## Links

* [Full online documentation](http://frederic.zinelli.gitlab.io/mkdocs-addresses/)
* [The project on PyPI](https://pypi.org/project/mkdocs-addresses/)
