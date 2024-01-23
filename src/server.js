import express from 'express';
import fs from 'fs';
import { GoogleDriveService } from './googleDriveService.js';
import multer from 'multer';

// const upload = multer({ dest: 'uploads/' });
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage: storage });

const app = express();
const port = process.env.PORT || 3000;

app.use(express.static('src'));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ limit: '50mb' }));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/src/index.html');
});

app.post('/upload', upload.single('image'), async (req, res) => {
  const googleDriveService = new GoogleDriveService();
  const now = new Date();
  const offsetMs = now.getTimezoneOffset() * 60 * 1000;
  const dateLocal = new Date(now.getTime() - offsetMs);
  const today = dateLocal.toISOString().slice(0, 19).replace(/-/g, "/").replace("T", " ");

  const folderName = `Folder${today}`;

  let folder = await googleDriveService.searchFolder(folderName);

  if (!folder) {
    folder = await googleDriveService.createFolder(folderName);
  }

  let folderId = folder.data ? folder.data.id : folder.id;

  const fileMetadata = {
    name: `snapshot${today}`,
    parents: [folderId],
  };

  const media = {
    mimeType: 'image/jpeg',
    body: fs.createReadStream(req.file.path)
  };

  try {
    const response = await googleDriveService.saveFile(fileMetadata, media);
    await fs.unlink(req.file.path, err => console.error(err));
    res.json({ status: response.status });
  } catch (error) {
    console.error('Error uploading image to Google Drive:', error);
    res.status(500).json({ error: 'Error uploading image to Google Drive' });
  }
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});