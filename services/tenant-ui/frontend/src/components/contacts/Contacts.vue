<template>
  <h3 class="mt-0">Connections</h3>

  <ProgressSpinner v-if="loading" />
  <div v-else>
    <DataTable
      v-model:selection="selectedContact"
      :value="contacts"
      :paginator="true"
      :rows="10"
      striped-rows
      selection-mode="single"
    >
      <template #header>
        <div class="flex justify-content-between">
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText placeholder="Connection Search" disabled />
          </span>
          <Button
            icon="pi pi-refresh"
            class="p-button-rounded p-button-outlined"
            title="Refresh Table"
            @click="loadTable"
          ></Button>
        </div>
      </template>
      <Column :sortable="true" field="alias" header="Name" />
      <Column field="role" header="Role" />
      <Column field="state" header="State" />
      <Column field="status" header="Status" />
      <Column field="created_at" header="Created at" />
      <Column field="contact_id" header="ID" />
    </DataTable>
  </div>
  <Button
    v-if="contacts"
    class="create-contact"
    icon="pi pi-plus"
    label="Create Contact"
    @click="createContact"
  ></Button>

  <Dialog
    v-model:visible="displayAddContact"
    header="Create a new contact"
    :modal="true"
  >
    <CreateContact @success="contactCreated" />
  </Dialog>
</template>

<script setup lang="ts">
// Vue
import { ref, onMounted } from "vue";

// PrimeVue
import Button from "primevue/button";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import Dialog from "primevue/dialog";
import ProgressSpinner from "primevue/progressspinner";
import InputText from "primevue/inputtext";

// Other imports

import { useToast } from "vue-toastification";
import { useContactsStore } from "../../store";
import { storeToRefs } from "pinia";

// Other components
import CreateContact from "./CreateContact.vue";

const toast = useToast();

const contactsStore = useContactsStore();
// use the loading state from the store to disable the button...
const { loading, contacts, selectedContact } = storeToRefs(useContactsStore());

const loadTable = async () => {
  contactsStore.listContacts().catch((err) => {
    console.error(err);
    toast.error(`Failure: ${err}`);
  });
};

onMounted(async () => {
  loadTable();
});
// -----------------------------------------------/Loading contacts

// ----------------------------------------------------------------
// Adding Contacts
// ----------------------------------------------------------------
const displayAddContact = ref(false);

const createContact = () => {
  displayAddContact.value = !displayAddContact.value;
};

const contactCreated = async () => {
  // Emited from the contact creation component when a successful invite is made
  console.log(
    'contact created emit - do we want to "manually" load contacts or have the store automatically do it?'
  );
  loadTable();
};
// -----------------------------------------------/Adding contacts
</script>

<style scoped>
fieldset {
  display: flex;
  align-items: center;
  justify-content: center;
}

.create-contact {
  float: right;
  margin: 3rem 1rem 0 0;
}
.p-datatable-header input {
  padding-left: 3rem;
}
</style>