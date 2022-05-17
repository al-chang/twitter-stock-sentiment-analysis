<script lang="ts">
import { defineComponent } from "vue";
import StockCard from "../components/StockCard.vue";
import { Trend } from "@/components/StockCard.vue";

export default defineComponent({
  data() {
    return {
      stockTickers: [] as string[],
    };
  },
  async mounted() {
    const res = await fetch(`${import.meta.env.VITE_SERVER_URL}/stocks`);
    const data = (await res.json()) as {
      stocks: string[];
    };
    this.stockTickers = data.stocks;
  },
  components: { StockCard },
});
</script>

<template>
  <h1>Hello world</h1>
  <div class="stock-cards">
    <StockCard
      :key="index"
      v-for="(stockTicker, index) in stockTickers"
      :ticker="stockTicker"
    />
  </div>
</template>

<style scoped>
.stock-cards {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
}
</style>
