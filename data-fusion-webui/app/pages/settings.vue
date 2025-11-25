<template>
  <div>
    <UiContentCard title="Settings" subtitle="Configure application preferences">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Settings Navigation -->
        <div class="lg:col-span-1">
          <nav class="space-y-1">
            <button
              v-for="section in settingsSections"
              :key="section.key"
              @click="activeSection = section.key"
              class="w-full text-left px-4 py-2 text-sm font-medium rounded-md transition-colors"
              :class="activeSection === section.key
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
            >
              <UIcon :name="section.icon" class="w-4 h-4 inline mr-2" />
              {{ section.label }}
            </button>
          </nav>
        </div>

        <!-- Settings Content -->
        <div class="lg:col-span-2">
          <!-- General Settings -->
          <div v-if="activeSection === 'general'" class="space-y-6">
            <UFormGroup label="Application Name" name="appName">
              <UInput v-model="settings.appName" placeholder="Data Fusion Hub" />
            </UFormGroup>
            <UFormGroup label="Default Page Size" name="pageSize">
              <USelect v-model="settings.pageSize" :options="[10, 25, 50, 100]" />
            </UFormGroup>
            <UFormGroup label="Auto-refresh Interval (seconds)" name="refreshInterval">
              <UInput v-model="settings.refreshInterval" type="number" min="0" />
            </UFormGroup>
            <UFormGroup label="Theme" name="theme">
              <USelect v-model="settings.theme" :options="['Light', 'Dark']" disabled />
              <template #help>
                <span class="text-xs text-gray-500">Dark theme coming soon</span>
              </template>
            </UFormGroup>
          </div>

          <!-- Data Sources Settings -->
          <div v-if="activeSection === 'data-sources'" class="space-y-6">
            <UFormGroup label="Default Connection Timeout (seconds)" name="connectionTimeout">
              <UInput v-model="settings.connectionTimeout" type="number" min="1" />
            </UFormGroup>
            <UFormGroup label="Max Retry Attempts" name="maxRetries">
              <UInput v-model="settings.maxRetries" type="number" min="0" />
            </UFormGroup>
            <UFormGroup label="Enable SSL Verification" name="sslVerification">
              <UToggle v-model="settings.sslVerification" />
            </UFormGroup>
            <UFormGroup label="Data Retention Period (days)" name="retentionPeriod">
              <UInput v-model="settings.retentionPeriod" type="number" min="1" />
            </UFormGroup>
          </div>

          <!-- Notifications Settings -->
          <div v-if="activeSection === 'notifications'" class="space-y-6">
            <UFormGroup label="Email Notifications" name="emailNotifications">
              <UToggle v-model="settings.emailNotifications" />
            </UFormGroup>
            <UFormGroup label="Slack Webhook URL" name="slackWebhook">
              <UInput v-model="settings.slackWebhook" placeholder="https://hooks.slack.com/..." />
            </UFormGroup>
            <UFormGroup label="Notify on Pipeline Failure" name="notifyOnFailure">
              <UToggle v-model="settings.notifyOnFailure" />
            </UFormGroup>
            <UFormGroup label="Notify on Data Quality Issues" name="notifyOnQualityIssues">
              <UToggle v-model="settings.notifyOnQualityIssues" />
            </UFormGroup>
          </div>

          <!-- API Settings -->
          <div v-if="activeSection === 'api'" class="space-y-6">
            <UFormGroup label="API Key" name="apiKey">
              <div class="flex space-x-2">
                <UInput v-model="settings.apiKey" disabled class="flex-1" />
                <UButton @click="regenerateApiKey">Regenerate</UButton>
              </div>
            </UFormGroup>
            <UFormGroup label="Rate Limit (requests per minute)" name="rateLimit">
              <UInput v-model="settings.rateLimit" type="number" min="1" />
            </UFormGroup>
            <UFormGroup label="Enable API Logging" name="apiLogging">
              <UToggle v-model="settings.apiLogging" />
            </UFormGroup>
            <UFormGroup label="CORS Origins" name="corsOrigins">
              <UTextarea v-model="settings.corsOrigins" placeholder="http://localhost:3000\nhttps://app.example.com" />
            </UFormGroup>
          </div>

          <!-- Save Button -->
          <div class="mt-8 pt-6 border-t border-gray-200">
            <UButton color="primary" @click="saveSettings" :loading="saving">
              Save Settings
            </UButton>
          </div>
        </div>
      </div>
    </UiContentCard>
  </div>
</template>

<script setup lang="ts">
// Set page meta
definePageMeta({
  title: 'Settings',
  subtitle: 'Configure application preferences'
})

const activeSection = ref('general')

const settingsSections = [
  { key: 'general', label: 'General', icon: 'i-heroicons-cog-6-tooth' },
  { key: 'data-sources', label: 'Data Sources', icon: 'i-heroicons-circle-stack' },
  { key: 'notifications', label: 'Notifications', icon: 'i-heroicons-bell' },
  { key: 'api', label: 'API', icon: 'i-heroicons-code-bracket' }
]

const settings = ref({
  appName: 'Data Fusion Hub',
  pageSize: 25,
  refreshInterval: 30,
  theme: 'Light',
  connectionTimeout: 30,
  maxRetries: 3,
  sslVerification: true,
  retentionPeriod: 90,
  emailNotifications: true,
  slackWebhook: '',
  notifyOnFailure: true,
  notifyOnQualityIssues: false,
  apiKey: 'dfh_live_xxxxxxxxxxxxxxxx',
  rateLimit: 1000,
  apiLogging: true,
  corsOrigins: 'http://localhost:3000'
})

const saving = ref(false)

const saveSettings = () => {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    // Show success message
    console.log('Settings saved:', settings.value)
  }, 1000)
}

const regenerateApiKey = () => {
  const newKey = 'dfh_live_' + Math.random().toString(36).substring(2, 22)
  settings.value.apiKey = newKey
}
</script>
