<template>
  <!-- whole page -->
  <div style="display: flex; align-items: center; justify-content: center; flex-flow: column; height: 100vh;">
    <div style="display: flex; width: 100%; height: 100%;">
      <!-- filters -->
      <div style="width: 10%; margin: 2rem 2rem;">
        <div>
          filter 1
        </div>

        <div>
          filter 2
        </div>

        <div>
          filter 3
        </div>

        <div>
          filter 4
        </div>
      </div>
      <!-- product list -->
      <div style="width: 90%; margin: 2rem .5rem; overflow-y: scroll; max-height: 100%; display: flex; flex-wrap: wrap; max-width: 90%;">
        <div v-for="item in data" class="card">
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
        right
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import data from "../fmp-data.json";


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