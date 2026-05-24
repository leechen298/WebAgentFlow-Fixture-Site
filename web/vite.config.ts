import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';

// Dev proxy forwards /validation-api/* to the local fixture API.
// This avoids CORS in development and keeps the frontend calling a same-origin path.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const fixtureApiTarget = env.FIXTURE_API_TARGET || 'http://127.0.0.1:8002';

  return {
    plugins: [vue()],
    server: {
      host: '127.0.0.1',
      port: 5175,
      strictPort: true,
      proxy: {
        '/validation-api': {
          target: fixtureApiTarget,
          changeOrigin: true,
        },
      },
    },
  };
});
