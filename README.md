# Sorcery Solutions Backend

**_This repo is for demo purposes only. All secret keys and sensitive data are fake._**

The purpose of this repository is to host the backend API code for Sorcery Solutions!

The application uses the FastAPI Python framework to handle API calls from the frontend application and retrieve/store data in a MongoDB database.

Configuration for this application is handled mainly through environment variables as noted below.

| Name        | Description                                                           |
| ----------- | --------------------------------------------------------------------- |
| `MONGO_URI` | The full URI (including basic auth) for the desired MongoDB instance. |
| `MONGO_DB`  | The database to use within the MonogoDB instance.                     |
