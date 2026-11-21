<template>
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

      <span>© {{ currentYear }} HalfCoke</span>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'page_footer',
  computed: {
    currentYear () {
      return new Date().getFullYear()
    }
  }
}
</script>
