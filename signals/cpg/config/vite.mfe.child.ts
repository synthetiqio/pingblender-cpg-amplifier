import path from 'path';
import react from '@vitejs/plugin-react';
import vitePluginSingleSpa from 'vite-plugin-single-spa';
import pkg from '../package.json';

export default {
    plugins:[
        react({
            babel: { plugins: []},
        }),
    vitePluginSingleSpa({
        type:'mife',
        serverPort:3001, 
        spaEntryPoints:'cpg/single-spa-child.tsx', 
        projectId: pkg.name, 
        cssStategy: 'multiMife',
    }),
    ].filter(Boolean), 
    build: {
        rollupOptions:{
            input: 'cpg/single-spa-child.tsx',
            preserveEntrySignatures: 'strict',
            output:{
                entryFileNames: `${pkg.name}.js`, 
                chunkFileNames: undefined, 
                assetFileNames: undefined, 
                format: 'system',
                dir: 'dist/child',
            },


    },},
};