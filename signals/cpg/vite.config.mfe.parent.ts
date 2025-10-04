import { defineConfig } from 'vite';

import defaultConfig from './config/vite.default';
import mfeConfig from './config/vite.mfe.parent';

const config = Object.assign({}, defaultConfig, mfeConfig)
export default defineConfig(
    config as any 
);