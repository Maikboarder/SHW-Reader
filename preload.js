const { contextBridge, ipcRenderer } = require('electron');

console.log('PRELOAD CARGADO'); // Esto debe verse en la consola de Electron

contextBridge.exposeInMainWorld('electronAPI', {
    onAbrirArchivoSHW: (callback) => {
        ipcRenderer.on('abrir-archivo-shw', (event, filePath) => {
            console.log('Evento recibido en preload:', filePath);
            callback(filePath);
        });
    },
    abrirDialogoArchivo: () => {
        console.log('Solicitando apertura de diálogo de archivo desde frontend');
        ipcRenderer.send('abrir-dialogo-archivo');
    }
});
