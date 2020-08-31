<a name="top_page"></a>

# Bulkdozer Lite

-   [Introduction](#introduction) <br/>
-   [Access](#access) <br/>
-   [Quickstart](#quickstart) <br/>
-   [Terms and Conditions](#terms_and_conditions) <br/>
-   [Support](#support) <br/>

<a name="introduction"></a>

## Introduction

Bulkdozer Lite is a simplified version of Bulkdozer that significantly
streamlines the deployment process of the tool. The main Bulkdozer version
requires a Google Cloud Project and an installation of the StarThinker tool to
perform updates in CM, Bulkdozer Lite on the other hand is fully self contained
in a Google Sheet, you simply make a copy of the sheet and you are ready to
start using it.

Bulkdozer Lite lacks some of the features of the main version of Bulkdozer, such
as event tag profiles, transcode configurations, asset upload, and advanced
display features to name a few. Also since Bulkdozer Lite runs on an environment
that is much more constrained than the main version, restrictions on memory and
execution time mean that only a couple of thousand items can be updated in a
single operation. Lite is also 20 to 30% slower than the main version depending
on the operation being performed.

Despite these restrictions, Bulkdozer Lite is a great way for users to start
experimenting with the tool, understand how it works, and gauge how it can
positively impact their organizations without commiting engineering resources or
requiring a Google Cloud Platform contract.

Note that Bulkdozer Lite is provided with the same terms and conditions as the
main Bulkdozer version, and by using any of its functionality you agree with
these terms, please see below.

[Back to top](#top_page)

<a name="access"></a>

## Access

Bulkdozer Lite is currently in alpha testing phase and we are only providing it
directly to selected partners and clients. Please contact your Google
representative for access and further information.

[Back to top](#top_page)

<a name="quickstart"></a>

## Quickstart

In this section we will explore the basic functionality of Bulkdozer Lite and
how to use it. This is not intended as a full re-write of the guides for the
main Bulkdozer version which are still broadly applicable to Lite. The goal here
is to show you how to operate Lite so you can go through the main version's
tutorials using this version.

[Back to top](#top_page)

### The Bulkdozer Lite Sidebar

The Bulkdzoer Lite sidebar is where you access all Bulkdozer Lite functionality.
To open the sidebar select the custom menu Bulkdozer -> Open.

Status: The "Status" text tells you what Bulkdozer is currently doing. "Ready"
means it is not executing any jobs and it is ready to process your next command.
When jobs are running, this status text changes to reflect the actions that are
being performed.

Clear Feed: This button will clear CM data from all tabs in the feed, preparing
it for the next activity, such as switching to work on a new campaign.

Load from CM: This button will load data from CM, which data to load is
identified by the IDs in the ID columns of the respective tabs. For instance, if
you would like to load all entities under a given Campaign, enter the Campaign
ID in the Campaign ID column of the Campaign tab and click Load from CM.

Push to CM: This button will push changes done to the feed back to CM.

[Back to top](#top_page)

### Clearing the Feed

Clearing the feed will erase any data from the tabs that contain CM data, it is
done through the Clear Feed button on the sidebar.

This is an essential step to ensure there is no left over data in the feed which
could cause inadverted changes to CM.

Always clear the feed whenever you start working on a new / different campaign,
and whenever the process of pushing or loading from CM is aborted either by the
user or by an unhandled error.

[Back to top](#top_page)

### Loading from CM

Bulkdozer Lite loads data from CM based on IDs you input in the respective tabs.
You can load entire campaigns or specific Placement Groups, Placements, and Ads.
Bulkdozer will load items in "cascade", e.g. if you decide to load campaigns
everything under the specified campaigns will be loaded. If you decide to load
Placements, everything under the placements will be loaded but not upstream
items such as campaigns and placement groups. This behavior is intended to allow
you to load only specific items you want to modify.

The first step is to clear the feed to ensure only the data you specify will be
loaded.

Next go to the tab that represents the top level entities you want to load. E.g.
if you want to load an entire campaign go to the Campaign Tab, if you want to
load specific placements go to the Placement tab.

In the selected tab enter the IDs of the items you'd like to loadd in the ID
column. For instance, if you are loading Campaigns, enter campaign IDs in the
Campaign ID column, if you are loading placement groups enter placement group
ids in the Placement Group column. You can also mix and match, for instance you
could load 1 entire campaign, 3 placement groups from another campaign, and 2
placements from yet another placement group by specifying the correct ids in the
correct tabs.

Finally open the sidebar and click "Load from CM". Monitor the Log tab until the
sidebar status changes to "Ready", which indicates the loading process is
complete and CM data is populated in the respective tabs.

[Back to top](#top_page)

### Pushing to CM

After building a campaign from scratch in the feed or loading and making
changes, you are ready to push back to CM.

Open the sidebar and click "Push to CM". Monitor the Log tab until the Status of
the sidebar changes to "Ready". This indicates the push is complete.

The Log tab will indicate any errors that happened during the push due to
misconfigurations, e.g. an end date that is earlier than a start date, a wrong
creative ID, an active ad that is not assigned to placements, incompatible
placement and creative types, etc. These errors can be fixed in the tabs and
another push executed.

If an unhandled error happens during the execution of a push such as quota
limits, API errors, memory usage exceeded etc., the Status field will not change
to "Ready", and the last entry in the Log tab will not be "Done", in this case
the feed is in an inconsistent state and you must reset the feed and start over
to avoid pushing misconfigured data causing potentially unintentional changes to
Campaign Manager.

[Back to top](#top_page)

# Terms and Conditions

By using Bulkdozer the user agrees with the
[Terms & Conditions](Terms_and_Conditions.md).

[Back to top](#top_page)

<a name="support"></a>

## Support

Bulkdozer is community supported, if you have any issues or questions please post a new issue [here](https://github.com/google/starthinker/issues)

Sign up for updates and announcements:
[Bulkdozer Announcements](https://groups.google.com/forum/#!forum/bulkdozer-announcements)

[Back to top](#top_page)
