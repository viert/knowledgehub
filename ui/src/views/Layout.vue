<template>
  <div class="page-layout">
    <PageHeader />
    <div class="page-wrapper">
      <router-view></router-view>
    </div>
    <PageFooter />
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import PageHeader from './PageHeader.vue'
import PageFooter from './PageFooter.vue'

@Component({
  components: {
    PageFooter,
    PageHeader
  }
})
export default class Layout extends Vue {}
</script>

<style lang="scss">
.page-wrapper {
  padding: 8px 0;
  background-color: #f9f9f9;
  .page-layout {
    display: flex;
    width: 82%;
    min-width: 1024px;
    margin: auto;
    box-sizing: border-box;
    min-height: calc(100vh - 128px);
    padding: 8px;
    main {
      background: white;
      flex-grow: 1;
    }

    aside {
      margin-left: 12px;
      background: white;
      width: 300px;
      min-width: 300px;
    }
  }
}
</style>
