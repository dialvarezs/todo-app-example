import PrimeVue from 'primevue/config'
import type { App } from 'vue'
import Aura from '@primeuix/themes/aura'

// Import PrimeVue components
import Button from 'primevue/button'
import Card from 'primevue/card'
import Checkbox from 'primevue/checkbox'
import Chip from 'primevue/chip'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Menubar from 'primevue/menubar'
import Message from 'primevue/message'
import MultiSelect from 'primevue/multiselect'
import ProgressSpinner from 'primevue/progressspinner'
import Tag from 'primevue/tag'
import Textarea from 'primevue/textarea'

export default function setupPrimeVue(app: App) {
  app.use(PrimeVue, {
    theme: {
      preset: Aura,
      options: {
        darkModeSelector: 'my-dark',
      },
    },
  })

  // Register components globally
  app.component('PButton', Button)
  app.component('PCard', Card)
  app.component('PCheckbox', Checkbox)
  app.component('PChip', Chip)
  app.component('PDialog', Dialog)
  app.component('PInputText', InputText)
  app.component('PMenubar', Menubar)
  app.component('PMessage', Message)
  app.component('PMultiSelect', MultiSelect)
  app.component('PProgressSpinner', ProgressSpinner)
  app.component('PTag', Tag)
  app.component('PTextarea', Textarea)
}
