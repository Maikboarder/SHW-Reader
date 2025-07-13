// Servidor HTTP de fallback embebido en Node.js
// Se usa cuando Python/Flask no está disponible en Windows

const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

function createFallbackServer(port = 5001) {
    console.log('🔄 Iniciando servidor de fallback en Node.js...');
    
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
    app.use('/static', express.static(path.join(__dirname, 'static')));
    app.use(express.json());
    app.use(express.urlencoded({ extended: true }));
    
    // Configurar multer para uploads
    const uploadsDir = path.join(__dirname, 'uploads');
    if (!fs.existsSync(uploadsDir)) {
        fs.mkdirSync(uploadsDir, { recursive: true });
    }
    
    const storage = multer.diskStorage({
        destination: uploadsDir,
        filename: (req, file, cb) => {
            cb(null, Date.now() + '_' + file.originalname);
        }
    });
    const upload = multer({ 
        storage: storage,
        fileFilter: (req, file, cb) => {
            if (file.originalname.toLowerCase().endsWith('.shw')) {
                cb(null, true);
            } else {
                cb(new Error('Solo se permiten archivos .shw'));
            }
        }
    });
    
    // Ruta principal
    app.get('/', (req, res) => {
        const templatePath = path.join(__dirname, 'templates', 'index.html');
        res.sendFile(templatePath);
    });
    
    // Ruta de upload simplificada
    app.post('/upload', upload.single('file'), (req, res) => {
        console.log('📁 Recibida solicitud de upload en servidor de fallback');
        
        if (!req.file) {
            return res.json({ 
                success: false, 
                error: 'No se seleccionó archivo o el archivo no es válido (.shw requerido)' 
            });
        }
        
        console.log('📁 Archivo recibido:', req.file.originalname);
        
        // Procesamiento básico de archivo SHW (simplificado)
        // Nota: Sin Python, no podemos procesar realmente el archivo SHW
        const mockData = {
            success: true,
            message: 'Archivo cargado en modo básico',
            warning: 'Funcionalidad limitada: Instale Python para procesamiento completo de archivos SHW',
            channels: [
                { 
                    id: 1, 
                    name: 'Canal de ejemplo', 
                    frequency: '500.000', 
                    group: 'A', 
                    type: 'Wireless',
                    note: 'Datos de ejemplo - instale Python para datos reales'
                }
            ],
            total: 1,
            filename: req.file.originalname,
            fallback_mode: true
        };
        
        res.json(mockData);
    });
    
    // Ruta para obtener datos
    app.get('/data', (req, res) => {
        res.json({ 
            success: false, 
            error: 'Funcionalidad limitada - instale Python para funcionalidad completa',
            fallback_mode: true,
            help_url: 'https://python.org/downloads/'
        });
    });
    
    // Rutas de exportación básicas
    app.get('/export/:format', (req, res) => {
        res.json({ 
            success: false, 
            error: `Exportación a ${req.params.format} requiere Python - instale Python para funcionalidad completa`,
            fallback_mode: true,
            help_url: 'https://python.org/downloads/'
        });
    });
    
    // Ruta para traducciones (fallback)
    app.get('/api/translations/:lang', (req, res) => {
        const lang = req.params.lang || 'es';
        const translationPath = path.join(__dirname, 'translations', `${lang}.json`);
        
        if (fs.existsSync(translationPath)) {
            try {
                const translations = JSON.parse(fs.readFileSync(translationPath, 'utf8'));
                res.json(translations);
            } catch (error) {
                console.error('Error leyendo traducciones:', error);
                res.status(500).json({ error: 'Error cargando traducciones' });
            }
        } else {
            // Fallback a español si no se encuentra el idioma
            const fallbackPath = path.join(__dirname, 'translations', 'es.json');
            if (fs.existsSync(fallbackPath)) {
                try {
                    const translations = JSON.parse(fs.readFileSync(fallbackPath, 'utf8'));
                    res.json(translations);
                } catch (error) {
                    res.status(404).json({ error: 'Traducciones no encontradas' });
                }
            } else {
                res.status(404).json({ error: 'Traducciones no encontradas' });
            }
        }
    });
    
    // Manejo de errores
    app.use((error, req, res, next) => {
        console.error('Error en servidor de fallback:', error);
        res.status(500).json({ 
            success: false, 
            error: 'Error interno del servidor de fallback',
            fallback_mode: true 
        });
    });
    
    return new Promise((resolve, reject) => {
        const server = app.listen(port, '127.0.0.1', () => {
            console.log(`✅ Servidor de fallback ejecutándose en http://127.0.0.1:${port}`);
            console.log('⚠️ NOTA: Funcionalidad limitada - instale Python para funcionalidad completa');
            resolve(server);
        });
        
        server.on('error', (err) => {
            console.error('❌ Error iniciando servidor de fallback:', err);
            reject(err);
        });
    });
}

module.exports = { createFallbackServer };
