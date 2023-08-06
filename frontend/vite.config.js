import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';
import path from 'path'; // Importeer de 'path'-module om paden op te lossen

export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // Gebruik 'path.resolve' om het absolute pad naar de 'src'-map te krijgen
    }
  }
});
