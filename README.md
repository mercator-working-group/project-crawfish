# Project Crawfish

Unified stack for crawler-based investigation of data sharing and pre-bid activity.

## Acknowledgements

The instrumentation of the crawl used to collect data for this project is accomplished using a [custom fork](https://github.com/mercator-working-group/OpenWPM) of the [OpenWPM](https://github.com/mozilla/OpenWPM) web privacy measurement framework, developed by Steven Englehardt at [Princeton University](https://webtap.princeton.edu/), currently hosted and maintained by [Mozilla](https://mozilla.org).

## Workflow

- Accept an arbitrary seed list of websites
- Determine one-depth a-tag linkage structure with a shallow preliminary crawl
- Perform a comprehensive crawl using OpenWPM to instrument Prebid.js-related JavaScript events at page visit
- Parse OpenWPM data into Pandas table
- Match against an arbitrary list
- Identify specific tracking pixels and potential fingerprinting attacks focusing on third-party loaded resources.
- Generate a report of third-party resources and tracking activity occurring per page (from originally provided seed-list).

## Usage instructions

### Preparations

Setup a Python 3 venv with the required modules:

```
./setup-python-venv.sh
```

Activate the Python 3 venv:

```
source venv/bin/activate
```

### Provide an input list

Save the initial list as `lists/pre-crawl-seed-list.csv`.

### Pre-crawl

Determines one-depth a-tag linkage structure with a shallow preliminary crawl:

```
python pre-crawl/main.py lists/pre-crawl-seed-list.csv lists/crawl-seed-list.csv
```

### OpenWPM crawl

To perform a comprehensive crawl using OpenWPM to instrument Prebid.js-related JavaScript events at page visit, follow the instructions in [./crawl/README.md](./crawl/README.md).

## Clean and analyze crawl results

```
jupyter notebook
```

After launching Jupyter, choose `Kernel -> Change Kernel -> project-crawfish` in the menu.

Navigate to `analysis/notebooks/cleanup.ipynb` to perform an initial dataset cleanup.

Use `analysis/notebooks/explore.ipynb` to explore the cleaned dataset.

## Developer notes

### Repository overview

This repo is structured as follows:
- `lists`: Contains csv files with base site lists for OpenWPM crawls
- `crawl`: Documentation and configuration to run local crawls on a Mac/Linux using Kubernetes.
- `crawl/OpenWPM`: Submodule of a Mercator-specific fork of OpenWPM that includes the Prebid.js-modified instrumentation
- `crawl/openwpm-crawler`: Submodule of the upstream mozilla/openwpm-crawler repo that includes general crawl deployment documentation and helper scripts
- `pre-crawl`: Python scripts to run the pre-crawl 
- `analysis`: Contains investigative methodology of OpenWPM result set and graphical exploration

### Submodules

To update the OpenWPM submodules to the latest commits in the remotely tracked branches:

```
git submodule update --init
git submodule update --remote
```
