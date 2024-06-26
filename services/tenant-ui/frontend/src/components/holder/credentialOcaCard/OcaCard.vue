<template>
  <div v-if="loadingCardOca">
    <SkeletonCard />
  </div>
  <div v-else>
    <CredentialCard10 :overlay="overlay" :credential="props.credential" />
    <!-- <Card>
      <template #title> Simple Card </template>
      <template #content>
        <p>
          {{ props.credential.state }}
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore
          sed consequuntur error repudiandae numquam deserunt quisquam repellat
          libero asperiores earum nam nobis, culpa ratione quam perferendis
          esse, cupiditate neque quas!

          {{  overlay }}
        </p>
      </template>
    </Card> -->
  </div>
</template>

<script setup lang="ts">
// Types
import { OcaRecord, IndyCredInfo } from '@/types/acapyApi/acapyInterface';
import OverlayBundle from '@/overlayLibrary/types/overlay/OverlayBundle';

// Vue
import { onMounted, ref, Ref } from 'vue';
// PrimeVue
import Card from 'primevue/card';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'vue-toastification';
// State
import { useHolderStore } from '@/store';
import { storeToRefs } from 'pinia';
// OCA Components
import CredentialCard10 from './CredentialCard10.vue';
import OverlayBundleFactory from '@/overlayLibrary/services/OverlayBundleFactory';
// Other
import SkeletonCard from '@/components/common/SkeletonCard.vue';

const props = defineProps<{
  credential: IndyCredInfo;
}>();

const toast = useToast();
const confirm = useConfirm();

// State
const holderStore = useHolderStore();
const { ocas } = storeToRefs(useHolderStore());

// OCA Fetching
const overlay: Ref<OverlayBundle | undefined> = ref(undefined);

const loadingCardOca = ref(false);
const loadOcaForCred = async () => {
  try {
    loadingCardOca.value = true;

    // From the oca list, get the oca (if there is one) for this cred
    const ocaRecord = ocas.value.find(
      (o) => o.cred_def_id === props.credential.cred_def_id
    );

    if (!ocaRecord) {
      // No OCA for this cred, done here
      loadingCardOca.value = false;
      return;
    }
    console.log(ocaRecord.url);

    // If the OCA has a URL, use the factory to get and parse the bundle
    if (ocaRecord.url) {
      overlay.value = await OverlayBundleFactory.fetchOverlayBundle(
        props.credential.cred_def_id || '',
        ocaRecord.url || ''
      );
      console.log(overlay);
    }
  } catch (err) {
    console.error(err);
    toast.error(`OCA loading failed for ${props.credential.cred_def_id}`);
  } finally {
    loadingCardOca.value = false;
  }
};

onMounted(async () => {
  // When loading this card, check for, and then fetch the OCA bundle and apply it
  loadOcaForCred();
});
</script>

<style scoped></style>
