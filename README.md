# Influxdb-grafana-ext #

With this extensions you can use Influxdb and Grafana inside Loko ;)

## Important!

This project will mount volumes inside this path:
```bash
/var/opt/loko/influxdb-grafana-ext/
```
Before starting it the first time, run this command in your terminal:

```bash
sudo mkdir -p /var/opt/loko/influxdb-grafana-ext/grafana-data && sudo chmod 777 /var/opt/loko/influxdb-grafana-ext/grafana-data
```
