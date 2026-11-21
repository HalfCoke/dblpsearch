<template>
  <div>
    <footer class="mt-8 border-t border-gray-200 bg-white">
      <div
        class="mx-auto flex w-full max-w-7xl flex-col gap-3 px-4 py-6 text-xs text-gray-500 sm:px-6 md:flex-row md:items-center md:justify-between lg:px-8"
      >
        <div class="flex flex-col gap-1.5 sm:flex-row sm:items-center sm:gap-4">
          <a class="transition hover:text-blue-600" target="_blank" rel="noopener" href="http://beian.miit.gov.cn">
            京 ICP 备 2020039820 号 - 1
          </a>
          <a class="inline-flex items-center gap-1 transition hover:text-blue-600"
             target="_blank"
             rel="noopener"
             href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802033291">
            <img class="h-3.5 w-3.5" src="https://beian.mps.gov.cn/img/logo01.dd7ff50e.png" alt="">
            京公网安备 11010802033291 号
          </a>
        </div>

        <div class="flex items-center justify-between gap-4 md:justify-end">
          <button ref="contactBtn" class="font-medium text-blue-600 transition hover:text-blue-700" @click="openDrawer">
            与我联系
          </button>
          <span>© {{ currentYear }} HalfCoke</span>
        </div>
      </div>
    </footer>

    <transition name="fade">
      <div v-if="drawer" class="fixed inset-0 z-50 bg-gray-900/40" aria-hidden="true" @click="closeDrawer"></div>
    </transition>
    <transition name="slide">
      <aside
        v-if="drawer"
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
export default {
  name: 'page_footer',
  data () {
    return {
      drawer: false
    }
  },
  computed: {
    currentYear () {
      return new Date().getFullYear()
    }
  },
  methods: {
    openDrawer () {
      this.drawer = true
      this.$nextTick(() => {
        if (this.$refs.closeBtn) this.$refs.closeBtn.focus()
      })
    },
    closeDrawer () {
      this.drawer = false
      if (this.$refs.contactBtn) this.$refs.contactBtn.focus()
    }
  }
}
</script>
