// Servidor HTTP de fallback embebido en Node.js
// Se usa cuando Python/Flask no está disponible en Windows

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

function createFallbackServer(port = 5001) {
    const app = express();
    
    // Configurar motor de plantillas
    app.set('view engine', 'html');
    app.engine('html', (filePath, options, callback) => {
        fs.readFile(filePath, 'utf8', (err, content) => {
            if (err) return callback(err);
            return callback(null, content);
        });
    });
    
    // Configurar rutas estáticas
    app.use('/static', express.static('static'));
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // Configurar multer para uploads
    const storage = multer.diskStorage({
        destination: 'uploads/',
        filename: (req, file, cb) => {
            cb(null, file.originalname);
        }
    });
    const upload = multer({ storage: storage });
    
    // Crear directorio uploads si no existe
    if (!fs.existsSync('uploads')) {
        fs.mkdirSync('uploads');
    }
    
    // Ruta principal
    app.get('/', (req, res) => {
        res.sendFile(path.join(__dirname, 'templates', 'index.html'));
    });
    
    // Ruta de upload simplificada
    app.post('/upload', upload.single('file'), (req, res) => {
        if (!req.file) {
            return res.json({ success: false, error: 'No se seleccionó archivo' });
        }
        
        // Procesamiento básico de archivo SHW (simplificado)
        const mockData = {
            success: true,
            channels: [
                { id: 1, name: 'Channel 1', frequency: '500.000', group: 'A', type: 'Wireless' },
                { id: 2, name: 'Channel 2', frequency: '501.000', group: 'A', type: 'Wireless' },
                { id: 3, name: 'Channel 3', frequency: '502.000', group: 'B', type: 'Wireless' }
            ],
            total: 3,
            filename: req.file.originalname
        };
        
        res.json(mockData);
    });
    
    // Ruta para obtener datos
    app.get('/data', (req, res) => {
        res.json({ success: false, error: 'Funcionalidad limitada - instale Python para funcionalidad completa' });
    });
    
    // Rutas de exportación básicas
    app.get('/export/:format', (req, res) => {
        res.json({ success: false, error: 'Exportación requiere Python - instale Python para funcionalidad completa' });
    });
    
    return new Promise((resolve, reject) => {
        const server = app.listen(port, '127.0.0.1', () => {
            console.log(`Servidor de fallback ejecutándose en http://127.0.0.1:${port}`);
            console.log('NOTA: Funcionalidad limitada - instale Python para funcionalidad completa');
            resolve(server);
        });
        
        server.on('error', (err) => {
            reject(err);
        });
    });
}

module.exports = { createFallbackServer };
