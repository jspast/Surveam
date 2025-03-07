# Surveam's data processing

Throughout the time, a couple of platforms and categories have been both added and removed of the Steam Survey.
Inside categories, changes were also made to better adapt the data to new hardware (e. g. VRAM went from being measured in MB to GB).
This means simply joining the data together creates a chaotic result.

To make the data more useful, Surveam does some processing, which is described below:

## 1. Category reassignment

Before the introduction of the Mac platform in 2010, every category was related to Windows.
At that point, they got segmented into Windows Only, Mac Only and Combined platforms, with Linux Only coming in 2014.
Surveam replicates the data from before 2010 to both Windows Only and Combined, with an exception to categories Valve kept to only one platform after 2010.

## 2. Item mapping

Some categories have had to adapt to new hardware over time, resulting in differences in the way data is shown and items overlapping.
For a few categories the amount of items have became practically impossible to deal with.
To counter that, Surveam group some items by mapping their names to something more useful.
Notably, Video Card Descriptions are mapped to their respective architecture name using the work done by [Devaniti](https://github.com/Devaniti/SteamHWSurveyGPUArchStats) (thanks!).

## 3. Category names clean-up

Originally, categories from specific platforms have the platform in their name as "\<category> (\<platform>)".
This is probably to make categories unique, regardless of platform.
Surveam strips that information because it is repetitive and also because Valve changed the way they name platforms over time: "PC" became "Windows" and "MAC" became "OSX"




