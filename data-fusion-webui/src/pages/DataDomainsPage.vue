<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>
            Data Domains
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="showCreateDialog = true">
              New Domain
            </v-btn>
          </v-card-title>
          
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-10">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
            <p class="mt-2">Loading data domains...</p>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="pa-4">
            <v-alert type="error" dismissible @click:close="clearError">
              {{ error }}
            </v-alert>
          </div>
          
          <!-- Content -->
          <div v-else>
            <v-data-table
              :headers="headers"
              :items="domains"
              :search="search"
              class="elevation-1"
            >
              <template v-slot:top>
                <v-toolbar flat>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search Domains"
                    single-line
                    hide-details
                  ></v-text-field>
                  
                  <v-spacer></v-spacer>
                  
                  <v-dialog v-model="showCreateDialog" max-width="500px">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                        Create New Domain
                      </v-btn>
                    </template>
                    
                    <v-card>
                      <v-card-title>
                        <span class="headline">{{ formTitle }}</span>
                      </v-card-title>
                      
                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-text-field
                                v-model="editedDomain.name"
                                label="Domain Name"
                                required
                              ></v-text-field>
                            </v-col>
                            
                            <v-col cols="12">
                              <v-textarea
                                v-model="editedDomain.description"
                                label="Description"
                                rows="3"
                              ></v-textarea>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>
                      
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="closeDialog">
                          Cancel
                        </v-btn>
                        <v-btn color="blue darken-1" text @click="saveDomain">
                          Save
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-toolbar>
              </template>
              
              <template v-slot:item.actions="{ item }">
                <v-icon small class="mr-2" @click="editItem(item)">
                  mdi-pencil
                </v-icon>
                <v-icon small @click="deleteItem(item)">
                  mdi-delete
                </v-icon>
              </template>
            </v-data-table>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue' // Added computed import

// Reactive variables
const loading = ref(false)
const error = ref(null)
const search = ref('')
const showCreateDialog = ref(false)
const editedDomain = ref({
  id: null,
  name: '',
  description: ''
})

// Table headers
const headers = [
  { text: 'Name', value: 'name' },
  { text: 'Description', value: 'description' },
  { text: 'Actions', value: 'actions', sortable: false }
]

// Mock data - in a real app this would come from an API
const domains = ref([
  { id: 1, name: 'Customer Data', description: 'Data related to customers and their interactions' },
  { id: 2, name: 'Product Catalog', description: 'Information about products and inventory' },
  { id: 3, name: 'Financial Records', description: 'Financial data and transactions' }
])

// Methods
const clearError = () => {
  error.value = null
}

const editItem = (item) => {
  editedDomain.value = Object.assign({}, item)
  showCreateDialog.value = true
}

const deleteItem = (item) => {
  // In a real app, this would call an API to delete the domain
  console.log('Deleting domain:', item.name)
  domains.value = domains.value.filter(domain => domain.id !== item.id)
}

const closeDialog = () => {
  showCreateDialog.value = false
  editedDomain.value = { id: null, name: '', description: '' }
}

const saveDomain = () => {
  if (editedDomain.value.id) {
    // Update existing domain
    const index = domains.value.findIndex(d => d.id === editedDomain.value.id)
    if (index !== -1) {
      domains.value[index] = Object.assign({}, editedDomain.value)
    }
  } else {
    // Create new domain
    const newId = Math.max(...domains.value.map(d => d.id)) + 1
    editedDomain.value.id = newId
    domains.value.push(Object.assign({}, editedDomain.value))
  }
  
  closeDialog()
}

const formTitle = computed(() => {
  return editedDomain.value.id ? 'Edit Domain' : 'Create New Domain'
})

// Simulate loading data on mount
onMounted(() => {
  loading.value = true
  
  // Simulate API call delay
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
</script>