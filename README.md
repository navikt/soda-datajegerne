# NADA soda
Naisjob example for periodically running [soda](https://github.com/sodadata/soda-core) checks against BigQuery tables and posting data quality errors to slack.

## Prerequisites
The script run by the dockerimage requires

- A [soda config](https://docs.soda.io/soda/connect-bigquery.html#connection-configuration) for connecting to one or several BigQuery datasource(s). See [config example](https://github.com/navikt/dp-nada-soda/blob/main/.local/soda-config/config.yaml) for configuring this for nais.
- One or several [soda check config(s)](https://docs.soda.io/soda-cl/soda-cl-overview.html) describing the checks you want to perform on the BigQuery tables. See [config folder](https://github.com/navikt/dp-nada-soda/tree/main/.local/soda-checks) for examples.
- The slack channel where you want to post data quality errors

All of the above requirements must be configured with environment variables as described in [Required environment variables](#required-environment-variables) below. 

>Note: The script requires that a datasource name matches the file name for the corresponding data quality tests, e.g. [./local/soda-checks/doc_demo.yaml](https://github.com/navikt/dp-nada-soda/tree/main/.local/soda-checks/doc_demo.yaml) without file extension must match the datasource name `doc_demo` in the [connection config](https://github.com/navikt/dp-nada-soda/blob/main/.local/soda-config/config.yaml#L1).

### Required environment variables
- `SODA_CONFIG`: Path to soda config file
- `SODA_CHECKS_FOLDER`: Path to folder containing soda check files for BigQuery datasets
- `SLACK_CHANNEL`: Desired slack channel for posting data quality errors

### Optional environment variables
- `NOTIFY_OK_SCAN_STATUS`: Set to "true" if you want enabel slack notifications for passing soda scans

## Deploy nais
To deploy to nais you can start from the [example naisjob yaml](https://github.com/navikt/dp-nada-soda/blob/main/.nais/naisjob.yaml) and modify this for your setup.

Change [the team and naisjob name](https://github.com/navikt/dp-nada-soda/blob/main/.nais/naisjob.yaml#L5-L7) and set [the slack channel](https://github.com/navikt/dp-nada-soda/blob/main/.nais/naisjob.yaml#L20-L21) you want your dataquality alerts to be posted to.

The soda config and the soda check files described in [Prerequisites](#prerequisites) needs to be mounted into the container environment on nais. In this example these configurations files are mounted from configmaps deployed together with the naisjob to the cluster. In the [.nais folder](https://github.com/navikt/dp-nada-soda/tree/main/.nais) there is an example on how to do this, i.e.

- The [soda config](https://github.com/navikt/dp-nada-soda/blob/main/.nais/soda-config.yaml) and [soda check files](https://github.com/navikt/dp-nada-soda/blob/main/.nais/soda-checks.yaml) are deployed as configmaps which are mounted into the naisjob pod as specified [here](https://github.com/navikt/dp-nada-soda/blob/main/.nais/naisjob.yaml#L27-L29).
- The files described in the configmaps are then mounted in the `/var/run/configmaps` folder of the container. You can then set the `SODA_CONFIG` and `SODA_CHECKS_FOLDER` environment variables described in [Required environment variables](#required-environment-variables) as specified [here](https://github.com/navikt/dp-nada-soda/blob/main/.nais/naisjob.yaml#L16-L19)

You will also need additional [project level iam roles](https://github.com/navikt/dp-nada-soda/blob/main/.nais/naisjob.yaml#L32-L46) for the naisjob service account in order to be allowed to perform the soda checks. Ensure that you set the correct project id for the roles.
