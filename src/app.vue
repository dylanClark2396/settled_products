<template>
  <!-- whole page -->
  <div style="display: flex; align-items: center; justify-content: center; flex-flow: column; height: 100vh;">
    <div class="give-border" style="display: flex; width: 100%; height: 100%;">
      <!-- filters -->
      <div class="give-border" style="width: 10%; margin: 1rem">
        left
      </div>
      <!-- product list -->
      <div class="give-border" style="width: 90%; margin: 1rem">
        right
      </div>
    </div>
  </div>
</template>

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
</style>