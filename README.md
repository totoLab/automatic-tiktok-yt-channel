# Automatic TikTok YT channel

### Video generation
Modify parameters inside start.sh
```
./start.sh
```

### Key generation for upload (service account, no OAuth)
- Find the Service Account you created previously from the list of service accounts on the [page](https://console.cloud.google.com/iam-admin/serviceaccounts). It should have the custom name you provided during the creation process.
- Generate Credentials File: In the Actions column for the specific Service Account, click on the three-dot menu (⋮) and select "Create key."
- Choose Key Type: In the "Create key" dialog, select "JSON" as the key type and click the "Create" button.
- Download the JSON Key File: Once you click "Create," a JSON file containing the Service Account credentials will be generated and downloaded to your computer. This file contains the private key, client ID, client email, and other authentication information.