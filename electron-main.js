const { app, BrowserWindow, Menu, shell, dialog, ipcMain, session } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const { createFallbackServer } = require('./fallback-server');
const { EmbeddedFlaskServer } = require('./embedded-flask-manager');

// Variables globales
let mainWindow;
let flaskServer; // Usar el gestor del servidor embebido
let currentLanguage = 'es'; // Idioma actual
let menuTranslations = {}; // Cache de traducciones para el menú
const FLASK_PORT = process.env.FLASK_PORT || 5001;
const FLASK_URL = `http://127.0.0.1:${FLASK_PORT}`;

// Función para obtener el nombre de la aplicación
function getAppName() {
    try {
        const packageJson = require('./package.json');
        return packageJson.build?.productName || packageJson.productName || app.getName() || 'SHW Reader';
    } catch (error) {
        console.error('Error leyendo package.json:', error);
        return app.getName() || 'SHW Reader';
    }
}

// TODAS LAS FUNCIONES DE PYTHON EXTERNO REMOVIDAS
// La aplicación ahora SOLO usa el backend embebido o fallback Node.js

// Función para verificar si Flask embebido está disponible
function checkFlaskReady() {
    return new Promise((resolve) => {
        const checkServer = () => {
            console.log('Verificando si Flask está disponible...');
            const req = http.get(FLASK_URL, (res) => {
                console.log('Flask responde con status:', res.statusCode);
                if (res.statusCode === 200) {
                    resolve(true);
                } else {
                    setTimeout(checkServer, 1000);
                }
            });
            
            req.on('error', (err) => {
                console.log('Flask aún no está disponible, reintentando...');
                setTimeout(checkServer, 1000);
            });
        };
        
        checkServer();
    });
}

// Función para iniciar el servidor Flask (SOLUCIÓN DEFINITIVA)
async function startFlaskServer() {
    console.log('🚀 === INICIO SERVIDOR DEFINITIVO ===');
    
    // Intentar servidor embebido primero
    flaskServer = new EmbeddedFlaskServer(FLASK_PORT);
    
    try {
        await flaskServer.start();
        console.log('✅ Servidor embebido iniciado exitosamente');
        // Mostrar mensaje de éxito al usuario (solo en desarrollo)
        if (process.env.NODE_ENV === 'development') {
            setTimeout(() => {
                if (mainWindow) {
                    dialog.showMessageBox(mainWindow, {
                        type: 'info',
                        title: '🚀 SHW Reader listo',
                        message: 'Aplicación funcionando correctamente',
                        detail: `✅ Backend embebido activo

🔧 Funciones disponibles:
✅ Procesamiento completo de archivos SHW
✅ Exportación a CSV, Excel, Word y PDF
✅ Interfaz completa sin dependencias
✅ Funcionamiento inmediato

🎉 ¡Listo para usar!`,
                        buttons: ['Perfecto'],
                        defaultId: 0
                    });
                }
            }, 3000);
        }
        return Promise.resolve();
    } catch (error) {
        console.error('❌ Error con servidor embebido:', error.message);
        // NO intentar Python externo, solo fallback Node.js básico
        console.log('🔄 Usando servidor de emergencia...');
        try {
            await createFallbackServer(FLASK_PORT);
            console.log('✅ Servidor de emergencia iniciado');
            // Solo mostrar mensaje en caso de que realmente falle el embebido
            setTimeout(() => {
                if (mainWindow) {
                    dialog.showMessageBox(mainWindow, {
                        type: 'warning',
                        title: 'Modo básico activo',
                        message: 'SHW Reader funcionando con limitaciones',
                        detail: `⚠️ El backend completo no está disponible

🔧 Funciones disponibles:
✅ Interfaz de usuario
✅ Visualización básica de archivos SHW
❌ Exportación completa (CSV, Excel, Word, PDF)
❌ Procesamiento avanzado

💡 Reinicie la aplicación para reintentar el modo completo.`,
                        buttons: ['Continuar'],
                        defaultId: 0
                    });
                }
            }, 2000);
            return Promise.resolve();
        } catch (fallbackError) {
            console.error('❌ Error crítico - todos los servidores fallaron');
            if (mainWindow) {
                dialog.showErrorBox(
                    'Error crítico',
                    `No se pudo iniciar ningún servidor.\n\nErrores:\n- Servidor embebido: ${error.message}\n- Servidor emergencia: ${fallbackError.message}\n\nLa aplicación se cerrará.`
                );
            }
            app.quit();
            return Promise.reject(new Error('Fallo crítico de todos los servidores'));
        }
    }
}

// TODAS LAS FUNCIONES OBSOLETAS DE PYTHON REMOVIDAS
// La aplicación funciona SOLO con backend embebido + fallback Node.js

// Función para crear la ventana principal
async function createMainWindow() {
    // Limpiar caché automáticamente al iniciar
    console.log('Limpiando caché de Electron al iniciar...');
    await clearElectronCache();
    
    console.log('Creando ventana principal...');
    
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        minWidth: 800,
        minHeight: 600,
        fullscreen: true, // Arrancar en pantalla completa
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            webSecurity: true,
            preload: path.join(__dirname, 'preload.js')
        },
        icon: path.join(__dirname, 'assets', 'mac', 'SHW Reader.icns'),
        titleBarStyle: 'hiddenInset', // Estilo nativo de macOS
        show: false, // No mostrar hasta que esté listo
        backgroundColor: '#1a1a1a' // Color de fondo oscuro
    });

    console.log('Ventana creada, configurando eventos...');

    // Cargar la aplicación web
    console.log('Intentando cargar URL:', FLASK_URL);
    
    // Verificar que Flask esté disponible antes de cargar
    checkFlaskReady().then(() => {
        console.log('Flask está listo, cargando URL...');
        mainWindow.loadURL(FLASK_URL)
            .then(() => {
                console.log('URL cargada exitosamente');
            })
            .catch((err) => {
                console.error('Error al cargar URL:', err);
            });
    });

    // Mostrar la ventana cuando esté lista
    mainWindow.once('ready-to-show', () => {
        console.log('Ventana lista para mostrar');
        mainWindow.show();
        
        // Enfocar la ventana
        if (process.platform === 'darwin') {
            app.dock.show();
        }
    });

    // Manejar enlaces externos
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        shell.openExternal(url);
        return { action: 'deny' };
    });

    // Debug: Manejar errores de carga
    mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDescription, validatedURL) => {
        console.error('Error al cargar la página:', errorCode, errorDescription, validatedURL);
    });

    // Debug: Confirmar cuando la página se carga
    mainWindow.webContents.on('did-finish-load', () => {
        console.log('Página cargada completamente');
    });

    // Debug: Mostrar errores de consola del renderer
    mainWindow.webContents.on('console-message', (event, level, message, line, sourceId) => {
        console.log('Console del renderer:', message);
    });

    // Evento cuando se cierra la ventana
    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // Configurar el menú
    createMenu();
}

// Manejadores de IPC (Comunicación entre procesos)
function setupIpcHandlers() {
    // Manejador para abrir diálogo de archivo desde el frontend
    ipcMain.on('abrir-dialogo-archivo', async (event) => {
        console.log('Recibida solicitud para abrir diálogo de archivo');
        
        // Obtener la ventana que envió el evento
        const senderWindow = BrowserWindow.fromWebContents(event.sender);
        
        if (!senderWindow) {
            console.error('No se pudo obtener la ventana que envió el evento');
            return;
        }
        
        try {
            const { canceled, filePaths } = await dialog.showOpenDialog(senderWindow, {
                title: getMenuTranslation('menu.select_shw_file'),
                filters: [{ name: 'SHW', extensions: ['shw'] }],
                properties: ['openFile']
            });
            
            if (!canceled && filePaths && filePaths[0]) {
                console.log('Archivo seleccionado desde frontend:', filePaths[0]);
                senderWindow.webContents.send('abrir-archivo-shw', filePaths[0]);
            }
        } catch (error) {
            console.error('Error al abrir diálogo de archivo:', error);
        }
    });
}

// Función para crear el menú de la aplicación
function createMenu() {
    const template = [
        {
            label: getAppName(),
            submenu: [
                {
                    label: getMenuTranslation('menu.about'),
                    click: () => {
                        dialog.showMessageBox(mainWindow, {
                            type: 'info',
                            title: getMenuTranslation('menu.about'),
                            message: `${getAppName()} v1.0.1`,
                            detail: getMenuTranslation('about.description'),
                            icon: path.join(__dirname, 'assets', 'mac', 'SHW Reader', 'icon.iconset', 'icon_128x128.png')
                        });
                    }
                },
                { type: 'separator' },
                {
                    label: getMenuTranslation('menu.quit'),
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        app.quit();
                    }
                }
            ]
        },
        {
            label: getMenuTranslation('menu.file'),
            submenu: [
                {
                    label: getMenuTranslation('menu.open_file'),
                    accelerator: 'CmdOrCtrl+O',
                    click: async () => {
                        // Usa la ventana activa siempre
                        const { BrowserWindow } = require('electron');
                        const focusedWindow = BrowserWindow.getFocusedWindow() || mainWindow;
                        if (!focusedWindow) {
                            console.error('No hay ventana activa para enviar el archivo');
                            return;
                        }
                        const { canceled, filePaths } = await dialog.showOpenDialog(focusedWindow, {
                            title: getMenuTranslation('menu.select_shw_file'),
                            filters: [{ name: 'SHW', extensions: ['shw'] }],
                            properties: ['openFile']
                        });
                        if (!canceled && filePaths && filePaths[0]) {
                            console.log('Enviando a renderer:', filePaths[0]);
                            focusedWindow.webContents.send('abrir-archivo-shw', filePaths[0]);
                        }
                    }
                },
                { type: 'separator' },
                {
                    label: getMenuTranslation('menu.export_csv'),
                    accelerator: 'CmdOrCtrl+E',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof exportData === 'function') {
                                exportData('csv');
                            } else if (typeof exportCSV === 'function') {
                                exportCSV();
                            } else if (typeof exportToCSV === 'function') {
                                exportToCSV();
                            } else {
                                console.log('Función de exportar no encontrada');
                            }
                        `);
                    }
                },
                {
                    label: getMenuTranslation('menu.export_pdf'),
                    accelerator: 'CmdOrCtrl+Shift+P',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof exportData === 'function') {
                                exportData('pdf');
                            } else {
                                console.log('Función exportData no encontrada');
                            }
                        `);
                    }
                },
                { type: 'separator' },
                {
                    label: getMenuTranslation('menu.clear_table'),
                    accelerator: 'CmdOrCtrl+K',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof clearTable === 'function') {
                                clearTable();
                            } else {
                                // Fallback para limpiar la tabla manualmente
                                if (typeof tableData !== 'undefined') {
                                    tableData = [];
                                    if (typeof renderTable === 'function') renderTable();
                                    if (typeof updateStats === 'function') updateStats(0, 0);
                                }
                                if (typeof currentData !== 'undefined') {
                                    currentData = [];
                                    if (typeof populateTable === 'function') populateTable([]);
                                }
                                console.log('Tabla limpiada');
                            }
                        `);
                    }
                }
            ]
        },
        {
            label: getMenuTranslation('menu.edit'),
            submenu: [
                {
                    label: getMenuTranslation('menu.select_all'),
                    accelerator: 'CmdOrCtrl+A',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof selectAllRows === 'function' && !window.editingCell) {
                                selectAllRows();
                                updateSelectionStatus();
                            }
                        `);
                    }
                },
                { type: 'separator' },
                {
                    label: getMenuTranslation('menu.delete_selected'),
                    accelerator: 'Delete',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof deleteSelected === 'function') deleteSelected();
                        `);
                    }
                },
                {
                    label: getMenuTranslation('menu.delete_na_channels'),
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof deleteAllNA === 'function') deleteAllNA();
                        `);
                    }
                }
            ]
        },
        {
            label: getMenuTranslation('menu.theme'),
            submenu: [
                {
                    label: getMenuTranslation('menu.light_mode'),
                    type: 'radio',
                    checked: false,
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeTheme === 'function') {
                                changeTheme('light');
                            }
                        `);
                    }
                },
                {
                    label: getMenuTranslation('menu.dark_mode'),
                    type: 'radio', 
                    checked: true, // Por defecto modo oscuro
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeTheme === 'function') {
                                changeTheme('dark');
                            }
                        `);
                    }
                }
            ]
        },
        {
            label: getMenuTranslation('menu.window'),
            submenu: [
                {
                    label: getMenuTranslation('menu.minimize'),
                    accelerator: 'CmdOrCtrl+M',
                    role: 'minimize'
                },
                {
                    label: getMenuTranslation('menu.close'),
                    accelerator: 'CmdOrCtrl+W',
                    role: 'close'
                },
                { type: 'separator' },
                {
                    label: getMenuTranslation('menu.fullscreen'),
                    accelerator: 'Ctrl+Cmd+F',
                    role: 'togglefullscreen'
                }
            ]
        },
        {
            label: getMenuTranslation('menu.help'),
            submenu: [
                {
                    label: getMenuTranslation('menu.dev_tools'),
                    accelerator: 'F12',
                    click: () => {
                        mainWindow.webContents.toggleDevTools();
                    }
                },
                { type: 'separator' },
                {
                    label: getMenuTranslation('menu.reload'),
                    accelerator: 'CmdOrCtrl+R',
                    click: () => {
                        mainWindow.reload();
                    }
                },
                {
                    label: getMenuTranslation('menu.clear_cache_reload'),
                    accelerator: 'CmdOrCtrl+Shift+R',
                    click: async () => {
                        const success = await clearElectronCache();
                        if (success) {
                            // Mostrar mensaje de confirmación
                            dialog.showMessageBox(mainWindow, {
                                type: 'info',
                                title: getMenuTranslation('menu.cache_cleared'),
                                message: getMenuTranslation('menu.cache_cleared_message'),
                                detail: getMenuTranslation('menu.cache_cleared_detail'),
                                buttons: ['OK']
                            }).then(() => {
                                mainWindow.reload();
                            });
                        } else {
                            dialog.showErrorBox('Error', getMenuTranslation('menu.cache_error'));
                        }
                    }
                }
            ]
        },
        {
            label: getMenuTranslation('menu.language'),
            submenu: [
                {
                    label: 'Español',
                    type: 'radio',
                    checked: currentLanguage === 'es',
                    click: () => {
                        updateMenuLanguage('es');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('es');
                            }
                        `);
                    }
                },
                {
                    label: 'English',
                    type: 'radio',
                    checked: currentLanguage === 'en',
                    click: () => {
                        updateMenuLanguage('en');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('en');
                            }
                        `);
                    }
                },
                {
                    label: 'Français',
                    type: 'radio',
                    checked: currentLanguage === 'fr',
                    click: () => {
                        updateMenuLanguage('fr');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('fr');
                            }
                        `);
                    }
                },
                {
                    label: 'Deutsch',
                    type: 'radio',
                    checked: currentLanguage === 'de',
                    click: () => {
                        updateMenuLanguage('de');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('de');
                            }
                        `);
                    }
                },
                {
                    label: 'Italiano',
                    type: 'radio',
                    checked: currentLanguage === 'it',
                    click: () => {
                        updateMenuLanguage('it');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('it');
                            }
                        `);
                    }
                },
                {
                    label: 'Português',
                    type: 'radio',
                    checked: currentLanguage === 'pt',
                    click: () => {
                        updateMenuLanguage('pt');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('pt');
                            }
                        `);
                    }
                },
                {
                    label: 'Català',
                    type: 'radio',
                    checked: currentLanguage === 'ca',
                    click: () => {
                        updateMenuLanguage('ca');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('ca');
                            }
                        `);
                    }
                },
                {
                    label: 'Galego',
                    type: 'radio',
                    checked: currentLanguage === 'gl',
                    click: () => {
                        updateMenuLanguage('gl');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('gl');
                            }
                        `);
                    }
                },
                {
                    label: 'Euskera',
                    type: 'radio',
                    checked: currentLanguage === 'eu',
                    click: () => {
                        updateMenuLanguage('eu');
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof changeLanguage === 'function') {
                                changeLanguage('eu');
                            }
                        `);
                    }
                }
            ]
        },
    ];

    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
}

// Función para vaciar la caché de Electron
async function clearElectronCache() {
    try {
        const ses = session.defaultSession;
        
        // Limpiar caché de almacenamiento
        await ses.clearStorageData({
            storages: ['appcache', 'cookies', 'filesystem', 'indexdb', 'localstorage', 
                      'shadercache', 'websql', 'serviceworkers', 'cachestorage']
        });
        
        // Limpiar caché HTTP
        await ses.clearCache();
        
        console.log('Caché de Electron limpiada correctamente');
        return true;
    } catch (error) {
        console.error('Error al limpiar la caché:', error);
        return false;
    }
}

// Función para cargar traducciones del menú desde el backend
async function loadMenuTranslations(lang = 'es') {
    return new Promise((resolve) => {
        const url = `${FLASK_URL}/api/translations/${lang}`;
        console.log(`🔄 Cargando traducciones del menú para: ${lang}`);
        
        http.get(url, (res) => {
            let data = '';
            
            res.on('data', (chunk) => {
                data += chunk;
            });
            
            res.on('end', () => {
                try {
                    if (res.statusCode === 200) {
                        const translations = JSON.parse(data);
                        menuTranslations[lang] = translations;
                        console.log(`✅ Traducciones del menú cargadas para: ${lang}`);
                        resolve(translations);
                    } else {
                        console.warn(`⚠️ Error cargando traducciones para ${lang}: ${res.statusCode}`);
                        resolve(null);
                    }
                } catch (error) {
                    console.error(`❌ Error parseando traducciones para ${lang}:`, error);
                    resolve(null);
                }
            });
        }).on('error', (error) => {
            console.error(`❌ Error cargando traducciones del menú para ${lang}:`, error);
            resolve(null);
        });
    });
}

// Función para obtener traducción con fallback
function getMenuTranslation(key, lang = currentLanguage) {
    const translations = menuTranslations[lang];
    if (!translations) return key;
    
    const keys = key.split('.');
    let translation = translations;
    
    for (const k of keys) {
        if (translation && typeof translation === 'object' && k in translation) {
            translation = translation[k];
        } else {
            // Fallback al español si no se encuentra la traducción
            if (lang !== 'es' && menuTranslations['es']) {
                return getMenuTranslation(key, 'es');
            }
            return key;
        }
    }
    
    return typeof translation === 'string' ? translation : key;
}

// Función para actualizar el idioma del menú
async function updateMenuLanguage(newLang) {
    if (newLang === currentLanguage) return;
    
    console.log(`🔄 Actualizando idioma del menú de ${currentLanguage} a ${newLang}`);
    
    // Cargar traducciones si no están en caché
    if (!menuTranslations[newLang]) {
        await loadMenuTranslations(newLang);
    }
    
    currentLanguage = newLang;
    createMenu(); // Recrear el menú con las nuevas traducciones
    
    console.log(`✅ Menú actualizado al idioma: ${newLang}`);
}

// Eventos de la aplicación
app.whenReady().then(async () => {
    try {
        await startFlaskServer();
        
        // Cargar traducciones iniciales del menú
        await loadMenuTranslations('es');
        await loadMenuTranslations('en'); // Precargar inglés también
        
        // Configurar manejadores de IPC
        setupIpcHandlers();
        
        await createMainWindow();
    } catch (error) {
        console.error('Error al iniciar la aplicación:', error);
        dialog.showErrorBox('Error', 'No se pudo iniciar el servidor interno.');
        app.quit();
    }

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createMainWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    // Terminar el servidor Flask embebido
    if (flaskServer && flaskServer.isServerRunning()) {
        console.log('🛑 Cerrando servidor embebido...');
        flaskServer.stop();
    }
});

// Prevenir navegación no deseada
app.on('web-contents-created', (event, contents) => {
    contents.on('will-navigate', (navigationEvent, navigationUrl) => {
        const parsedUrl = new URL(navigationUrl);
        
        if (parsedUrl.origin !== FLASK_URL) {
            navigationEvent.preventDefault();
        }
    });
});

// ARCHIVO COMPLETAMENTE LIMPIO - SOLO BACKEND EMBEBIDO
