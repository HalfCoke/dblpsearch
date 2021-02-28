<template xmlns="http://www.w3.org/1999/html">
  <div class="main-pic">
    <div class="main-text">
      <p>
        基于DBLP数据及CCF推荐会议和期刊分类目录检索工具</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "main_intro"
}
</script>

<style lang="less" scoped>
@height: 330px;
.main-pic {
  height: @height;
  width: 100%;
  overflow: hidden;
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-image: url("https://gitee.com/halfcoke/blog_img/raw/master/20210226204012.webp");
}

.main-text {
  overflow: hidden;
  height: @height;
  width: 100%;
  font-style: normal;
  font-weight: bold;
  font-size: 48px;
  text-align: center;
  color: #FFFFFF;
  p{
    line-height: @height;
    margin: 0 auto;
  }
}
</style>
