import express from 'express';
import fs from 'fs';
import { GoogleDriveService } from './services/googleDriveService.js';
import multer from 'multer';

const upload = multer({ dest: 'uploads/' });

const app = express();
const port = 3000;

app.use(express.static('src'));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb' }));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/src/index.html');
});

app.post('/upload', upload.single('image'), async (req, res) => {
  const googleDriveService = new GoogleDriveService();
  const folderName = 'superwurdfolder';

  let folder = await googleDriveService.searchFolder(folderName);

  if (!folder) {
    folder = await googleDriveService.createFolder(folderName);
  }

  const fileMetadata = {
    name: 'image.png',
    parents: folder.id ? [folder.id] : [],
  };

  const media = {
    mimeType: 'image/png',
    body: fs.createReadStream(req.file.path)
  };

  try {
    const response = await googleDriveService.saveFile(fileMetadata, media);
    await fs.promises.unlink(req.file.path);
    res.json({ fileId: response });
  } catch (error) {
    console.error('Error uploading image to Google Drive:', error);
    res.status(500).json({ error: 'Error uploading image to Google Drive' });
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});