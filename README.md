# Introduction

This repository runs a CRON-job at 5-minute intervals that updates the "dashboard_statistics" collection in the `DEV` cluster. This database provides pre-computed values to allow the dashboard to load efficiently as well as provide almost-realtime updated values.

The script being run is in `main.py`. This script is hosted on an EC2 instance, and is run at 5-minute intervals using a CRON job.
