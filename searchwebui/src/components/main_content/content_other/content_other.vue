<template>
  <div>
    <section class="card p-5">
      <h2 class="text-sm font-semibold text-gray-900">热门搜索</h2>
      <div class="mt-3 h-40 w-full">
        <vue-word-cloud
          v-if="keywords.length"
          class="h-full w-full"
          :words="keywords"
          :color="wordColor"
          :font-size-ratio="8"
          :spacing="3"
          font-family="sans-serif"
        />
        <div v-else class="flex h-full items-center justify-center text-xs text-gray-400">
          暂无搜索数据
        </div>
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
        <button class="font-medium text-blue-600 transition hover:text-blue-700" @click="drawer = true">
          与我联系
        </button>
        <span>© {{ currentYear }} HalfCoke</span>
      </div>
    </footer>

    <transition name="fade">
      <div v-if="drawer" class="fixed inset-0 z-50 bg-gray-900/40" @click="drawer = false"></div>
    </transition>
    <transition name="slide">
      <aside v-if="drawer" class="fixed inset-y-0 right-0 z-50 flex w-80 max-w-[85vw] flex-col bg-white p-6 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-semibold text-gray-900">联系方式</h3>
          <button
            class="flex h-8 w-8 items-center justify-center rounded-full text-gray-400 transition hover:bg-gray-100 hover:text-gray-600"
            aria-label="关闭"
            @click="drawer = false"
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
import VueWordCloud from 'vuewordcloud'
import { request } from '@/requests'

export default {
  name: 'content_other',
  components: { VueWordCloud },
  data () {
    return {
      drawer: false,
      keywords: [],
      maxWeight: 1,
      timer: null
    }
  },
  computed: {
    currentYear () {
      return new Date().getFullYear()
    }
  },
  created () {
    this.getKeyWord()
    this.timer = setInterval(this.getKeyWord, 10000)
  },
  beforeDestroy () {
    clearInterval(this.timer)
  },
  methods: {
    wordColor ([, weight]) {
      if (weight >= this.maxWeight * 0.6) return '#1d4ed8'
      if (weight >= this.maxWeight * 0.3) return '#3b82f6'
      return '#93c5fd'
    },
    buildKeywords (words) {
      const map = new Map()
      for (const [phrase, count] of words) {
        if (!phrase || phrase.length > 40 || phrase.indexOf('\\') !== -1) continue
        for (const token of phrase.split(/\W/)) {
          if (!token) continue
          map.set(token, (map.get(token) || 0) + count)
        }
      }
      return [...map.entries()]
        .sort((a, b) => b[1] - a[1])
        .slice(0, 15)
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
        this.keywords = this.buildKeywords(res.data.most_search_word || [])
        this.maxWeight = this.keywords.length ? this.keywords[0][1] : 1
      }).catch(() => {})
    }
  }
}
</script>
