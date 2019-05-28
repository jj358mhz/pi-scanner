# CHANGELOG

# Version 2.3.0 - (27-May-2019)
UPDATED:
- Renamed `dbpurge.sh` file to `dbpurge`
- Refactored code to run on Debian Stretch

## Version 2.2.1 - (04-March-2019)
* ADDED: `stats.py` script to allow feed listener email notifications
* FIXED: Conditional check from `greater than or equal` to `greater than`
* UPDATED: Renamed `dbpurge` file to `dbpurge.sh` 

## Version 2.2.0 - (04-March-2019)
### ADDED
- New `alerts_slack.py` script to enable users to send Feed notifications to Slack 
- New `alerts_email.py` script to enable users to send Feed notifications to email

## Version 2.1.0 - (27-December-2018)
### ADDED
- Merry Christmas! `Dbpurge` now allows for maximum file archiving by setting the `DAYS=<value>` parameter in the `dbpurge.conf` file 

## Version 2.0.0 - (28-July-2017)
### UPDATED
- `Dbpurge` script refactored
- `Dbpurge.conf` file updated to match refactored Dbpurge script
### FIXED
- Various script comment typos

## Version 1.1.4 - (12-May-2017)
### UPDATED
- Dbpurge script now queries your Dropbox app folder and deletes oldest file
- Dropbox Uploader & Dbpurge script README instruction sections added
### FIXED
- Various script comment typos

## Version 1.1.3 - (08-Dec-2016)
### UPDATED
`darkice.cfg` Updated `server` URL domain

## Version 1.1.2 - (12-Sep-2016)
### FIXED
 - `USEDROPBOX = "yes"` parameter added

## Version 1.1.1 - (07-Sep-2016)
### FIXED
- Shebang syntax correction
- `Dbpurge` function corrected
### ADDED
- Changelog

## Version 1.1 - (08-Apr-2016)
### ADDED
- `Dbpurge` script

## Version 1.00 - (20-Mar-2014)
### NEW
- ScannerPi
