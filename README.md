# perlmod\_install\_info Ansible module -- Determine from where to install Perl modules

Searches dnf, yum, apt, and/or cpanm to determine the best source from
which to install a Perl module. 

Prefers the OS repositories over cpanm. 

Specify module names as you would specify them with the `use` command
in a Perl script. 

Does not actually install modules. Instead, returns information about
where they can be installed from, which can be supplied to subsequent
tasks to do the actual installation. 

Note that this module will not fail by default if it cannot locate a
requested module. If you want that behavior, include a `failed_when`
which checks for `missing` being non-empty. 

## Requirements

- `apt-file` executable in search path on systems that use the apt
  package manager
- `dnf` or `yum` executable in search path on systems that use the
  dnf/yum package manager
- `cpanm` executable in search path if you want to be able to search
  for packages using cpanm

## Options

- **name [list of str]** -- Specify one or more Perl modules to search
  for.
- **try_apt [str, one of "auto", "true", "false"]** -- Specify whether
  to check for modules using the apt package manager. Defaults to true
  if apt-file executable is available.
- **try_cpanm [str, one of "auto", "true", "false"]** -- specify
  whether to check for modules using cpanm. Defaults to true if cpanm
  executable is available.
- **try_dnf [str, one of "auto", "true", "false"]** -- Specify whether
  to check for modules using the dnf package manager. Defaults to true
  if dnf executable is available.
- **try_installed [bool]** -- Specify whether to check if modules are
  already installed and not look elsewhere if they are.
- **try_yum [str, one of "auto", "true", "false"]** -- Specify whether
  to check for modules using the dnf package manager. Defaults to true
  if `try_dnf` is false and yum executable is available.
- **update [bool]** -- Specify whether to update package manager
  databases before searching.

## Return values

- **apt [list of str]** -- List of apt packages that should be
  installed to provide at least some of the required Perl modules
  - Returned when `try_apt` is true and requested modules were found
    in apt
  - Example: ['libnet-dns-perl']
- **cpanm [list of str]** -- List of modules that should be installed
  via CPAN
  - Returned when `try_cpanm` is true and requested modules were found
    in CPAN and nowhere else
  - Example: ['Net::DNS']
- **dnf [list of str]** -- List of dnf requirements that should be
  installed to provide at least some of the required Perl modules
  - Returned when `try_dnf` is true and requested modules were found
    in dnf
  - Example: ['perl(Net::DNS)']
- **installed [list of str]** -- List of modules that are already
  installed
  - Returned when `try_installed` is true and installed modules were
    found
  - Example: ['Net::DNS']
- **missing [list of str]** -- List of Perl modules that could not be
  found
  - Returned when there are missing modules
  - Example: ['No::Such::Module']
- **yum [list of str]** -- List of yum requirements that should be
  installed to provide at least some of the required Perl modules
  - Returned when `try_yum` is true and requested modules were found
    in yum
  - Example: ['perl(Net::DNS)']

## Examples

    # Search and fail if the package can't be found
    - name: Search for Net::DNS if it isn't already installed
      perlmod_install_info:
        name: Net::DNS
      register: perlmod_info
      failed_when: perlmod_info.missing is defined

    - name: Search for two modules, even if they're already installed
      perlmod_install_info:
        name:
        - URI
        - WWW::Mechanize
      try_installed: false
      register: perlmod_info

    - name: install dnf packages identified by perlmod_install_info
      dnf:
        name: "{{perlmod_info.dnf}}"
      when: perlmod_info.dnf is defined

    - name: install yum packages identified by perlmod_install_info
      yum:
        name: "{{perlmod_info.yum}}"
      when: perlmod_info.yum is defined

    - name: install yum packages identified by perlmod_install_info
      apt:
        name: "{{perlmod_info.apt}}"
      when: perlmod_info.apt is defined

    - name: install cpanm packages identified by perlmod_install_info
      cpanm:
        name: "{{item}}"
      with_items: "{{perlmod_info.cpanm}}"
      when: perlmod_info.cpanm is defined

## Author

- Jonathan Kamens <jik@kamens.us>

## Usage

Copy or symlink `plugins/modules/perlmod_install_info.py` into your
`library` directory.

## Copyright

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
