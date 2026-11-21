<template>
  <section class="card overflow-hidden">
    <div class="border-b border-gray-100 p-4 sm:p-5">
      <form class="flex gap-2" @submit.prevent="handleSearch">
        <div class="relative flex-1">
          <svg class="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
               viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd"
                  d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                  clip-rule="evenodd"/>
          </svg>
          <input
            v-model="search_input"
            class="field pl-9 pr-9"
            type="text"
            placeholder="搜索论文标题，多个关键词用空格分隔"
            aria-label="搜索论文标题，多个关键词用空格分隔"
            autocomplete="off"
            spellcheck="false"
            enterkeyhint="search"
            @input="handleInput"
          >
          <button
            v-if="search_input"
            type="button"
            class="absolute right-2 top-1/2 flex h-5 w-5 -translate-y-1/2 items-center justify-center rounded-full text-gray-400 transition hover:bg-gray-100 hover:text-gray-600"
            aria-label="清空搜索"
            @click="clearSearch"
          >
            <svg class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
        <button
          type="submit"
          class="inline-flex shrink-0 items-center gap-1.5 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="data_loading"
        >
          <svg v-if="data_loading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          <svg v-else class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd"
                  d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
                  clip-rule="evenodd"/>
          </svg>
          <span class="hidden sm:inline">搜索</span>
        </button>
      </form>
    </div>

    <div class="p-4 sm:p-5">
      <div v-if="error" class="mb-3 flex items-start gap-2 rounded-lg bg-red-50 px-3 py-2 text-xs text-red-600"
           role="alert">
        <svg class="mt-0.5 h-4 w-4 shrink-0" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
          <path fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clip-rule="evenodd"/>
        </svg>
        {{ error }}
      </div>

      <div v-if="data_loading && !hasSearched" aria-hidden="true">
        <div v-for="i in 3" :key="i" class="animate-pulse border-b border-gray-100 py-3 last:border-0 motion-reduce:animate-none">
          <div class="h-4 w-3/4 rounded bg-gray-100"></div>
          <div class="mt-2 h-3 w-1/2 rounded bg-gray-100"></div>
          <div class="mt-3 flex gap-2">
            <div class="h-5 w-12 rounded bg-gray-100"></div>
            <div class="h-5 w-16 rounded bg-gray-100"></div>
            <div class="h-5 w-8 rounded bg-gray-100"></div>
          </div>
        </div>
      </div>

      <template v-else-if="hasSearched">
        <div class="mb-2 flex flex-wrap items-center justify-between gap-2">
          <p class="text-xs text-gray-500" role="status" aria-live="polite" aria-atomic="true">
            共 <span class="font-semibold tabular-nums text-gray-700">{{ formattedTotal }}</span> 篇结果
          </p>
          <div class="flex items-center gap-0.5 rounded-lg bg-gray-100 p-0.5 text-xs" role="group" aria-label="排序方式">
            <button
              v-for="option in sortOptions"
              :key="option.value"
              type="button"
              class="rounded-md px-2 py-1 transition"
              :class="sort === option.value ? 'bg-white font-medium text-blue-600 shadow-sm' : 'text-gray-500 hover:text-gray-700'"
              :aria-pressed="String(sort === option.value)"
              @click="changeSort(option.value)"
            >{{ option.label }}</button>
          </div>
        </div>

        <div :class="{ 'pointer-events-none opacity-50': data_loading }" :aria-busy="data_loading ? 'true' : 'false'">
          <ul v-if="papers.length" role="list" class="divide-y divide-gray-100">
            <li v-for="paper in papers" :key="genPaperKey(paper)">
              <component
                :is="paper.url ? 'a' : 'div'"
                :href="paper.url || undefined"
                :target="paper.url ? '_blank' : undefined"
                :rel="paper.url ? 'noopener' : undefined"
                class="group block rounded-lg px-2 py-3 transition hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-200"
              >
                <span class="block text-sm font-semibold leading-relaxed text-gray-900 transition group-hover:text-blue-600"
                      v-html="paper.title"></span>
                <div class="mt-1.5 flex flex-wrap gap-x-2 gap-y-1 text-[11px] text-gray-500">
                  <span v-for="author in visibleAuthors(paper)" :key="author">{{ author }}</span>
                </div>
                <div class="mt-2 flex flex-wrap items-center gap-2">
                  <span class="rounded bg-gray-100 px-1.5 py-0.5 text-[11px] tabular-nums text-gray-600">{{ paper.year }}</span>
                  <span class="rounded bg-gray-100 px-1.5 py-0.5 text-[11px] text-gray-600">{{ paper.abbreviation }}</span>
                  <span class="rounded px-1.5 py-0.5 text-[11px] font-medium" :class="categoryClass(paper.category)">
                    {{ paper.category }}
                  </span>
                </div>
              </component>
            </li>
          </ul>

          <div v-if="papers.length === 0" class="py-12 text-center">
            <svg class="mx-auto h-10 w-10 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="1.5" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M21 21l-4.35-4.35M17 10.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z"/>
            </svg>
            <p class="mt-3 text-sm font-medium text-gray-500">没有找到相关论文</p>
            <p class="mt-1 text-xs text-gray-400">多个关键词需同时命中，可减少关键词或放宽年份与类别筛选</p>
          </div>

          <nav v-if="totalPages > 1" class="mt-4 flex items-center justify-center gap-3 text-xs" aria-label="结果分页">
            <button
              type="button"
              class="rounded-lg border border-gray-200 px-3 py-1.5 text-gray-600 transition hover:border-gray-300 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
              :disabled="page <= 1 || data_loading"
              @click="goPage(page - 1)"
            >上一页</button>
            <span class="tabular-nums text-gray-500" aria-live="off">{{ page }} / {{ totalPages }}</span>
            <button
              type="button"
              class="rounded-lg border border-gray-200 px-3 py-1.5 text-gray-600 transition hover:border-gray-300 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
              :disabled="page >= totalPages || data_loading"
              @click="goPage(page + 1)"
            >下一页</button>
          </nav>
        </div>
      </template>

      <div v-else class="py-12 text-center">
        <svg class="mx-auto h-10 w-10 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.5" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M21 21l-4.35-4.35M17 10.5a6.5 6.5 0 11-13 0 6.5 6.5 0 0113 0z"/>
        </svg>
        <p class="mt-3 text-sm font-medium text-gray-500">输入关键词开始检索</p>
        <p class="mt-1 text-xs text-gray-400">默认按发表年份倒序，可切换为按相关性排序</p>
      </div>
    </div>
  </section>
</template>

<script>
import store from '@/store'
import { request } from '@/requests'

const PAGE_SIZE = 20

export default {
  name: 'content_search',
  data () {
    return {
      search_input: '',
      data_loading: false,
      hasSearched: false,
      error: '',
      papers: [],
      total: 0,
      page: 1,
      sort: 'time',
      lastKeys: '',
      filterTimer: null,
      sortOptions: [
        { value: 'time', label: '时间倒序' },
        { value: 'relevance', label: '相关性' }
      ]
    }
  },
  computed: {
    totalPages () {
      return Math.max(1, Math.ceil(this.total / PAGE_SIZE))
    },
    formattedTotal () {
      return this.total.toLocaleString('en-US')
    },
    filterSignature () {
      return [
        store.state.categories.join(''),
        store.state.from_year,
        store.state.to_year
      ].join('|')
    },
    searchSeq () {
      return store.state.search_seq
    }
  },
  watch: {
    filterSignature () {
      clearTimeout(this.filterTimer)
      this.filterTimer = setTimeout(() => {
        if (this.hasSearched) this.fetchPage(1)
      }, 300)
    },
    // 点击词云等外部入口时，同步输入框并直接检索
    searchSeq () {
      const keys = store.state.search_keys
      if (!keys) return
      this.search_input = keys
      this.lastKeys = keys
      this.fetchPage(1)
    }
  },
  beforeDestroy () {
    clearTimeout(this.filterTimer)
  },
  methods: {
    handleInput () {
      if (this.search_input === '') {
        this.clearSearch()
      }
    },
    clearSearch () {
      this.search_input = ''
      this.hasSearched = false
      this.error = ''
      this.lastKeys = ''
      this.papers = []
      this.total = 0
      this.page = 1
    },
    genPaperKey (paper) {
      return `${paper.title}${paper.url}`
    },
    visibleAuthors (paper) {
      return (paper.authors || []).filter(author => author.indexOf('&') === -1)
    },
    categoryClass (category) {
      if (category === 'A') return 'bg-emerald-50 text-emerald-600'
      if (category === 'B') return 'bg-amber-50 text-amber-600'
      return 'bg-gray-100 text-gray-500'
    },
    handleSearch () {
      const keys = this.search_input.trim()
      if (keys === '') return
      this.lastKeys = keys
      this.fetchPage(1)
    },
    changeSort (sort) {
      if (this.sort === sort) return
      this.sort = sort
      if (this.hasSearched) this.fetchPage(1)
    },
    goPage (page) {
      if (page < 1 || page > this.totalPages || this.data_loading) return
      this.fetchPage(page)
    },
    fetchPage (page) {
      if (!this.lastKeys) return
      this.data_loading = true
      this.error = ''

      request({
        url: '/api/v1/search',
        method: 'post',
        data: {
          yf: store.state.from_year,
          yt: store.state.to_year,
          category: store.state.categories,
          keys: this.lastKeys,
          sort: this.sort,
          page,
          page_size: PAGE_SIZE
        }
      }).then(res => {
        this.papers = res.data.papers || []
        this.total = res.data.total || 0
        this.page = res.data.page || page
        this.hasSearched = true
        this.data_loading = false
        store.commit('mutate_search_done')
      }).catch(() => {
        this.error = '请求超时，请稍后重试'
        this.data_loading = false
      })
    }
  }
}
</script>
