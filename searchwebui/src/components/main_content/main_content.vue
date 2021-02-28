<template>
  <div class="main_content_wrapper">
    <el-row :gutter="70">
      <el-col :span="6">
        <div class="grid-content">
          <content_filter/>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="grid-content search_block">
          <content_search/>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="grid-content">
          <content_other/>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>

import Content_filter from "@/components/main_content/content_filter/content_filter";
import Content_other from "@/components/main_content/content_other/content_other";
import Content_search from "@/components/main_content/content_search/content_search";
export default {
  name: "main_content",
  components: { Content_search, Content_other, Content_filter }
}
</script>

<style lang="less" scoped>
.main_content_wrapper {
  width: 85%;
  margin-top: 20px;
  overflow: hidden;
  margin-right: auto;
  margin-left: auto;
}

.el-row {
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
}
.el-col {
  border-radius: 4px;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.search_block{
  background-color: #fff;
  padding: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>
