<!--
SPDX-FileCopyrightText: 2023 Phu Hung Nguyen <phuhnguyen@outlook.com>
SPDX-License-Identifier: CC-BY-SA-4.0
-->

# hugo-gettext

I18n with gettext for Hugo.

## Install

```bash
pip install hugo-gettext
```

### Custom functions
The path of the file should be passed as an argument to the command line with `-c` or `--customs` option,
or set in the config file with `customs` key.

The following functions are called to make `default_domain_name`, `excluded_keys`,
`report_address`, and `team_address` attributes of the `Config`:
- `get_default_domain_name`: will be called with `package` as an argument, returns `package` by default
- `get_custom_excluded_keys`: returns an empty set by default
- `get_pot_fields`: returns a dictionary of `'report_address'` and `'team_address'` keys

Two functions are called during the generation step:
- `load_lang_names`: returns an empty dictionary by default
- `convert_lang_code`: function to convert gettext language codes to Hugo language codes,
returns gettext language codes by default

### hg-stop shortcode to stop processing a content file