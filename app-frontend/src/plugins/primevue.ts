import PrimeVue from 'primevue/config'
import type { App } from 'vue'
import Aura from '@primeuix/themes/aura'

export default function setupPrimeVue(app: App) {
  app.use(PrimeVue, {
    theme: {
      preset: Aura,
      options: {
        darkModeSelector: 'my-dark',
      },
    },
  })
}
