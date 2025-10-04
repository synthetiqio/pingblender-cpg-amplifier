import path from 'path';
import react from '@vitejs/plugin-react';

export default {
    plugins: [
        react({
            babel: { plugins: [] },
        }),
    ],
    optimizeDeps: {
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
            input: 'index.html', 
            preserveEntrySignatures:'allow-extension', 
            output: {
                entryFileNames: 'assets/[name]-[hash].js',
                chunkFileNames: 'assets/[name]-[hash].js',
                assetFileNames: 'assets/[name]-[hash].[ext]',
                format: 'es', 
                dir: 'dist/standalone',
            },
        },
    },
    server:{
        port: 3000,
    },
};