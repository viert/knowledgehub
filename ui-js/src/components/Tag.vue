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
        <div class="tag-expand_name">{{ tag && tag.name || name }}</div>
        <div class="tag-expand_content">
          <div class="tag-expand_loading" v-if="tagLoading">
            <i class="fa fa-spinner fa-spin fa-2x"></i>
          </div>
          <fragment v-else>
            <div v-if="tag" class="tag-expand_counters">
              <div class="tag-expand_counters-subs">{{ tag.subscribers_count }} subscribers</div>
              <div class="tag-expand_counters-questions">{{ tag.questions_count }} questions</div>
            </div>
            <p class="tag-expand_description">{{ tag && tag.description || defaultTagDescription }}</p>
            <div class="tag-expand_ctrl">
              <SpinnerButton
                v-if="subscribed"
                :loading="subscribeInProgress"
                @click="handleUnsubscribe"
                class="btn btn-sm btn-block btn-outline-danger"
              >Unsubscribe</SpinnerButton>
              <SpinnerButton
                v-else
                :loading="subscribeInProgress"
                @click="handleSubscribe"
                class="btn btn-sm btn-block btn-outline-primary"
              >Subscribe</SpinnerButton>
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

<script>
import { mapState } from 'vuex'
export default {
  props: {
    name: {
      type: String,
      required: true
    },
    cross: {
      type: Boolean,
      default: false
    },
    expandable: {
      type: Boolean,
      default: true
    },
    clickable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      showDetails: false,
      tagLoading: false,
      subscribeInProgress: false
    }
  },
  computed: {
    ...mapState({
      tagSubscriptions: state => state.users.tagSubscriptions
    }),
    defaultTagDescription() {
      return `Questions related to ${this.name}`
    },
    subscribed() {
      return this.tagSubscriptions.includes(this.name)
    },
    tag() {
      const tag = this.$store.getters['tags/getTag'](this.name)
      if (!tag) {
        this.loadTag()
      }
      return tag
    }
  },
  methods: {
    handleSubscribe() {
      this.subscribeInProgress = true
      this.$store.dispatch('users/subscribeToTag', this.name).finally(() => {
        this.subscribeInProgress = false
      })
    },
    handleUnsubscribe() {
      this.subscribeInProgress = true
      this.$store
        .dispatch('users/unsubscribeFromTag', this.name)
        .finally(() => {
          this.subscribeInProgress = false
        })
    },
    loadTag() {
      this.tagLoading = true
      this.$store.dispatch('tags/lazyLoadTag', this.name).finally(() => {
        this.tagLoading = false
      })
    },
    crossClick(e) {
      this.$emit('close', e)
    },
    tagClick(e) {
      this.$emit('click', e)
    }
  }
}
</script>

<style lang='scss'>
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

  .expand-enter-active,
  .expand-leave-active {
    transition: opacity 0.3s;
  }

  .expand-enter,
  .expand-leave-to {
    opacity: 0;
  }
}
</style>
