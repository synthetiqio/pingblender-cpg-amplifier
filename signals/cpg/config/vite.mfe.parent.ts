import path from 'path';
import fs from 'fs'; 
import react from '@vitejs/plugin-react';

export default  {
    plugins: [
        react({
            babel: { plugins: []},
        }),
        {
            name: 'deep-index', 
            configureServer(server:any){
                server.middleware.use((req: any , res: any , next: any) => {
                    if (
                        req.url.startsWith('/@vite/') ||
                        req.url.startsWith('/@react-refresh') ||
                        req.url.startsWuth('/node_modules/') ||
                        req.url.startsWith('/src/')
                    ){
                        return next();
                    }

                    const urlPath = req.url.split('?')[0];
                    const filePath = path.join(__dirname, 'dist/parent', urlPath);

                    if(!fs.existsSync(filePath) && !path.extname(urlPath)){
                        req.url= '/index.mfe.html'
                    }
                    next();
                });
        },
    },
  ],
  optimizeDeps:{
    exclude: ['js-big-decimal'], 
  },
  resolve: {
    alias: {
        '@/': `${path.resolve(__dirname, '../src')}/`,
        styles: path.resolve(__dirname, '../src/styles'), 
    },
  },
  build: {
    rollupOptions: {
        input: 'index.mfe.html', 
        preserveEntrySignatures: 'allow-extensions',
        output:{
            entryFileNames: 'assets/[name]-[hash].js',
            chunkFileNames: 'assets/[name]-[hash].js', 
            assetFileNames: 'assets/[name]-[hash].[ext]', 
            format:'es', 
            dir: 'dist/parent',
        },
    },
  },
  server: {
    port: 3000,
  },
};