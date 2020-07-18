<template>
  <nav aria-label="Page navigation" class="pagination-wrapper">
    <ul class="pagination" v-if="needPagination">
      <li
        v-for="page in pages"
        :key="page.id"
        :class="{
          'page-item': true,
          active: page.page === current,
          disabled: page.disabled
        }"
      >
        <a
          href="#"
          class="page-link"
          @click.prevent="pageClick(page)"
          v-if="page.id === 'prev'"
          >&larr;</a
        >
        <a
          href="#"
          class="page-link"
          @click.prevent="pageClick(page)"
          v-else-if="page.id === 'next'"
          >&rarr;</a
        >
        <a href="#" class="page-link" @click.prevent="pageClick(page)" v-else>{{
          page.page
        }}</a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'pagination',
  props: {
    total: {
      type: Number,
      required: true
    },
    current: {
      type: Number,
      required: true
    },
    spread: {
      type: Number,
      default: 3
    }
  },
  methods: {
    pageClick(page) {
      if (page.disabled) return
      var newPage
      switch (page.page) {
        case 'prev':
          newPage = this.current - 1
          break
        case 'next':
          newPage = this.current + 1
          break
        default:
          newPage = page.page
      }
      this.$emit('page', newPage)
    }
  },
  computed: {
    needPagination() {
      if (this.total > 1) return true
      if (this.total === 1 && this.current !== this.total) return true
      return false
    },
    pages() {
      const { current, total, spread } = this

      // always show the first page
      const result = [
        { id: 'prev', page: 'prev', disabled: current === 1 },
        { id: 1, page: 1, disabled: current === 1 }
      ]

      let i = 2
      if (current - spread > 2) {
        result.push({ id: 2, page: '...', disabled: true })
        i = current - spread
      }

      while (i <= current + spread && i <= total) {
        result.push({ id: i, page: i, disabled: current === i })
        i++
      }

      if (i < total) {
        result.push({ id: i, page: '...', disabled: true })
        // show the last page
        result.push({ id: total, page: total, disabled: current === total })
      }

      result.push({ id: 'next', page: 'next', disabled: current === total })
      return result
    }
  }
}
</script>

<style lang="scss">
.pagination {
  width: max-content;
  margin: 8px auto;
}

.page-item:not(.disabled):hover {
  .page-link {
    background-color: #75a4d3;
    color: white;
  }
}

.page-item.active {
  .page-link {
    transition: background-color 0.15s ease;
    background-color: #426d98;
    color: white;
  }
  &:hover .page-link {
    background-color: #123d68;
  }
}
</style>
