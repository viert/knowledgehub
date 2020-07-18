<template>
  <div v-if="appInfo.app" class="page-footer">
    &copy; 2020 {{ appInfo.app.name }} v.{{ appInfo.app.version }}
    <span class="details">
      Flask {{ appInfo.flask_version }} / MongoDB
      {{ appInfo.mongodb.meta.version }}
    </span>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState({ appInfo: state => state.data.appInfo })
  }
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
