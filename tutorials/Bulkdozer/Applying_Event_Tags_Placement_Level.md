# Applying Event Tags at the Placement Level

## Introduction

This guide will show you how to apply event tags in bulk at the
placement level. Out of the box, Campaign Manager only allows event tags
to be applied at the advertiser, campaign, and ad level. Since the
publisher site is typically defined at the placement level applying
event tags there can be very helpful as usually there are publisher
specific event tags that need to be defined.


## Before you Begin

You will need a Bulkdozer feed, if you don't have one please refer to
the Feed Setup page. You will also need an existing campaign to
validate. We suggest that you do not use Bulkdozer to modify live
campaigns before you have familiarized yourself with the tool, so either
use an old campaign that is no longer live, or create your own. If you
want to create a test campaign with Bulkdozer you can do so by following
the Getting Started guide.


## Reset your feed

Since we are going to start working on a new campaign, it is always a
good idea to reset your feed. You can do that through the menu Bulkdozer
-> Reset. Resetting may take up to a minute, wait for the "Running
script" message to disappear before moving to the next step.

<img src="Images/bulkdozer_dropdown_menu.png" width="200">

## Load your Campaign

For details on how to load an existing campaign into the Bulkdozer feed
refer to the [Changing Existing Campaigns guide](Applying_Event_Tags_Placement_Level.md).

## Creating new Event Tags

Let's create 2 new event tags that we will then apply in bulk to all ads
under one of our placements.

Go to the Event Tag tab enter a new row:

- Advertiser ID: The same Advertiser ID as your campaign, refer to the
  Campaign tab.
- Campaign ID: Select your campaign ID from the dropdown.
- Event Tag ID: ext_event_tag_1
- Event Tag Name: Bulkdozer Event Tag 1
- Event Tag Status: ENABLED
- Enable By Default: FALSE Event Tag Type: IMPRESSION_IMAGE_EVENT_TAG
- Event Tag URL: Any valid url starting with https, e.g.
  https://www.google.com

Copy and paste the row that you've created above to create another event
tag, and change the following:

- Event Tag ID: ext_event_tag_2
- Event Tag Name: Bulkdozer Event Tag 2

Any fields not specified above can be left blank.


## Define an Event Tag Profile

The event tag profile is what we will use to apply a number of event
tags to all items under a placement, we need to define a profile with
the 2 event tags we've created in the previous step.

Go to the Event Tag Profile tab and enter a new row:

- Event Tag Profile: Any arbitrary name, we will use "My Event Tag
  Profile"
- Event Tag ID: ext_event_tag_1

Create another row for the second event tag:

- Event Tag Profile: Same as the one above: "My Event Tag Profile"
- Event nTag ID: ext_event_tag_2

Any fields not specified above can be left blank.


## Apply Event Tag Profile to a Placement
Go to the Placement tab and select a placement to apply the profile,
this should be a placement with ads under it, otherwise nothing will be
done.

On the Event Tag Profile field of the Placement tab for the row of
the placement you've selected, choose "My Event Tag Profile" from the
dropdown.

## Push to Campaign Manager

Push to Campaign Manager by going to your StarThinker recipe and clicking the
"Run" button.

Watch the Log tab as the process runs and your campaign is trafficked.
When you see the message "Bulkdozer traffic job ended" in the logs the
process is done.

If you see any errors in the Log tab you can make corrections to the
appropriate tab and push again.

Once the process completes successfully, go to your campaign in Campaign
manager and verify the event tags applied to the ads under the placement
you've configured with the profile.

<br/><br/>
---
&copy; 2019 Google Inc. - Apache License, Version 2.0

By using Bulkdozer the user agrees with the [Terms & Conditions](Terms_and_Conditions.md)


