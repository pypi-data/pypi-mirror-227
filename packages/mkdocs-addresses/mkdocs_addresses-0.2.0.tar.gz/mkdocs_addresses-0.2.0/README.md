
https://gitlab.com/frederic.zinelli/mkdocs-addresses/badges/main/coverage.svg

https://gitlab.com/frederic.zinelli/mkdocs-addresses/-/badges/release.svg


## Overview

### About

The [`mkdocs-addresses`][mkdocs-addresses-repo]{: target=_blank } plugin is a tool which offers:

* Abstraction of the concrete tree hierarchy of pages and the anchors within those, when writing a link, utilizing unique identifiers.
* Verification of numerous links and addresses to ensure the absence of dead links or images within the documentation (including verifications beyond mkdocs 1.5+ capabilities).
* Convenient helpers to facilitate the usage of those identifiers within the docs pages. For users working with compatible IDEs, this translates to the availability of auto-completion features.

Concretely, with the `mkdocs-addresses` plugin, one  gain the following benefits:


### Identifiers: separating structure from content {: .goals }

Instead of defining the addresses or anchors relative to the current document's path, the plugin relies on unique identifiers spanning the entire documentation. This approach eliminates various inconveniences:

- No need to adapt the address of a target based on the current page's location
- No need to recall the file where the identifier is defined (_assuming the autocompletion features are available and used_)
- No need to go check the target file for the exact header syntax to use, to ensure the validity of the link.

The plugin automatically reconstructs the appropriate addresses, based on where the relative location of the current and target files.

Additionally, one can still use the "old-fashioned" way of writing addresses, and the plugin will also [validate them](#overview-checks).


```markdown title="Defined in docs/main_page.md"
## Very important title with anchor and id {: #point-here }
```

```markdown title="Used in docs/subdir/other.md"
Click here to navigate to [this very important title](--point-here).


Or use the old fashion way...:
- With use_directory_urls = false: [go there](../main_page.html#point-here)
- With use_directory_urls = true:  [go there](../../main_page/#point-here)
```

!!! warning "One down side of the plugin?"

    Because writing addresses relative to the current location is a real pain when writing documentation with mkdocs, some alternatives have already been provided. For instance, it is possible to write the addresses using the location of the markdown filename instead of using the address in the final html document.

    This approach abstracts away the need to consider how addresses change depending on the value of the `use_directory_urls` configuration option.

    __This way of writing adresses is not compatible with the plugin...__

    ...But this syntax ___should not to be used anymore___, given that identifiers are available and offer finer features.


### Reduce dependencies on the files hierarchy {: .goals }

![moving documents without breaking links](!!move-deeper_png){: loading=lazy .w25 align=right }

by utilizing identifiers, the addresses become independent of the headers content and the files locations. Whether a substantial page is divided into smaller files or a directory name within the documentation's hierarchy is altered, addresses targeting identifier remain valid without any modification.


### Provide autocompletion helpers (IDE dependent) {: .goals }

<div style="display:grid; width:100%;">
    <div class="row-of-imgs w75">
        <div class="c1"><img src="!!auto-completion-point-here_png" /></div>
    </div>
</div>

Depending on the plugin's configuration , identifiers will be registered for various elements:

* Any tag in the final html document that contains an `id` attribute. When working in the original markdown document, this involves defining the ids with the [`attr_list`][attr_list]{: target=_blank } markdown extension (example: `## header {: #header-id }`)
* Any file within the `docs_dir` (<span class="gray">_recursively; includes images, .html files, .md files, ..._</span>).
* Links references, stored in a separate file (<span class="gray">_using `[id]: https://...`_</span>).
* Files that can be included in other documents (<span class="gray">_using `--<8--` / relies on [`pymdownx.snippets`][PyMdown-Extensions]{: target=_blank } python markdown extension_</span>).

When using a VSC-like IDE, code snippets will be built automatically for each identifier (sometimes in various ways), providing autocompletion features as shown in the picture above.

![alt](!!references-as-txt_png){: loading=lazy .w35 align=right } If VSC-like IDEs are not used, a `.txt` file is generated, which includes all currently defined identifiers. This offers an alternative method for finding what identifier to use, even though it might be somewhat cumbersome compared to using autocompletion.


### Tracking dead links or addresses in the docs {: .goals #overview-checks }

#### Verifications scope {: .goals2 }

During each "serve" operation, the plugin does extensive verifications to alert the user of potential issues. The plugin issues a warning...:

* ... if an invalid identifier is used somewhere,
* ... if an identifier or an address ("old-fashion way") points to a non-existent file.


<div style="display:grid; width:100%;">
    <div class="row-of-imgs w75">
        <div class="c1"><img src="!!errors-summary_png" /></div>
        <div class="c1 img-legend">One of the possible ways the plugin will signal problems...</div>
    </div>
</div>


#### How it is done {: .goals2 }

The plugin operates on the final html versions of the documentation files, interacting with every address and identifier found in the following tags:

* `<a href="...">`
* `<img src="..."/>`

This implies the following:

- Html code and markdown can be freely mixed within the original document, as the verifications are done on the final html.
- The plugin can also validate modifications done by other plugins.

Note that absolute and/or external links are not validated (refer to the [black_list_pattern](--mkdocs_addresses_config_plugin_PluginOptions_black_list_pattern) option to see how addresses are identified as external/absolute or not).


#### User handed configuration {: .goals2 }

In contrast to to mkdocs, the plugin offers multiple ways to fine-tune the verification process. The key point is it allows to mark some addresses or tags to exclude them from being checked. For example:

* List of [html ids, identifiers or addresses to ignore](--mkdocs_addresses_config_plugin_PluginOptions_ignored_identifiers_or_addresses)
* List of [html classes to ignore](--mkdocs_addresses_config_plugin_PluginOptions_ignored_classes)
* [Regex pattern of addresses to ignore](--mkdocs_addresses_config_plugin_PluginOptions_black_list_pattern)




## Dependencies

* Python 3.8+
* [mkdocs 1.4+][mkdocs]{: target=_blank }
* [BeautifulSoup 4+][BeautifulSoup]{: target=_blank }




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




### Recommended configuration {: #installation-config }

Here is a recommended configuration for the `mkdocs.yml` file. All the available options are detailed in the [configuration](--configuration/) section.


#### Markdown extensions {: .goals }

Since the plugin's primary benefit comes from using HTML attributes directly defined in the markdown documents, it's recommended to use the following [Python markdown extensions][PyMdown-Extensions]{: target=_blank }:

```yaml title="Recommended markdown extensions"
markdown_extensions:
    - attr_list
    - pymdownx.snippets:
        check_paths: true
        auto_append: ["path_to_external_links_definition.md"]
        #               ^ see plugin's external_link_file configuration
```

#### Plugin configuration {: .goals }

For the plugin itself:

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
So, if VSC isn't the utilized IDE, the [`use_vsc`](--mkdocs_addresses_config_plugin_PluginOptions_use_vsc) option should at the very least be modified.


#### When using mkdocs 1.5+ {: .goals #mkdocs-1-5-config }

 significant enhancement in address verification logic (which was notoriously lacking in earlier versions...) has been added in `mkdocs 1.5+`.

Because of this, the identifiers used in the [`mkdocs-addresses`][mkdocs-addresses-repo]{: target=_blank } plugin will trigger warnings with `1.5+`, necessitating the deactivation of those verifications. It is important to note the plugin takes on the responsibility of the equivalent verifications.

To deactivate `mkdocs 1.5+` verifications, apply the following to the `mkdocs.yml` file:

```yaml title="Deactivate the default verification logic for mkdocs 1.5+"
validation:
    absolute_links: ignore
    unrecognized_links: ignore
```

(_For the record, the development of the plugin began only a few weeks before the release of 1.5+ and was nearly complete when it did..._ x) )
{: style="font-size:85%" .gray }






## Links

* [Project repository (GitLab)][mkdocs-addresses-repo]{: target=_blank }
* [Online documentation][mkdocs-addresses-docs]{: target=_blank }
* [The project on PyPI][mkdocs-addresses on pyPI]{: target=_blank }
