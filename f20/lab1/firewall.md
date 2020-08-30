# Firewall Setup

1. Go to the Google Cloud Console at https://console.cloud.google.com/.  Then sign into your account.

<img src="img/7.png" width=600>

2. In the menu on the left, scroll down to "Networking"; under that, open
the "VPC network" menu and select "Firewall"

<img src="img/Firewall_part2_update.png" width=600>

3. Click the "CREATE FIREWALL RULE" button

<img src="img/Firewall_part3_update.png" width=600>

4. For the name and description, enter "cs320"

<img src="img/10.png" width=450>

5. Under Targets, chose "All instances in the network".  Set "Source filter" to "IP ranges" and "Source IP ranges" to "0.0.0.0/0".  Choose "Allow all" under "Protocols and ports".  Click "Create".

<img src="img/11.png" width=450>

6. You should see the new "cs320" rule in the table:

<img src="img/12.png" width=600>
