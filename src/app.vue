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
              Symbol: {{ item.symbol }}
            </div>
            <div>
              Sector: {{ item.sector }}
            </div>
            <div>
              Founded: {{ item.founded }}
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </div>

  <UModal v-model="isFilterModalOpen">
    <div class="p-4">
      Symbol
      <USelectMenu v-model="symbolfilter" :options="symbolOptions"/>
    </div>
  </UModal>
</template>
<script setup lang="ts">
import tempData from "../fmp-data.json";

interface TempData {
  symbol: string; 
  name: string; 
  sector: string; 
  subSector: string; 
  headQuarter: string; 
  dateFirstAdded: string;
  cik: string; 
  founded: string;
}

const isFilterModalOpen = ref(false)

const searchFilter = ref()

const symbolfilter = ref()

const symbolOptions = computed(() => {
  return tempData.map((temp) => {
    return temp.symbol
  })
})

const filteredRows = computed(() => {
  console.log(symbolfilter.value)
  if (!symbolfilter.value) {
    return tempData
  }

  return tempData.filter(item => item.symbol.toLowerCase() === symbolfilter.value.toLowerCase());

})

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
@media only screen and (min-width: 1900px) {
  .card {
    flex: 0 0 calc(33.33% - 20px);
    max-width: calc(33.33% - 20px);
    margin: 10px;
    box-sizing: border-box; 
  }
}
</style>