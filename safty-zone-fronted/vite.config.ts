import { defineConfig } from 'vite';
import { resolve } from 'path';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import svgLoader from 'vite-svg-loader';
import mkcert from 'vite-plugin-mkcert';

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueJsx(),
        svgLoader({ defaultImport: 'url' }),
        mkcert(),
    ],
    resolve: {
        alias: {
            '@': resolve('./src')
        }
    },
    server: {
        hmr: {
            overlay: false
        },
        host: '0.0.0.0',
        port: 9100,
        https: false
    },
    build: {
        minify: true,
        outDir: "build",
        chunkSizeWarningLimit: 256,
        sourcemap: true,
    },
    esbuild: {
        include: /\.[jt]sx$/,
        jsxInject: `import { Fragment, jsx } from '@/vue-shim'`,
        jsxFactory: 'jsx',
        jsxFragment: 'Fragment',
    },
    css: {
        charset: 'utf-8'
    }
})
