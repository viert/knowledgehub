<template>
  <div
    class="tag"
    :class="{ 'tag--derived': derived, 'tag--clickable': clickable }"
    @click.self="tagClick"
  >
    {{ name }}
    <a v-if="cross" class="tag-cross" href="#" @click.prevent="crossClick">
      <i class="fa fa-times"></i>
    </a>
  </div>
</template>

<script>
export default {
  props: {
    derived: {
      type: Boolean,
      default: false
    },
    name: {
      type: String,
      required: true
    },
    cross: {
      type: Boolean,
      default: false
    },
    clickable: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    crossClick(e) {
      this.$emit('close', e)
    },
    tagClick(e) {
      this.$emit('click', e)
    }
  }
}
</script>

<style>
.tag {
  font-size: 80%;
  padding: 1px 4px;
  box-sizing: border-box;
  border-radius: 2px;
  color: black;
  display: inline-block;
  margin-right: 4px;
  background: #efe;
  border: 1px solid #cdc;
}

.tag.tag--clickable {
  cursor: pointer;
}

.tag.tag--derived {
  border: 1px solid #ccd;
  background: #eef;
}

.tag a.tag-cross {
  color: black;
  font-size: 0.9em;
  margin-left: 1px;
}
</style>
