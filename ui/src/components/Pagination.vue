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

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

interface PageDescriptor {
  id: number | 'prev' | 'next' // page number or prev/next
  page: number | string // page label
  disabled: boolean
}

@Component
export default class Pagination extends Vue {
  @Prop({ type: Number, required: true }) readonly total!: number
  @Prop({ type: Number, required: true }) readonly current!: number
  @Prop({ type: Number, default: 3 }) readonly spread!: number

  pageClick(page: PageDescriptor) {
    if (page.disabled) return
    let newPage: number
    switch (page.page) {
      case 'prev':
        newPage = this.current - 1
        break
      case 'next':
        newPage = this.current + 1
        break
      default:
        newPage = page.page as number
    }
    this.$emit('page', newPage)
  }

  get needPagination() {
    // more than 1 page -> need pagination
    if (this.total > 1) return true

    // just one page, but accidentally (i.e. by url) an invalid page was chosen,
    // we need to show pagination to make user able to switch to a valid page
    if (this.total === 1 && this.current !== this.total) return true

    // otherwise no pagination is needed
    return false
  }

  get pages() {
    // pages list generator
    const { current, total, spread } = this

    const result: PageDescriptor[] = [
      { id: 'prev', page: 'prev', disabled: current === 1 },
      // always show the first page
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
