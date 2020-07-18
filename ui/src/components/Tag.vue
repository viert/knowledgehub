<template>
  <div
    class="tag"
    :class="{ 'tag--clickable': clickable }"
    @click.self="tagClick"
    @mouseenter="showDetails = true"
    @mouseleave="showDetails = false"
  >
    <transition v-if="expandable" name="expand">
      <div v-if="showDetails" class="tag-expand">
        <div class="tag-expand_name">{{ (tag && tag.name) || name }}</div>
        <div class="tag-expand_content">
          <div class="tag-expand_loading" v-if="tagLoading">
            <i class="fa fa-spinner fa-spin fa-2x"></i>
          </div>
          <fragment v-else>
            <div v-if="tag" class="tag-expand_counters">
              <div class="tag-expand_counters-subs"
                >{{ tag.subscribers_count }} subscribers</div
              >
              <div class="tag-expand_counters-questions"
                >{{ tag.questions_count }} questions</div
              >
            </div>
            <p class="tag-expand_description">{{
              (tag && tag.description) || defaultTagDescription
            }}</p>
            <div class="tag-expand_ctrl">
              <SpinnerButton
                v-if="subscribed"
                :loading="subscribeInProgress"
                @click="handleUnsubscribe"
                class="btn btn-sm btn-block btn-outline-danger"
                >Unsubscribe</SpinnerButton
              >
              <SpinnerButton
                v-else
                :loading="subscribeInProgress"
                @click="handleSubscribe"
                class="btn btn-sm btn-block btn-outline-primary"
                >Subscribe</SpinnerButton
              >
            </div>
          </fragment>
        </div>
      </div>
    </transition>
    {{ name }}
    <a v-if="cross" class="tag-cross" href="#" @click.prevent="crossClick">
      <i class="fa fa-times"></i>
    </a>
  </div>
</template>

<script lang="ts">
import { mapState } from 'vuex'
import { Component, Prop, Vue } from 'vue-property-decorator'
import { namespace } from 'vuex-class'
const users = namespace('users')

@Component
export default class Tag extends Vue {
  @Prop({ type: String, required: true }) readonly name!: string
  @Prop({ type: Boolean, default: false }) readonly cross!: boolean
  @Prop({ type: Boolean, default: true }) readonly expandable!: boolean
  @Prop({ type: Boolean, default: false }) readonly clickable!: boolean

  private showDetails = false
  private tagLoading = false
  private subscribeInProgress = false

  @users.State
  public tagSubscriptions: any
}
</script>

<style scoped></style>
