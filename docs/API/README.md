# API Request / Response Disclosures 
For the convenience of the user in both the API and the frontend consumers the API set is built around the concept of the 'Entity'. The Entity, is the proper noun person, object, place, or thing which is being considered within the data formats (unstructured, sql, csv, json, sqlite, postgresql, vector, graph) and will pivot around that for the permissible lifetime of that data's use.

## FILE Entity and Actions
The data which is presented to Graffiti's controls architecture will go through a series of initial transformations for assurances and quality management for the benefit of the system digest conformity. At times, the system may decide to store or use the data in some temporary format. Graffiti's data controls can be triggered by uploads and folder changes via FTP, or by use of the FILE Entity API set. 

Each of the ACTIONS affiliated with the file (upload, mapping, embedding, storing, updating, or delete) will happen on the same root endpoint and be stored in the representative steps. 

```bash 
    POST https://pingblender.local:8000/v1/API/file/{ACTION_NAME}
```

For the purpose of creating a useful pipeline for ETL and additional extended GenAI capabilities, the system can digest a series of lables which can be applied for differentiating comparative ideal TARGET files. These would be the data in the PERFECTED FORM to assign how the PRETZL system can handle and transform this data.

### File Upload 
Service Endpoint: [dev] - /file/upload/
Request: (form-data)

```
file(binary)
label: {assigned-string}
type: target
```