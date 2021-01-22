# import-saxony-water-levels

Allows you to import data from Saxonys "Landeshochwasserzentrum" which includes water levels and precipitation data.

## Credentials

In order to gain access to the data you need to register with the "Landeshochwasserzentrum" and provide credentials to
this import. Simply edit the credentials.json file in the root directory and enter your username and password. 

## Outputs
* value (float): measured or predicted value
* unit (string): unit of value
* status (string): status message (unavailable for predictions)
* tendency (string): description of the water level tendency (only available for water levels, unavailable for all predictions)
* predicted_for (string, date in rfc3339): timestamp the value is predicted for (only available for predictions)
* meta (Object): 
  + station_id (string): station id
  + name (string): station name
  + lat (float): station latitude
  + long (float): station longitude
  + waterbody (string): name of the associated water body

## Configs
 * stations (List(string)): List of station ids to import. Ensure that the provided credentials have access to these stations. Default: []
 * type (string): station type. Either 'Pegel' (water levels) or 'Ombrometer' (precipitation). Default: 'Pegel'
 * series (string): series to import. This can be one of 'Ziel', 'Ziel-MW-1T', 'Vorh-Mitte-1H', 'Vorh-Unten-1H', 'Vorh-Oben-1H' for 'Pegel' stations or 'Ziel', 'Ziel-Sum-1T-7-7' for 'Ombrometer' stations. Not all stations support all series. Default: 'Ziel'
 * phys_unit (string): Physical unit to import. This can be 'W' or 'Q' for 'Pegel' stations and has to be 'P' for 'Ombrometer' stations.
 * historic (bool): If true, all available historic data will be imported. Default: false

---

This tool uses data provided by Saxonys Landeshochwasserzentrum. More information available [here](https://www.umwelt.sachsen.de/umwelt/infosysteme/lhwz/index.html).
