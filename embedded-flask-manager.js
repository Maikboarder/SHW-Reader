const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

/**
 * Gestor del Servidor Flask Embebido
 * Solución definitiva para ejecutar el backend sin dependencias externas
 */
class EmbeddedFlaskServer {
    constructor(port = 5001) {
        this.port = port;
        this.process = null;
        this.isRunning = false;
        this.startupTimeout = 15000; // 15 segundos máximo
        this.checkInterval = 500; // Verificar cada 500ms
    }

    /**
     * Obtener la ruta del ejecutable embebido
     */
    getExecutablePath() {
        const serverName = process.platform === 'win32' ? 'flask_server.exe' : 'flask_server';
        const possiblePaths = [
            path.join(__dirname, 'dist', 'flask_server', serverName),
            path.join(__dirname, 'flask_server', serverName),
            path.join(process.cwd(), 'dist', 'flask_server', serverName),
            path.join(process.cwd(), 'flask_server', serverName)
        ];

        for (const testPath of possiblePaths) {
            if (fs.existsSync(testPath)) {
                console.log(`✅ Ejecutable encontrado: ${testPath}`);
                return testPath;
            }
        }

        console.log('❌ Ejecutable embebido no encontrado');
        return null;
    }

    /**
     * Verificar si el servidor está respondiendo
     */
    async checkServerHealth() {
        return new Promise((resolve) => {
            const req = http.get(`http://127.0.0.1:${this.port}`, (res) => {
                resolve(res.statusCode === 200);
            });
            
            req.on('error', () => {
                resolve(false);
            });
            
            req.setTimeout(2000, () => {
                req.destroy();
                resolve(false);
            });
        });
    }

    /**
     * Esperar hasta que el servidor esté listo
     */
    async waitForServer() {
        const startTime = Date.now();
        
        while (Date.now() - startTime < this.startupTimeout) {
            if (await this.checkServerHealth()) {
                this.isRunning = true;
                console.log('✅ Servidor embebido respondiendo correctamente');
                return true;
            }
            
            await new Promise(resolve => setTimeout(resolve, this.checkInterval));
        }
        
        console.log('❌ Timeout esperando servidor embebido');
        return false;
    }

    /**
     * Iniciar el servidor embebido
     */
    async start() {
        console.log('🚀 Iniciando servidor Flask embebido...');
        
        const executablePath = this.getExecutablePath();
        if (!executablePath) {
            throw new Error('Ejecutable embebido no encontrado');
        }

        // Verificar permisos de ejecución
        try {
            fs.accessSync(executablePath, fs.constants.X_OK);
        } catch (error) {
            console.log('🔧 Aplicando permisos de ejecución...');
            fs.chmodSync(executablePath, 0o755);
        }

        // Preparar argumentos
        const args = [
            '--port', this.port.toString(),
            '--templates', path.join(__dirname, 'templates'),
            '--static', path.join(__dirname, 'static')
        ];

        console.log(`Ejecutando: ${executablePath}`);
        console.log(`Argumentos: ${args.join(' ')}`);
        console.log(`Puerto: ${this.port}`);

        // Iniciar proceso
        this.process = spawn(executablePath, args, {
            cwd: path.dirname(executablePath),
            stdio: ['ignore', 'pipe', 'pipe'],
            detached: false,
            env: {
                ...process.env,
                PORT: this.port.toString(),
                PYTHONUNBUFFERED: '1'
            }
        });

        // Manejar salida del proceso
        if (this.process.stdout) {
            this.process.stdout.on('data', (data) => {
                console.log(`[Flask] ${data.toString().trim()}`);
            });
        }

        if (this.process.stderr) {
            this.process.stderr.on('data', (data) => {
                const message = data.toString().trim();
                if (message && !message.includes('WARNING')) {
                    console.error(`[Flask Error] ${message}`);
                }
            });
        }

        // Manejar eventos del proceso
        this.process.on('error', (error) => {
            console.error('❌ Error en proceso Flask:', error);
            this.isRunning = false;
            throw error;
        });

        this.process.on('exit', (code, signal) => {
            console.log(`[Flask] Proceso terminado - Código: ${code}, Señal: ${signal}`);
            this.isRunning = false;
        });

        // Esperar a que el servidor esté listo
        const success = await this.waitForServer();
        if (!success) {
            this.stop();
            throw new Error('El servidor embebido no pudo iniciarse en el tiempo esperado');
        }

        console.log('✅ Servidor Flask embebido iniciado exitosamente');
        return true;
    }

    /**
     * Detener el servidor
     */
    stop() {
        if (this.process && !this.process.killed) {
            console.log('🛑 Deteniendo servidor embebido...');
            this.process.kill('SIGTERM');
            
            // Forzar cierre si no responde
            setTimeout(() => {
                if (!this.process.killed) {
                    console.log('🔨 Forzando cierre del servidor...');
                    this.process.kill('SIGKILL');
                }
            }, 5000);
        }
        
        this.isRunning = false;
        this.process = null;
    }

    /**
     * Verificar si está ejecutándose
     */
    isServerRunning() {
        return this.isRunning && this.process && !this.process.killed;
    }
}

module.exports = { EmbeddedFlaskServer };
