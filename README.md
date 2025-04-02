# SalahGraph
This project was created to help individuals visualize prayer times throughout the year. By inputting a location 
and date range, users can generate customized graphs to better understand daily prayer schedules.

### Why This Project Was Created
Muslims around the world follow specific prayer times that change daily based on the location and time of the year. 
This app provides a simple way to visualize these changes, helping individuals plan their routines throughout the 
year, and muslim organizations/mosques plan their prayer schedules throughout the year.

### Features
- Generate prayer time graphs for any date range.
- Customizable graph titles, styles, and labels.
- Support for various locations worldwide.
- Incorporates time changes due to DST.

### Future Improvements
- Integration with geolocation services for automatic location detection.
- Enhanced styling options for the graphs.

### Repo Diagram
```mermaid
flowchart TD
    A["User Input / Interface"]:::core
    B["Application Core (app.py)"]:::core
    C["Date Handler Module (date_handler.py)"]:::module
    D["Prayer Times API Module (prayer_times_api.py)"]:::module
    E["Graph Generation/Visualization Engine"]:::core
    F["External Dependencies / Libraries"]:::external

    A -->|"inputs"| B
    B -->|"processDateRange"| C
    B -->|"fetchPrayerTimes"| D
    C -->|"validatedDates"| B
    D -->|"prayerTimesData"| B
    B -->|"generateGraph"| E
    B -->|"utilizes"| F
    C -->|"usesLibs"| F
    D -->|"usesLibs"| F

    click A "https://github.com/manafasif/prayer_times/blob/master/app.py"
    click B "https://github.com/manafasif/prayer_times/blob/master/app.py"
    click E "https://github.com/manafasif/prayer_times/blob/master/app.py"
    click C "https://github.com/manafasif/prayer_times/blob/master/date_handler.py"
    click D "https://github.com/manafasif/prayer_times/blob/master/prayer_times_api.py"
    click F "https://github.com/manafasif/prayer_times/blob/master/requirements.txt"

    classDef core fill:#BBDEFB,stroke:#000,stroke-width:1px,color:#000;
    classDef module fill:#FFCDD2,stroke:#000,stroke-width:1px,color:#000;
    classDef external fill:#C8E6C9,stroke:#000,stroke-width:1px,color:#000;
```
