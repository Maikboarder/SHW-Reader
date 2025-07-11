const { app, BrowserWindow, Menu, shell, dialog, ipcMain, session } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const http = require('http');
const { createFallbackServer } = require('./fallback-server');

// Variables globales
let mainWindow;
let flaskProcess;
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

// Función para verificar si Python está disponible
function checkPython() {
    return new Promise((resolve) => {
        console.log('Verificando disponibilidad de Python...');
        
        // Primero intentar con python3
        const python3 = spawn('python3', ['--version'], { shell: true });
        python3.on('error', () => {
            console.log('python3 no encontrado, intentando con python...');
            
            // Intentar con 'python' si 'python3' no funciona
            const python = spawn('python', ['--version'], { shell: true });
            python.on('error', () => {
                console.log('❌ Python no encontrado en el sistema');
                resolve(false);
            });
            python.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ Python encontrado como "python"');
                    resolve('python');
                } else {
                    console.log('❌ Error ejecutando python');
                    resolve(false);
                }
            });
        });
        python3.on('close', (code) => {
            if (code === 0) {
                console.log('✅ Python encontrado como "python3"');
                resolve('python3');
            } else {
                console.log('❌ Error ejecutando python3');
                resolve(false);
            }
        });
    });
}

// Función para instalar Flask automáticamente
function installFlask(pythonCmd) {
    return new Promise((resolve, reject) => {
        console.log('🔄 Intentando instalar Flask y dependencias...');
        
        // Verificar si pip está disponible
        const pipCheck = spawn(pythonCmd, ['-m', 'pip', '--version'], { shell: true });
        
        pipCheck.on('error', (error) => {
            console.error('❌ pip no está disponible:', error);
            reject(new Error('pip no está disponible. Instale Python con pip incluido.'));
            return;
        });
        
        pipCheck.on('close', (code) => {
            if (code !== 0) {
                console.error('❌ pip no está disponible (código:', code, ')');
                reject(new Error('pip no está disponible. Reinstale Python con pip incluido.'));
                return;
            }
            
            console.log('✅ pip disponible, instalando Flask...');
            
            // Intentar instalar Flask con pip
            const pip = spawn(pythonCmd, ['-m', 'pip', 'install', '--user', 'flask', 'openpyxl', 'python-docx', 'reportlab'], { 
                shell: true,
                stdio: ['pipe', 'pipe', 'pipe']
            });
            
            let stdout = '';
            let stderr = '';
            
            if (pip.stdout) {
                pip.stdout.on('data', (data) => {
                    stdout += data.toString();
                    console.log('pip stdout:', data.toString().trim());
                });
            }
            
            if (pip.stderr) {
                pip.stderr.on('data', (data) => {
                    stderr += data.toString();
                    console.error('pip stderr:', data.toString().trim());
                });
            }
            
            pip.on('error', (error) => {
                console.error('❌ Error instalando Flask:', error);
                reject(new Error(`Error instalando Flask: ${error.message}`));
            });
            
            pip.on('close', (code) => {
                if (code === 0) {
                    console.log('✅ Flask instalado exitosamente');
                    resolve(true);
                } else {
                    console.error('❌ Error instalando Flask, código:', code);
                    console.error('❌ stderr:', stderr);
                    reject(new Error(`Error instalando Flask (código ${code}): ${stderr || 'Error desconocido'}`));
                }
            });
        });
    });
}

// Función para verificar si Flask está disponible
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

// Función para iniciar el servidor Flask
async function startFlaskServer() {
    console.log('🚀 Iniciando servidor Flask...');
    const pythonCmd = await checkPython();
    
    if (!pythonCmd) {
        console.log('⚠️ Python no encontrado, usando servidor de fallback...');
        
        try {
            // Usar servidor de fallback de Node.js
            await createFallbackServer(FLASK_PORT);
            console.log('✅ Servidor de fallback iniciado exitosamente');
            
            // Mostrar advertencia al usuario después de que la ventana esté lista
            setTimeout(() => {
                if (mainWindow) {
                    dialog.showMessageBox(mainWindow, {
                        type: 'warning',
                        title: 'Python no encontrado',
                        message: 'La aplicación está funcionando con funcionalidad limitada',
                        detail: `Python no está instalado en su sistema.

Para obtener todas las características de SHW Reader, necesita instalar Python:

1. Descargue Python desde python.org
2. Durante la instalación, marque "Add Python to PATH"
3. Reinicie SHW Reader

Actualmente puede visualizar archivos SHW con funciones básicas.`,
                        buttons: ['Entendido', 'Descargar Python', 'Ver Tutorial'],
                        defaultId: 0
                    }).then((result) => {
                        if (result.response === 1) {
                            shell.openExternal('https://www.python.org/downloads/');
                        } else if (result.response === 2) {
                            shell.openExternal('https://github.com/Maikboarder/SHW-Reader#installation');
                        }
                    });
                }
            }, 3000);
            
            return Promise.resolve();
        } catch (error) {
            console.error('❌ Error iniciando servidor de fallback:', error);
            if (mainWindow) {
                dialog.showErrorBox(
                    'Error crítico del servidor',
                    `No se pudo iniciar ningún servidor interno.

Error: ${error.message}

Por favor:
1. Cierre la aplicación
2. Instale Python desde python.org
3. Reinicie SHW Reader

Si el problema persiste, contacte al soporte.`
                );
            }
            app.quit();
            return Promise.reject(error);
        }
    }

    console.log(`✅ Python encontrado: ${pythonCmd}`);

    // Verificar si Flask está instalado
    return new Promise((resolve, reject) => {
        console.log('🔍 Verificando si Flask está instalado...');
        const flaskCheck = spawn(pythonCmd, ['-c', 'import flask; print("Flask OK")'], { shell: true });
        
        flaskCheck.on('error', (error) => {
            console.error('❌ Error al verificar Flask:', error);
            reject(`Error al verificar Flask: ${error.message}`);
        });
        
        flaskCheck.on('close', (code) => {
            if (code !== 0) {
                console.log('⚠️ Flask no está instalado, intentando instalación automática...');
                
                // Intentar instalar Flask automáticamente
                installFlask(pythonCmd).then(() => {
                    console.log('🔄 Verificando Flask después de la instalación...');
                    
                    // Verificar nuevamente si Flask está disponible después de la instalación
                    const flaskCheckPostInstall = spawn(pythonCmd, ['-c', 'import flask; print("Flask OK")'], { shell: true });
                    
                    flaskCheckPostInstall.on('error', (error) => {
                        console.error('❌ Error verificando Flask después de instalación:', error);
                        showPythonInstallationError();
                        reject(`Error verificando Flask después de instalación: ${error.message}`);
                    });
                    
                    flaskCheckPostInstall.on('close', (code) => {
                        if (code !== 0) {
                            console.error('❌ Flask sigue sin funcionar después de la instalación');
                            showPythonInstallationError();
                            return;
                        }
                        
                        console.log('✅ Flask verificado después de la instalación');
                        // Iniciar el servidor Flask después de la instalación exitosa
                        startFlaskServerInternal(pythonCmd, resolve, reject);
                    });
                }).catch((error) => {
                    console.error('❌ Error durante la instalación automática:', error);
                    showPythonInstallationError(error.message);
                    reject(error);
                });
                return;
            }
            
            console.log('✅ Flask ya está instalado');
            // Iniciar el servidor Flask directamente
            startFlaskServerInternal(pythonCmd, resolve, reject);
        });
    });
}

// Función para mostrar error de instalación de Python
function showPythonInstallationError(errorDetails = '') {
    setTimeout(() => {
        if (mainWindow) {
            dialog.showMessageBox(mainWindow, {
                type: 'error',
                title: 'Error instalando Python',
                message: 'No se pudo instalar Flask automáticamente',
                detail: `${errorDetails ? 'Error: ' + errorDetails + '\n\n' : ''}Para usar todas las funciones de SHW Reader, instale Python manualmente:

1. Descargue Python desde python.org
2. Durante la instalación, marque "Add Python to PATH"
3. Abra una terminal y ejecute: pip install flask openpyxl python-docx reportlab
4. Reinicie SHW Reader

Mientras tanto, puede usar la funcionalidad básica con el servidor de emergencia.`,
                buttons: ['Usar Modo Básico', 'Descargar Python', 'Ver Tutorial'],
                defaultId: 0
            }).then((result) => {
                if (result.response === 1) {
                    shell.openExternal('https://www.python.org/downloads/');
                } else if (result.response === 2) {
                    shell.openExternal('https://github.com/Maikboarder/SHW-Reader#installation');
                }
                
                // Si el usuario elige modo básico, iniciar servidor de fallback
                if (result.response === 0) {
                    createFallbackServer(FLASK_PORT).catch((error) => {
                        console.error('Error iniciando servidor de fallback:', error);
                        app.quit();
                    });
                }
            });
        }
    }, 1000);
}

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
                            message: `${getAppName()} v1.0.0`,
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
                    label: getMenuTranslation('menu.export_excel'),
                    accelerator: 'CmdOrCtrl+Shift+E',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof exportData === 'function') {
                                exportData('excel');
                            } else {
                                console.log('Función exportData no encontrada');
                            }
                        `);
                    }
                },
                {
                    label: getMenuTranslation('menu.export_word'),
                    accelerator: 'CmdOrCtrl+Shift+W',
                    click: () => {
                        mainWindow.webContents.executeJavaScript(`
                            if (typeof exportData === 'function') {
                                exportData('word');
                            } else {
                                console.log('Función exportData no encontrada');
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
    // Terminar el proceso de Flask
    if (flaskProcess) {
        flaskProcess.kill();
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

// Función interna para iniciar el servidor Flask (evita duplicación de código)
function startFlaskServerInternal(pythonCmd, resolve, reject) {
    // Determinar la ruta correcta del archivo Python
    let appPath;
    let workingDir;
    
    // Lista de posibles ubicaciones para el archivo Python
    const possiblePaths = [];
    
    if (app.isPackaged) {
        // En modo empaquetado, intentar varias ubicaciones posibles
        const resourcesPath = process.resourcesPath;
        const appResourcesPath = path.join(resourcesPath, 'app');
        
        possiblePaths.push(
            path.join(appResourcesPath, 'app_simple.py'),
            path.join(appResourcesPath, 'app_desktop.py'),
            path.join(resourcesPath, 'app_simple.py'),
            path.join(resourcesPath, 'app_desktop.py'),
            path.join(__dirname, 'app_simple.py'),
            path.join(__dirname, 'app_desktop.py'),
            path.join(process.cwd(), 'app_simple.py'),
            path.join(process.cwd(), 'app_desktop.py')
        );
    } else {
        // En modo desarrollo
        possiblePaths.push(
            path.join(__dirname, 'app_simple.py'),
            path.join(__dirname, 'app_desktop.py'),
            path.join(process.cwd(), 'app_simple.py'),
            path.join(process.cwd(), 'app_desktop.py')
        );
    }
    
    // Buscar el archivo en las ubicaciones posibles
    let foundPath = null;
    for (const testPath of possiblePaths) {
        console.log('Verificando ruta:', testPath);
        if (fs.existsSync(testPath)) {
            foundPath = testPath;
            console.log('Archivo encontrado en:', foundPath);
            break;
        }
    }
    
    if (!foundPath) {
        const error = new Error(`No se encontró archivo Python en ninguna de las ubicaciones: ${possiblePaths.join(', ')}`);
        console.error(error.message);
        dialog.showErrorBox(
            'Archivo no encontrado',
            `No se encontró el archivo Python del servidor.\nUbicaciones verificadas:\n${possiblePaths.join('\n')}`
        );
        reject(error);
        return;
    }
    
    appPath = foundPath;
    workingDir = path.dirname(appPath);
    
    console.log('Ejecutando:', appPath);
    console.log('Directorio de trabajo:', workingDir);
    console.log('Puerto Flask:', FLASK_PORT);
    console.log('Comando Python:', pythonCmd);
    console.log('Sistema operativo:', process.platform);
    
    // Configurar opciones específicas para Windows
    const spawnOptions = {
        cwd: workingDir,
        env: {
            ...process.env,
            PORT: FLASK_PORT.toString(),
            PYTHONUNBUFFERED: '1'
        }
    };
    
    // En Windows, añadir configuraciones específicas
    if (process.platform === 'win32') {
        spawnOptions.shell = true;
        spawnOptions.stdio = ['pipe', 'pipe', 'pipe'];
    } else {
        spawnOptions.stdio = 'inherit';
    }
    
    flaskProcess = spawn(pythonCmd, [appPath], spawnOptions);
    
    // Capturar salida para debugging en Windows
    if (process.platform === 'win32' && flaskProcess.stdout && flaskProcess.stderr) {
        flaskProcess.stdout.on('data', (data) => {
            console.log('Flask stdout:', data.toString());
        });
        
        flaskProcess.stderr.on('data', (data) => {
            console.error('Flask stderr:', data.toString());
        });
    }
    
    flaskProcess.on('error', (err) => {
        console.error('Error al iniciar Flask:', err);
        const errorMsg = `Error iniciando servidor Flask: ${err.message}`;
        
        // Mostrar error específico en Windows
        if (process.platform === 'win32') {
            dialog.showErrorBox(
                'Error del servidor interno',
                `No se pudo iniciar el servidor interno.\n\nDetalles técnicos:\n${errorMsg}\n\nAsegúrese de que Python esté instalado correctamente.`
            );
        }
        
        reject(err);
    });
    
    flaskProcess.on('close', (code) => {
        console.log('Flask process closed with code:', code);
        if (code !== 0) {
            const errorMsg = `El servidor Flask se cerró con código: ${code}`;
            console.error(errorMsg);
            
            if (process.platform === 'win32') {
                dialog.showErrorBox(
                    'Error del servidor interno',
                    `${errorMsg}\n\nPuede que falten dependencias de Python. La aplicación intentará instalarlas automáticamente en el próximo inicio.`
                );
            }
        }
    });
    
    // Esperar un momento para que el servidor se inicie
    setTimeout(() => {
        console.log('Flask debería estar listo ahora');
        resolve();
    }, 3000); // Aumentar a 3 segundos
}
