<template>
  <div class="voter" :class="{ 'voter--mini': mini }">
    <a
      class="voter-link"
      href
      :class="{ 'voter-link--green': this.value > 0 }"
      @click.prevent="voteUp"
    >
      <i class="fa fa-chevron-up"></i>
    </a>
    <div v-if="!mini || points > 0" class="voter-points">{{ points }}</div>
    <a
      v-if="!mini"
      class="voter-link"
      href
      :class="{ 'voter-link--red': this.value < 0 }"
      @click.prevent="voteDown"
    >
      <i class="fa fa-chevron-down"></i>
    </a>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator'

@Component
export default class Voter extends Vue {
  @Prop({ type: Number, default: 0 }) readonly points!: number
  @Prop({ type: Number, default: 0 }) readonly value!: number
  @Prop({ type: Boolean, default: false }) readonly mini!: number

  voteUp() {
    if (this.value <= 0) {
      this.$emit('input', 1)
    } else {
      this.$emit('input', 0)
    }
  }

  voteDown() {
    if (this.value >= 0) {
      this.$emit('input', -1)
    } else {
      this.$emit('input', 0)
    }
  }
}
</script>

<style lang="scss">
.voter {
  font-size: 2em;
  text-align: center;
  line-height: 1.1em;

  &.voter--mini {
    font-size: 0.95em;
    line-height: 1em;
    color: #aaaaaa;
    a.voter-link {
      color: inherit;
    }
    .voter-points {
      font-weight: normal;
    }
  }

  a.voter-link {
    color: gray;
    text-decoration: none;
    &.voter-link--green {
      color: #494;
    }
    &.voter-link--red {
      color: #c44;
    }
  }

  .voter-points {
    font-weight: bold;
  }
}
</style>
