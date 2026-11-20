<template>
  <section class="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
    <div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
      <aside class="order-2 lg:order-1 lg:col-span-3">
        <content_filter/>
      </aside>
      <div class="order-1 lg:order-2 lg:col-span-6">
        <content_search/>
      </div>
      <aside class="order-3 lg:col-span-3">
        <content_other/>
      </aside>
    </div>
  </section>
</template>

<script>
import Content_filter from '@/components/main_content/content_filter/content_filter'
import Content_other from '@/components/main_content/content_other/content_other'
import Content_search from '@/components/main_content/content_search/content_search'

export default {
  name: 'main_content',
  components: { Content_search, Content_other, Content_filter }
}
</script>
