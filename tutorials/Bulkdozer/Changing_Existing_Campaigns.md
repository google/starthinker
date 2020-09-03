
# Changing Existing Campaigns

## Introduction

This guide will show you how to make bulk changes to existing campaigns.
This is particularly useful if your team uses a planning tool that auto
generates the shell of the campaign (e.g. campaign, placement groups,
placements) and you need to create the lower levels of the campaign
(e.g. ads, ad placement assignments, ad creative assignment, creative
rotation, etc).

## Before you Begin

You will need a Bulkdozer feed, if you don't have one please refer to
the *Feed Setup* page. You will also need an existing campaign to
modify. We suggest that you do not use Bulkdozer to modify live
campaigns before you have familiarized yourself with the tool, so either
use an old campaign that is no longer alive, or create your own. If you
want to create a test campaign with Bulkdozer you can do so by following
the *Getting Started guide*.

## Reset your feed

Since we are going to start working on a new campaign, it is always a
good idea to reset your feed. You can do that through the menu Bulkdozer
-> Reset. Resetting may take up to a minute, wait for the "Running
script" message to disappear before moving to the next step.

![Bulkdozer_drop_down_menu](Images/bulkdozer_dropdown_menu.png)

## Identify items to load

We will use the Bulkdozer "Load Entities" functionality to load the
existing campaign. You can identify the items you'd like to load by
putting an existing ID in the respective column of your feed. In this
particular case we want to load an entire campaign, and therefore we
will put the campaign ID in the "Campaign ID" field of the Campaign tab:


![Bulkdozer_Campaign_tab](Images/Bulkdozer_Campaign_tab.png)

If you'd like to load multiple campaigns you can enter multiple IDs in
the Campaign ID column, one per row. If instead of loading the entire
campaign you would like to load a specific set of placement groups you
can simply enter the placement group IDs in the Placement Group ID
column of the Placement Group tab. The same can be done for placements
or even individual ads and creatives. Bulkdozer loads entities in
"cascade", if you specify a campaign ID the entire hierarchy under that
campaign will be loaded (placement groups, placements, ads, and
creatives). If you specify Placement IDs, only the hierarchy under those
placements will be loaded (ads and creatives but not placement groups
and campaigns).


## Load Entities

Now that the items we'd like to load have been identified, click the
menu Bulkdozer -> Load Entities.

Click yes in the confirmation popup, and notice how Bulkdozer moves to
the "Log" tab of the feed, there you can visualize the progress.

Once you see a final message saying: "Campaign manager data load
complete" the process is done.

Now you can browse the Bulkdozer tabs and see your campaign manager
data.

![Bulkdozer_load_entities](Images/bulkdozer_load_entities_menu.png)

## Create a new Ad

We will now create a new ad under this existing campaign, to do so, go
to the Ad tab and add a new row with the following:
- Campaign ID: Pick the campaign ID from the drop down.
- Ad Type: AD_SERVING_DEFAULT_AD
- Ad Priority: AD_PRIORITY_1
- Ad ID: ext_ad_1
- Ad Name: Bulkdozer new ad in existing campaign
- Ad Start Date: Same as the start date in the Campaign tab
- Ad End Date: Same as the end date in the Campaign tab

Fields not mentioned above can be left blank.


## Create Ad associations

We will tie the ad with the placement by going into the Ad Placement
Assignment tab and adding a new row:

- Placement ID: Pick a placement ID from the drop down.
- Ad ID: ext_ad_1

Next we will tie the ad with the creative by adding a new row to the Ad
Creative Assignment tab:

- Ad ID: ext_ad_1
- Creative ID: Pick a creative ID from the drop down.

Fields not mentioned above can be left blank.

## Push to Campaign Manager

Push to Campaign Manager by going to your StarThinker recipe and clicking the
"Run" button.Watch the Log tab as the process runs and your campaign is
trafficked. When you see the message "Bulkdozer traffic job ended" in the logs
the process is done. If you see any errors in the Log tab you can make
corrections to the appropriate tab and push again.


[Back to Documentation](Intsallation_and_User_guides.md) <br/>


<br/><br/>
---
&copy; 2019 Google Inc. - Apache License, Version 2.0

By using Bulkdozer the user agrees with the [Terms & Conditions](Terms_and_Conditions.md).
