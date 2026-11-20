<template>
  <section class="card p-5">
    <h2 class="text-sm font-semibold text-gray-900">过滤器</h2>

    <div class="mt-5">
      <div class="flex items-center justify-between">
        <h3 class="text-xs font-medium text-gray-500">会议 / 期刊类别</h3>
        <label class="flex cursor-pointer select-none items-center gap-1.5 text-xs text-gray-500">
          <input
            type="checkbox"
            class="peer sr-only"
            v-model="checkAll"
            :indeterminate.prop="isIndeterminate"
            @change="handleCheckAllChange"
          >
          <span
            class="flex h-4 w-4 shrink-0 items-center justify-center rounded border text-white transition"
            :class="(checkAll || isIndeterminate) ? 'border-blue-600 bg-blue-600' : 'border-gray-300 bg-white'"
          >
            <svg v-if="checkAll" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="isIndeterminate" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <rect x="4" y="9" width="12" height="2" rx="1"/>
            </svg>
          </span>
          全选
        </label>
      </div>

      <div class="mt-3 flex items-center gap-5">
        <label
          v-for="category in categories"
          :key="category"
          class="flex cursor-pointer select-none items-center gap-1.5 text-sm text-gray-700"
        >
          <input
            type="checkbox"
            class="peer sr-only"
            :value="category"
            v-model="checkedCategories"
            @change="handleCheckedCategoriesChange"
          >
          <span
            class="flex h-4 w-4 shrink-0 items-center justify-center rounded border border-gray-300 bg-white text-white transition peer-checked:border-blue-600 peer-checked:bg-blue-600 peer-focus-visible:ring-2 peer-focus-visible:ring-blue-200"
          >
            <svg class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clip-rule="evenodd"/>
            </svg>
          </span>
          {{ category }}
        </label>
      </div>
    </div>

    <div class="mt-6">
      <div class="flex items-baseline justify-between">
        <h3 class="text-xs font-medium text-gray-500">时间范围</h3>
        <span class="text-xs tabular-nums text-gray-400">{{ range[0] }} - {{ range[1] }}</span>
      </div>

      <div class="mt-4">
        <div class="relative h-5">
          <div class="absolute top-1/2 h-1 w-full -translate-y-1/2 rounded-full bg-gray-200"></div>
          <div class="absolute top-1/2 h-1 -translate-y-1/2 rounded-full bg-blue-600" :style="activeTrackStyle"></div>
          <input
            class="range-input"
            type="range"
            :min="min"
            :max="max"
            step="1"
            :value="range[0]"
            aria-label="起始年份"
            @input="handleLeftInput"
          >
          <input
            class="range-input"
            type="range"
            :min="min"
            :max="max"
            step="1"
            :value="range[1]"
            aria-label="终止年份"
            @input="handleRightInput"
          >
        </div>
        <div class="mt-2 flex justify-between text-[11px] text-gray-400">
          <span>{{ min }}</span>
          <span>1980</span>
          <span>2000</span>
          <span>{{ max }}</span>
        </div>
      </div>

      <div class="mt-4 flex items-start gap-3">
        <label class="flex-1">
          <span class="text-[11px] text-gray-400">起始年份</span>
          <input
            type="number"
            class="field mt-1 px-2 py-1.5 text-xs tabular-nums"
            :min="min"
            :max="range[1]"
            :value="range[0]"
            @change="handleFromYearChange"
          >
        </label>
        <span class="mt-5 text-gray-300">-</span>
        <label class="flex-1">
          <span class="text-[11px] text-gray-400">终止年份</span>
          <input
            type="number"
            class="field mt-1 px-2 py-1.5 text-xs tabular-nums"
            :min="range[0]"
            :max="max"
            :value="range[1]"
            @change="handleToYearChange"
          >
        </label>
      </div>
    </div>
  </section>
</template>

<script>
import store from '@/store'

const categoryOptions = ['A', 'B', 'C']

export default {
  name: 'content_filter',
  data () {
    const max = new Date().getFullYear()
    return {
      checkAll: store.state.categories.length === categoryOptions.length,
      checkedCategories: [...store.state.categories],
      categories: categoryOptions,
      isIndeterminate: false,
      min: 1930,
      max,
      range: [store.state.from_year, store.state.to_year],
      yearCommitTimer: null
    }
  },
  computed: {
    activeTrackStyle () {
      const span = this.max - this.min || 1
      const left = ((this.range[0] - this.min) / span) * 100
      const right = 100 - ((this.range[1] - this.min) / span) * 100
      return {
        left: `${Math.max(0, Math.min(100, left))}%`,
        right: `${Math.max(0, Math.min(100, right))}%`
      }
    }
  },
  beforeDestroy () {
    clearTimeout(this.yearCommitTimer)
  },
  methods: {
    handleCheckAllChange (val) {
      this.checkedCategories = val ? [...this.categories] : []
      this.isIndeterminate = false
      this.commitCategories()
    },
    handleCheckedCategoriesChange () {
      const count = this.checkedCategories.length
      this.checkAll = count === this.categories.length
      this.isIndeterminate = count > 0 && count < this.categories.length
      this.commitCategories()
    },
    commitCategories () {
      store.commit('mutate_categories', [...this.checkedCategories])
      store.commit('mutate_display_papers_by_filter')
    },
    handleLeftInput (event) {
      const val = Math.min(Number(event.target.value), this.range[1])
      this.range = [val, this.range[1]]
      this.scheduleYearCommit()
    },
    handleRightInput (event) {
      const val = Math.max(Number(event.target.value), this.range[0])
      this.range = [this.range[0], val]
      this.scheduleYearCommit()
    },
    handleFromYearChange (event) {
      const val = this.normalizeYear(event, this.min, this.range[1], this.range[0])
      this.range = [val, this.range[1]]
      this.commitYears()
    },
    handleToYearChange (event) {
      const val = this.normalizeYear(event, this.range[0], this.max, this.range[1])
      this.range = [this.range[0], val]
      this.commitYears()
    },
    normalizeYear (event, low, high, fallback) {
      const parsed = parseInt(event.target.value, 10)
      const val = Number.isNaN(parsed) ? fallback : Math.min(Math.max(parsed, low), high)
      event.target.value = val
      return val
    },
    scheduleYearCommit () {
      clearTimeout(this.yearCommitTimer)
      this.yearCommitTimer = setTimeout(this.commitYears, 300)
    },
    commitYears () {
      store.commit('mutate_from_year', this.range[0])
      store.commit('mutate_to_year', this.range[1])
      if (store.state.papers !== null) {
        store.commit('mutate_display_papers_by_filter')
      }
    }
  }
}
</script>
