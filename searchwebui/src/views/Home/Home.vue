<template>
  <div class="flex min-h-screen flex-col bg-gray-50">
    <navbar/>
    <main_intro/>
    <main_content/>
  </div>
</template>

<script>
import Navbar from '@/components/navbar/navbar'
import Main_intro from '@/components/main_intro/main_intro'
import Main_content from '@/components/main_content/main_content'

export default {
  name: 'Home',
  components: { Main_content, Main_intro, Navbar }
}
</script>
