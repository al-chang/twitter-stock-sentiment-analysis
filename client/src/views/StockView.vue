<script lang="ts">
import { defineComponent } from "vue";

interface StockSentimentData {
  num_pos: number;
  time: string;
  total: number;
}

export default defineComponent({
  data() {
    return {
      ticker: "",
      data: [] as StockSentimentData[],
    };
  },
  async mounted() {
    this.ticker = this.$route.params.ticker as string;
    const res = await fetch(
      `${import.meta.env.VITE_SERVER_URL}/stocks/${this.ticker}`
    );
    this.data = await res.json();
  },
});
</script>

<template>
  <h2>{{ ticker }}</h2>
  <p :key="index" v-for="(sentiment, index) in data">
    {{ sentiment.num_pos }}
  </p>
</template>
