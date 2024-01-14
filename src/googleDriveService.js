import { google } from 'googleapis';
import dotenv from 'dotenv';

dotenv.config();

export class GoogleDriveService {
  driveClient;

  constructor() {
    this.driveClient = this.createDriveClient(
      process.env.GOOGLE_DRIVE_CLIENT_ID, 
      process.env.GOOGLE_DRIVE_CLIENT_SECRET, 
      process.env.GOOGLE_DRIVE_REDIRECT_URI, 
      process.env.GOOGLE_DRIVE_REFRESH_TOKEN
    );
  }

  createDriveClient(clientId, clientSecret, redirectUri, refreshToken) {
    const client = new google.auth.OAuth2(clientId, clientSecret, redirectUri);

    client.setCredentials({ refresh_token: refreshToken });

    return google.drive({
      version: 'v3',
      auth: client,
    });
  }


  async createFolder(folderName) {
    return this.driveClient.files.create({
      resource: {
        name: folderName,
        mimeType: 'application/vnd.google-apps.folder',
      },
      fields: 'id, name',
    });
  }

  async searchFolder(folderName) {
    return new Promise((resolve, reject) => {
      this.driveClient.files.list(
        {
          q: `mimeType='application/vnd.google-apps.folder' and name='${folderName}'`,
          fields: 'files(id, name)',
        },
        (err, res) => {
          if (err) {
            return reject(err);
          }

          return resolve(res.data.files ? res.data.files[0] : null);
        },
      );
    });
  }

  async saveFile(fileMetadata, media)
  {
    return this.driveClient.files.create({
      resource: fileMetadata,
      media: media,
      fields: 'id'
    });
  }
}