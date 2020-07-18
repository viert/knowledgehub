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

  public get defaultTagDescription() {
    return `Questions related to ${this.name}`
  }

  public get subscribed() {
    return this.tagSubscriptions.includes(this.name)
  }

  public get tag() {
    const tag = this.$store.getters['tags/getTag'](this.name)
    if (!tag) {
      this.loadTag()
    }
    return tag
  }

  loadTag() {
    this.tagLoading = true
    this.$store.dispatch('tags/lazyLoadTag', this.name).finally(() => {
      this.tagLoading = false
    })
  }

  handleSubscribe() {
    this.subscribeInProgress = true
    this.$store.dispatch('users/subscribeToTag', this.name).finally(() => {
      this.subscribeInProgress = false
    })
  }

  handleUnsubscribe() {
    this.subscribeInProgress = true
    this.$store.dispatch('users/unsubscribeFromTag', this.name).finally(() => {
      this.subscribeInProgress = false
    })
  }

  crossClick() {
    this.$emit('close')
  }

  tagClick(e: Event) {
    this.$emit('click', e)
  }
}
</script>

<style lang="scss">
.tag {
  font-size: 80%;
  position: relative;
  padding: 1px 8px;
  box-sizing: border-box;
  border-radius: 3px;
  color: black;
  display: inline-block;
  margin-right: 4px;
  background: #f9f9f9;
  border: 1px solid #ccc;

  &.tag--clickable {
    cursor: pointer;
  }

  a.tag-cross {
    color: black;
    font-size: 0.9em;
    margin-left: 1px;
  }

  .tag-expand {
    z-index: 10;
    box-sizing: border-box;
    border-radius: 3px;
    color: black;
    display: block;
    position: absolute;
    top: -1px;
    left: -1px;
    width: 250px;
    border: 1px solid #ccc;
    background: white;

    .tag-expand_name {
      background: #f9f9f9;
      padding: 1px 8px;
      font-weight: bold;
    }

    .tag-expand_content {
      padding: 8px;

      .tag-expand_description {
        margin-bottom: 12px;
      }

      .tag-expand_counters {
        display: flex;
        justify-content: center;
        margin-bottom: 12px;
        div {
          margin-right: 1em;
        }
      }

      .tag-expand_loading {
        text-align: center;
        margin: 20px 0;
      }
    }
  }
}

.expand-enter-active,
.expand-leave-active {
  transition: opacity 0.3s;
}

.expand-enter,
.expand-leave-to {
  opacity: 0;
}
</style>
