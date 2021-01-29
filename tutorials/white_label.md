# White Label

StarThinker is licensed under Apache License 2.0 allowing anyone to white label it. The process mainly requires
changing the logo and a few internal links. Here is how to do it...

1. Modify the domain name using the deployment script: [deploy_enterprise.md](deploy_enterprise.md).
1. Alter the logo storage bucket: [/starthinker_ui/ui/settings.py](/starthinker_ui/ui/settings.py#L45)
1. Alter the title: [starthinker_ui/templates/page.html](starthinker_ui/templates/page.html#L88)
1. Alter the copyright ( if modified ): [starthinker_ui/templates/footer.html](starthinker_ui/templates/footer.html)
1. Change the help email:
  - [starthinker_ui/templates/website/help.html](starthinker_ui/templates/website/help.html)
  - [starthinker_ui/templates/recipe/recipe_list.html](starthinker_ui/templates/website/help.html)
1. Edit the author and manager of each file in [/scripts/](/scripts/).
1. Update all generated assets using [/install/developer.sh#L320](/install/developer.sh#L320)

# Custom Package

Although StarThinker does accept contributions, sometimes a private package may be required.
Customize the [/install/developer.sh](/install/developer.sh#L321) script to re-package StarThinker.

# SAAS Billing Possibilities

The StarThinker UI and Workers typically run in their own Google Cloud Project seperate from the actual tasks within each recipe.
This approach naturally isolates any GCP costs incurred by recipes from the costs of operating StarThinker infrastrcture. The
setup allows several billing models for organizations wanting to package and sell services via StarThinker. Review the
[Cost Sheet](cost_sheet.md) for baseline StarThinker operating costs.

1. A per user access fee or tiered user fee.
1. A per recipe run fee, see [Cost Sheet](cost_sheet.md) for projected costs.
1. A recipe marketplace, with a cost associated with each recipe.
1. A mark-up based on cloud resources used. Requires setup of [GCP Subaccounts](https://cloud.google.com/billing/docs/concepts#subaccounts).
1. Software development fees for adding new recipes to the UI for non-technical people.
1. Offer access to the UI as a free enterprise add-on for clients to engage in wider partner services.
1. StarThinker remains internal to ad operations and the assets it produces such as dashboards, automation workflows, and  datasets are monetized.

---
&copy; 2019 Google LLC. - Apache License, Version 2.0
