# Data Structure Description

This project contains data structures that store information about cities along with their geographic coordinates.

## Data Structure

The data structure is represented as a dictionary (JSON file format), where the key is the city name, and the value
is a dictionary containing its geographical coordinates and distances to other cities in the data structure.

An example fragment of a data structure:

```json
{
    "Baden-Württemberg": {"lat": 48.7758, "lng": 9.1829, "distances": {}},
    "Bavaria": {"lat": 48.1351, "lng": 11.5820, "distances": {}},
    "Berlin": {"lat": 52.5200, "lng": 13.4050, "distances": {}},
}
```

## Adding New Data

To add new data to an existing structure, create a new key with the name of the new region and fill it in
appropriate data. Then, if necessary, distances to other cities should be completed manually or
use the appropriate distance calculation function.

## Comments
In the event of modification or extension of the data structure, care must be taken to maintain data consistency
appropriate documentation in the source file.
