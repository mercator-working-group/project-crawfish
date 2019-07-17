# Project Crawfish

Unified stack for crawler-based investigation of data sharing and pre-bid activity.

## Developer notes

### Repository overview

This repo is structured as follows:
- `crawl/OpenWPM`: Submodule of a Mercator-specific fork of OpenWPM that includes the Prebid.js-modified instrumentation
- `crawl/openwpm-crawler`: Submodule of the upstream mozilla/openwpm-crawler repo that includes general crawl deployment documentation and helper scripts
- `pre-crawl`: Python scripts to run the pre-crawl 
- `analysis`: Notebooks used to analyze the resulting crawl datasets

### Submodules

To update the OpenWPM submodules to the latest commits in the remotely tracked branches:

```
git submodule update --init
git submodule update --remote
```
