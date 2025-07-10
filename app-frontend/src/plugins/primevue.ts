import PrimeVue from 'primevue/config'
import type { App } from 'vue'
import Aura from '@primeuix/themes/aura'
import ConfirmationService from 'primevue/confirmationservice';


export default function setupPrimeVue(app: App) {
  app.use(PrimeVue, {
    theme: {
      preset: Aura,
      options: {
        darkModeSelector: 'my-dark',
      },
    },
  })
  app.use(ConfirmationService)
}
