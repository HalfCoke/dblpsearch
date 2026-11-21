<template>
  <div>
    <section ref="section" class="card p-5 lg:flex lg:min-h-[360px] lg:flex-col">
      <h2 class="text-sm font-semibold text-gray-900">热门搜索</h2>
      <div
        v-if="keywords.length"
        ref="cloud"
        class="relative mt-3 h-56 overflow-hidden lg:h-auto lg:flex-1"
      >
        <button
          v-for="word in placedWords"
          :key="word.text"
          type="button"
          class="absolute -translate-x-1/2 -translate-y-1/2 whitespace-nowrap rounded leading-none transition-all duration-300 hover:z-10 hover:text-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-200 motion-reduce:transition-none"
          :style="wordStyle(word)"
          :title="`搜索 ${word.text}（${word.count} 次）`"
          :aria-label="`搜索 ${word.text}，出现 ${word.count} 次`"
          @click="applyWord(word.text)"
        >{{ word.text }}</button>
      </div>
      <div v-else class="flex h-56 items-center justify-center text-xs text-gray-400 lg:h-auto lg:flex-1">
        暂无搜索数据
      </div>
    </section>

    <footer class="card mt-4 p-5 text-xs text-gray-500">
      <div class="space-y-1.5">
        <div>
          <a class="transition hover:text-blue-600" target="_blank" rel="noopener" href="http://beian.miit.gov.cn">
            京 ICP 备 2020039820 号 - 1
          </a>
        </div>
        <div>
          <a class="inline-flex items-center gap-1 transition hover:text-blue-600"
             target="_blank"
             rel="noopener"
             href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802033291">
            <img class="h-3.5 w-3.5" src="https://beian.mps.gov.cn/img/logo01.dd7ff50e.png" alt="">
            京公网安备 11010802033291 号
          </a>
        </div>
      </div>

      <div class="mt-4 flex items-center justify-between border-t border-gray-100 pt-3">
        <button ref="contactBtn" class="font-medium text-blue-600 transition hover:text-blue-700" @click="openDrawer">
          与我联系
        </button>
        <span>© {{ currentYear }} HalfCoke</span>
      </div>
    </footer>

    <transition name="fade">
      <div v-if="drawer" class="fixed inset-0 z-50 bg-gray-900/40" aria-hidden="true" @click="closeDrawer"></div>
    </transition>
    <transition name="slide">
      <aside
        v-if="drawer"
        ref="drawer"
        class="fixed inset-y-0 right-0 z-50 flex w-80 max-w-[85vw] flex-col overflow-y-auto bg-white p-6 shadow-2xl"
        role="dialog"
        aria-modal="true"
        aria-label="联系方式"
        @keydown.esc="closeDrawer"
      >
        <div class="flex items-center justify-between">
          <h3 class="text-base font-semibold text-gray-900">联系方式</h3>
          <button
            ref="closeBtn"
            class="flex h-8 w-8 items-center justify-center rounded-full text-gray-400 transition hover:bg-gray-100 hover:text-gray-600"
            aria-label="关闭"
            @click="closeDrawer"
          >
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <div class="mt-8 space-y-5 text-sm text-gray-600">
          <div>
            <span class="text-xs text-gray-400">邮箱</span>
            <p class="mt-1">halfcoke@163.com</p>
          </div>
          <div>
            <span class="text-xs text-gray-400">博客</span>
            <p class="mt-1">
              <a class="text-blue-600 transition hover:text-blue-700" href="https://halfcoke.github.io/" target="_blank"
                 rel="noopener">
                https://halfcoke.github.io
              </a>
            </p>
          </div>
          <div>
            <span class="text-xs text-gray-400">公众号</span>
            <p class="mt-1">微信搜索 “Coder沙拉” 或 “half_640”</p>
            <div class="mt-3 flex justify-center">
              <img class="w-2/3 rounded-lg border border-gray-100"
                   src="https://cdn.osyb.cn/gh/HalfCoke/blog_img@master/img/202205011147820.png"
                   alt="公众号二维码">
            </div>
          </div>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script>
import store from '@/store'
import { request } from '@/requests'

const POLL_INTERVAL = 5000
const MAX_WORDS = 24
const MIN_FONT_SIZE = 11
const MAX_FONT_SIZE = 34
// 颜色由浅到深：blue-200 -> blue-900
const COLOR_LIGHT = [191, 219, 254]
const COLOR_DARK = [30, 58, 138]
// 检索词拆分后的无意义词，避免长句查询里的虚词占据词云
const STOP_WORDS = new Set([
  'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'in', 'is', 'it',
  'of', 'on', 'or', 'the', 'to', 'with', 'you', 'your', 'all', 'need', 'via', 'using',
  'based', 'towards', 'toward', 'into', 'over', 'under', 'between', 'we', 'our',
  'this', 'that', 'its', 'their', 'can', 'do', 'does', 'not'
])

export default {
  name: 'content_other',
  data () {
    return {
      drawer: false,
      keywords: [],
      placedWords: [],
      maxWeight: 1,
      minWeight: 1,
      timer: null,
      refreshTimer: null,
      resizeTimer: null,
      measureCtx: null,
      observer: null,
      inViewport: true,
      pageVisible: true,
      lastSignature: ''
    }
  },
  computed: {
    currentYear () {
      return new Date().getFullYear()
    },
    searchSeq () {
      return store.state.search_seq
    },
    searchDoneSeq () {
      return store.state.search_done_seq
    }
  },
  watch: {
    // 点击词云后与检索完成后都立即更新一次，保证词云随搜索频次实时变化
    searchSeq () {
      this.scheduleRefresh()
    },
    searchDoneSeq () {
      this.scheduleRefresh()
    }
  },
  mounted () {
    window.addEventListener('resize', this.handleResize)
    document.addEventListener('visibilitychange', this.handleVisibility)
    // 组件滚出视口或标签页切到后台时暂停轮询，回到可见时立即刷新
    if ('IntersectionObserver' in window) {
      this.observer = new IntersectionObserver(entries => {
        this.inViewport = entries[0].isIntersecting
        this.syncPolling()
      }, { rootMargin: '100px' })
      this.observer.observe(this.$refs.section)
    }
    this.syncPolling()
  },
  beforeDestroy () {
    this.stopPolling()
    clearTimeout(this.refreshTimer)
    clearTimeout(this.resizeTimer)
    window.removeEventListener('resize', this.handleResize)
    document.removeEventListener('visibilitychange', this.handleVisibility)
    if (this.observer) this.observer.disconnect()
  },
  methods: {
    startPolling () {
      if (this.timer) return
      this.timer = setInterval(this.getKeyWord, POLL_INTERVAL)
    },
    stopPolling () {
      clearInterval(this.timer)
      this.timer = null
    },
    handleVisibility () {
      this.pageVisible = !document.hidden
      this.syncPolling()
    },
    syncPolling () {
      const active = this.pageVisible && this.inViewport
      if (!active) {
        this.stopPolling()
        return
      }
      this.startPolling()
      this.getKeyWord()
    },
    openDrawer () {
      this.drawer = true
      this.$nextTick(() => {
        if (this.$refs.closeBtn) this.$refs.closeBtn.focus()
      })
    },
    closeDrawer () {
      this.drawer = false
      if (this.$refs.contactBtn) this.$refs.contactBtn.focus()
    },
    scheduleRefresh () {
      clearTimeout(this.refreshTimer)
      this.refreshTimer = setTimeout(this.getKeyWord, 400)
    },
    handleResize () {
      clearTimeout(this.resizeTimer)
      this.resizeTimer = setTimeout(this.layoutWords, 200)
    },
    // 以最高频词为中心，按频次由内向外做螺旋布局，并做碰撞检测
    layoutWords () {
      const box = this.$refs.cloud
      if (!box) return
      const width = box.clientWidth
      const height = box.clientHeight
      if (!width || !height) return
      if (!this.measureCtx) {
        this.measureCtx = document.createElement('canvas').getContext('2d')
      }
      const ctx = this.measureCtx
      const placed = []
      const cx = width / 2
      const cy = height / 2
      const gap = 4
      this.keywords.forEach((word, index) => {
        const style = this.wordStyle(word)
        ctx.font = `${style.fontWeight} ${style.fontSize} system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`
        const w = ctx.measureText(word.text).width + 6
        const h = parseFloat(style.fontSize) * 1.2
        let spot = null
        if (index === 0) {
          spot = { x: cx, y: cy }
        } else {
          for (let step = 1; step < 700; step++) {
            const angle = step * 2.39996322
            const radius = 3 + step * 1.6
            const x = cx + Math.cos(angle) * radius
            const y = cy + Math.sin(angle) * radius * 0.66
            if (x - w / 2 < 1 || x + w / 2 > width - 1 || y - h / 2 < 1 || y + h / 2 > height - 1) continue
            const collides = placed.some(p =>
              Math.abs(p.x - x) < (p.w + w) / 2 + gap && Math.abs(p.y - y) < (p.h + h) / 2 + gap
            )
            if (!collides) {
              spot = { x, y }
              break
            }
          }
        }
        if (!spot) return
        placed.push({ ...word, x: spot.x, y: spot.y, w, h })
      })
      this.placedWords = placed
    },
    wordStyle (word) {
      // 频次做 min-max 归一化，避免最大值把其他词的差异压平
      const span = this.maxWeight - this.minWeight
      const ratio = span > 0 ? (word.count - this.minWeight) / span : 1
      const size = Math.round(MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * Math.pow(ratio, 0.8))
      const style = {
        fontSize: `${size}px`,
        color: this.mixColor(ratio),
        fontWeight: Math.round(400 + 200 * ratio)
      }
      if (word.x !== undefined) {
        style.left = `${word.x}px`
        style.top = `${word.y}px`
      }
      return style
    },
    mixColor (ratio) {
      const rgb = COLOR_LIGHT.map((start, i) => Math.round(start + (COLOR_DARK[i] - start) * ratio))
      return `rgb(${rgb.join(', ')})`
    },
    buildKeywords (words) {
      // 短语按空格拆词后按词累计频次，忽略大小写合并同一词
      const map = new Map()
      for (const [phrase, count] of words) {
        if (!phrase || phrase.length > 40 || phrase.indexOf('\\') !== -1) continue
        for (const raw of phrase.split(/\W+/)) {
          const token = raw.trim()
          if (token.length < 2) continue
          const key = token.toLowerCase()
          if (STOP_WORDS.has(key)) continue
          const item = map.get(key)
          if (item) {
            item.count += count
          } else {
            map.set(key, { text: token, count })
          }
        }
      }
      return [...map.values()]
        .sort((a, b) => b.count - a.count)
        .slice(0, MAX_WORDS)
    },
    getKeyWord () {
      request({
        url: '/api/v1/getkeyword',
        method: 'post',
        data: {
          top_k: 50,
          recent_k: 10
        }
      }).then(res => {
        const next = this.buildKeywords(res.data.most_search_word || [])
        // 数据没变化时跳过重新布局，避免每 5 秒无意义的重排与动画抖动
        const signature = next.map(word => `${word.text}:${word.count}`).join('|')
        if (signature === this.lastSignature) return
        this.lastSignature = signature
        this.keywords = next
        if (this.keywords.length) {
          this.maxWeight = this.keywords[0].count
          this.minWeight = this.keywords[this.keywords.length - 1].count
        } else {
          this.maxWeight = 1
          this.minWeight = 1
        }
        this.placedWords = []
        this.$nextTick(this.layoutWords)
      }).catch(() => {})
    },
    applyWord (word) {
      store.commit('mutate_search_keys', word)
    }
  }
}
</script>
