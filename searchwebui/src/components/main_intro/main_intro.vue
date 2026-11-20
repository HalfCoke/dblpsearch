<template>
  <section class="relative flex h-64 items-center justify-center overflow-hidden sm:h-80">
    <div class="absolute inset-0 bg-cover bg-center" :style="backgroundStyle"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-gray-900/60 via-gray-900/45 to-gray-900/60"></div>
    <div class="relative px-4 text-center">
      <h1 class="text-2xl font-bold leading-snug tracking-tight text-white sm:text-4xl lg:text-5xl">
        基于 DBLP 数据及 CCF 推荐会议和期刊分类目录检索工具
      </h1>
      <p class="mt-4 text-sm text-white/80 sm:text-base">当前仅支持英文检索</p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'main_intro',
  data () {
    return {
      backgroundStyle: {
        backgroundImage: 'url("https://cdn.osyb.cn/gh/HalfCoke/blog_img@master/img/202205011158935.webp")'
      }
    }
  }
}
</script>
