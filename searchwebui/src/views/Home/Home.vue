<template>
  <div class="flex min-h-screen flex-col bg-gray-50">
    <navbar/>
    <main class="flex-1">
      <main_intro/>
      <main_content/>
    </main>
    <page_footer/>
  </div>
</template>

<script>
import Navbar from '@/components/navbar/navbar'
import Main_intro from '@/components/main_intro/main_intro'
import Main_content from '@/components/main_content/main_content'
import Page_footer from '@/components/page_footer/page_footer'

export default {
  name: 'Home',
  components: { Main_content, Main_intro, Navbar, Page_footer }
}
</script>
