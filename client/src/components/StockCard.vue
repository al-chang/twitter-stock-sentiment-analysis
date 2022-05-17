<script lang="ts">
import { defineComponent, type PropType } from "vue";

export enum Trend {
  UP = "positive",
  DOWN = "negative",
  NEUTRAL = "neutral",
}

export default defineComponent({
  props: {
    ticker: { type: String, required: true },
  },
});
</script>

<template>
  <router-link class="stock-card-link" :to="`/stock/${ticker}`">
    <div class="stock-card-container">
      <h2 class="stock-card-header">{{ `$${ticker}` }}</h2>
    </div>
  </router-link>
</template>

<style scoped>
.stock-card-link {
  text-decoration: none;
}
.stock-card-container {
  border: 1px solid lightgrey;
  padding: 20px;
  margin: 20px;
  text-align: center;
}

.stock-card-header {
  color: green;
}
</style>
