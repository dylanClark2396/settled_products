<template>
  <!-- whole page -->
  <div style="display: flex; align-items: center; justify-content: center; flex-flow: column; max-height: 100vh;">
    <div style="display: flex; margin-top: 1rem; flex-flow: row;">
      <!-- search bar -->
       <div style="margin-right: 1rem;">
         <UInput v-model="searchFilter" placeholder="Search"/>
       </div>
      <UButton label="Filter" @click="isFilterModalOpen = true" />
    </div>
    <!-- product list -->
    <div style="width: 95%; overflow-y: auto; max-height: 95%; display: flex; flex-wrap: wrap;">
      <div v-for="item in filteredRows" class="card">
        <UCard :ui="{background: 'bg-transparent', divide: 'divide-y divide-stone-400', ring: 'ring-1 ring-stone-400'}">
          <template #header>
            {{ item.name }}
          </template>
          <div>
            <div>
              Product Type: {{ item.product_type }}
            </div>
            <div>
              Width: {{ item.width }}
            </div>
            <div>
              Depth: {{ item.depth }}
            </div>
            <div>
              Height: {{ item.height }}
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </div>

  <UModal v-model="isFilterModalOpen" :ui="{container: 'items-center'}">
    <div class="p-4" style="display: flex; flex-direction: column;">
      Product Type
      <UButtonGroup size="sm" orientation="horizontal">
        <USelectMenu v-model="productTypeFilter" :options="productTypeOptions" @update:model-value="addFilterControl('product_type', productTypeFilter)"/>
        <UButton icon="i-heroicons:x-mark-solid" color="red" v-if="productTypeFilter" @click="removeFilterControl('product_type'), productTypeFilter = ''" />
      </UButtonGroup>
    </div>
    <div class="p-4" style="display: flex; flex-direction: column;">
      Width
      <UButtonGroup size="sm" orientation="horizontal">
        <UInput v-model="widithFilter" @update:model-value="addFilterControl('width', widithFilter)"/>
        <UButton icon="i-heroicons:x-mark-solid" color="red" v-if="widithFilter" @click="removeFilterControl('width'), widithFilter = ''" />
      </UButtonGroup>
    </div>
    <div class="p-4" style="display: flex; flex-direction: column;">
      Depth
      <UButtonGroup size="sm" orientation="horizontal">
        <UInput v-model="depthFilter" @update:model-value="addFilterControl('depth', depthFilter)"/>
        <UButton icon="i-heroicons:x-mark-solid" color="red" v-if="depthFilter" @click="removeFilterControl('depth'), depthFilter = ''" />
      </UButtonGroup>
    </div>
    <div class="p-4"  style="display: flex; flex-direction: column;">
      Height
      <UButtonGroup size="sm" orientation="horizontal">
        <UInput v-model="heightFilter" @update:model-value="addFilterControl('height', heightFilter)"/>
        <UButton icon="i-heroicons:x-mark-solid" color="red" v-if="heightFilter" @click="removeFilterControl('height'), heightFilter = ''" />
      </UButtonGroup>
    </div>
  </UModal>
</template>
<script setup lang="ts">
import tempData from "../settled_product_database_acrylic_bins.json";

interface TempData {
  [id: string]: string;
  name: string; 
  image: string;
  width: string;
  depth: string;
  height: string;
  sku: string;
  store: string;
  price: string
  room_used_in: string;
  product_type: string;
  material: string;
}

const isFilterModalOpen = ref(false)

const searchFilter = ref()

const productTypeFilter = ref('')
const widithFilter = ref('')
const depthFilter = ref('')
const heightFilter = ref('')


const filters = ref<{[id: string]: string}>({})

const productTypeOptions = computed(() => {
  return [...new Set(tempData.map((temp) => temp.product_type).filter(type => type))];
})

const filteredRows = computed(() => {
  return tempData.filter((item: TempData) => 
    Object.keys(filters.value).every(key =>{
      console.log(key)
      return item[key].toLowerCase() === filters.value[key].toLowerCase() || filters.value[key] === undefined
    })
  );
})

const addFilterControl = (filterControl: string, filterValue: string) => {
   filters.value[filterControl] = filterValue
}

const removeFilterControl = (filterControl: string) => {
   delete filters.value[filterControl]
}

</script>
<style lang="css">
.give-border {
  border: 2px dotted rgb(96 139 168);
}

.box {
  display: flex;
  align-items: center;
  justify-content: center;
  height: fit-content;
  width: fit-content;
}

.card {
  flex: 0 0 calc(100% - 20px);
  max-width: calc(100% - 20px);
  margin: 10px;
  box-sizing: border-box; 
}

@media only screen and (min-width: 1000px) {
  .card {
    flex: 0 0 calc(50% - 20px);
    max-width: calc(50% - 20px);
    margin: 10px;
    box-sizing: border-box; 
  }
}
@media only screen and (min-width: 1400px) {
  .card {
    flex: 0 0 calc(33.33% - 20px);
    max-width: calc(33.33% - 20px);
    margin: 10px;
    box-sizing: border-box; 
  }
}
</style>