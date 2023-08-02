# Automatic TikTok YT channel

## TODOs
- [x] download
- [x] blurring
- [x] concatenating
- [x] extract verbose logging out of stdout 
- [ ] automate changing number in thumbnail
- [ ] add intro based on thumbnail at the start
- [ ] extract hard-coded parameters as option in the start script
- [ ] upload to yt

### Video generation
Create a `config.json file` inside service files modifiying `template.json` provided. 

Modify parameters inside of start script
```
./start.sh
```

### Key generation for upload (service account, no OAuth)
- Find the Service Account you created previously from the list of service accounts on the [page](https://console.cloud.google.com/iam-admin/serviceaccounts). It should have the custom name you provided during the creation process.
- Generate Credentials File: In the Actions column for the specific Service Account, click on the three-dot menu (⋮) and select "Create key."
- Choose Key Type: In the "Create key" dialog, select "JSON" as the key type and click the "Create" button.
- Download the JSON Key File: Once you click "Create," a JSON file containing the Service Account credentials will be generated and downloaded to your computer. This file contains the private key, client ID, client email, and other authentication information. Put it in `service_files/`.