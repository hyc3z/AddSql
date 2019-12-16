# AddSql
A tool for database testing.

This simple script can generate random data based on the Datatypes defined in [config.json](config.json). You can also set certain percentage of the data to (NULL).

Currently supported random datatypes:
TINYINT,SMALLINT,MEDIUMINT,INT,BIGINT,BIT,FLOAT,DOUBLE,VARCHAR.

*Note that using datatypes other than these may generate unpredictable data or SQL errors.

Personnally I used this script to generate random data (10^7 magnitude) to test SQL performance.
