# Steam Survey over the years

Quite a lot has changed since Valve first released a Steam Hardware & Software Survey in 2004.
This document serves as a reference for what is known about the survey and its data.


## Contents
- [Survey information](#information)
- [Survey inconsistencies](#inconsistencies)

<a name="information"/>

## Survey information

__April 2004__

  - URL: http://www.steampowered.com/status/survey.html
  - Sample size and user quantities displayed
  - Data collection runs periodically (e.g. _This survey began on August 9th, 2005. This page last updated: 6:30pm PST (02:30 GMT), September 15 2005_)
  - Page was not updated monthly (e.g. December 2005 reporting results for September that year)
  - Some of the categories displayed change over the years

__December 2007__

  - Content and displayed information remains the same, just a cosmetic update
  - Change in the time frame of data collecting. Instead of doing a periodic sampling, they do a rolling update (e.g. _This survey began November 13th, 2007. Last updated: 3:53am PST (11:53 GMT), November 04 2008_)
  - Page updated randomly, sometimes multiple times per month or no update in a whole month (e.g. September 2007)

__December 2008__

  - URL: http://store.steampowered.com/hwsurvey
  - Major page overhaul with first charts, but sample size and quantity information not shown, and time-frame of the survey disappears
  - We have to assume that from this point forward the sampling is on a monthly basis, given the change in the description from _Every few months we run a hardware survey on Steam_ to _Each month, Steam collects data about [...]_, and the fact that time-frame information gets removed

__May 2010__

  - Addition of Mac information, with some charts and the possibility to filter categories by Windows, Mac or combined platforms
  - Old categories are moved to the __Windows only__ tab

__September 2010__

  - Addition of software information for Windows platform, although data is not updated on a monthly schedule (time froze at July 2010)

__December 2011__

  - Charts are rendered with Adobe Flash (you can still browse the content, although charts will not be displayed)

__April 2013__

  - The Windows software list disappears, after not having been ever updated

__February 2014__

  - Linux platform statistics filter is added

__June 2016__

  - Adobe Flash charts are no more

<a name="inconsistencies"/>

## Inconsistencies

__May 2012__

Official note:

> Why do many of the Steam Hardware Survey numbers seem to undergo a significant change in April 2012?
>
> There was a bug introduced into Steam's survey code several months ago that caused a bias toward older systems. Specifically, only systems that had run the survey prior to the introduction of the bug would be asked to run the survey again. This caused brand new systems to never run the survey. In March 2012, we caught the bug, causing the survey to be run on a large number of new computers, thus giving us a more accurate survey and causing some of the numbers to vary more than they normally would month-to-month. Some of the most interesting changes revealed by this correction were the increased OS share of Windows 7 (as Vista fell below XP), the rise of Intel as a graphics provider and the overall diversification of Steam worldwide (as seen in the increase of non-English language usage, particularly Russian).

__December 2012__

Windows Version category start presenting Linux distributions. This would remain the case until January 2014, when Linux platform was added to the survey. It was probably people running Steam on Linux through Wine.

__February 2018__

Official note:

> STEAM HARDWARE SURVEY FIX – 5/2/2018
>
> The latest Steam Hardware Survey incorporates a number of fixes that address over counting of cyber cafe customers that occurred during the prior seven months.
>
> Historically, the survey used a client-side method to ensure that systems were counted only once per year, in order to provide an accurate picture of the entire Steam user population. It turns out, however, that many cyber cafes manage their hardware in a way that was causing their customers to be over counted.
>
> Around August 2017, we started seeing larger-than-usual movement in certain stats, notably an increase in Windows 7 usage, an increase in quad-core CPU usage, as well as changes in CPU and GPU market share. This period also saw a large increase in the use of Simplified Chinese. All of these coincided with an increase in Steam usage in cyber cafes in Asia, whose customers were being over counted in the survey.
>
> It took us some time to root-cause the problem and deploy a fix, but we are confident that, as of April 2018, the Steam Hardware Survey is no longer over counting users.

__December 2022__

After an initial release of December 2022 hardware data that showed some odd discrepancies, Valve re-uploaded a revised dataset.

__March 2023__

Data from March 2023 (posted in April 2023 on the Steam website) saw unusual spikes in several areas (like growth in "Language: Simplified Chinese" or "Intel CPU" share among others). The reason was never officially addressed (but may be due to similar reasons as pointed in the 2018 official statement) nor was the data updated during the span April on the website. With the April data update in May, these outliers have seemed to be mitigated and numbers are closer to prior months.

__December 2024__

Data from December 2024 (uploaded January 2025) show large inconsistencies, where sums can add up to mathematically incorrect >100%. The data remained as is throughout January (i.e. was not revised by Valve). The following February upload (of January 2025 data) seems to be correct again, and was changed around February 19th 2025 by Valve to account for correct changes in relation to December (e.g. the first entry for Windows 11 from beginning of February changed from "-0.0150,0.5346" to "0.0034,0.5346" at that date). It is then possible to recalculate the values for December 2024 using the revised changes.

## Additional information

https://github.com/jdegene/steamHWsurvey

https://github.com/myagues/steam-hss-data

https://www.cluoma.com/?page=blog&id=51

