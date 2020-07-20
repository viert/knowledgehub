<template>
  <div v-if="appInfo" class="page-footer">
    &copy; 2020 {{ appInfo.app.name }} v.{{ appInfo.app.version }}
    <span class="details">
      Flask {{ appInfo.flask_version }} / MongoDB
      {{ appInfo.mongodb.meta.version }}
    </span>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
import { AppInfo } from '../store/types'

const data = namespace('data')

@Component
export default class PageFooter extends Vue {
  @data.State('appInfo') appInfo!: () => AppInfo | null
}
</script>

<style lang="scss">
.page-footer {
  height: 56px;
  display: flex;
  align-items: center;
  background-color: white;
  border-top: 1px solid #dfd7ca;
  padding: 0 16px;
  font-family: Montserrat;
  font-size: 0.75em;
  .details {
    margin-left: 20px;
    color: #aaaaaa;
  }
}
</style>
