<template>
  <div class="content_other">
    <div class="text">
      <p>最近搜索</p>
    </div>
    <div class="text">
      <p>...</p>
    </div>
    <div class="text">
      <p>最多搜索</p>
    </div>
    <div class="text">
      <p>...</p>
    </div>
    <div class="beian">
      <div class="icp">
        <a target="_blank" href="http://beian.miit.gov.cn">京 ICP 备 2020039820 号 - 1</a>
      </div>
      <div class="gongan">
        <a class="gongan_link"
           target="_blank" href="http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802033291">
          <img src="https://gitee.com/halfcoke/blog_img/raw/master/img/gongAn.png" alt=""/>
          京公网安备 11010802033291 号
        </a>
      </div>
    </div>
    <div class="contact_wrapper">
      <span class="contact"
            @click="showContact">
        与我联系
      </span>
      © 2021 HalfCoke
    </div>
  </div>
</template>

<script>
export default {
  name: "content_other",
  methods: {
    showContact () {
      //todo:显示联系方式
      console.log("contact")
    }
  }
}
</script>

<style lang="less" scoped>
.text {
  font-style: normal;
  font-weight: bold;
  font-size: 16px;
  color: #18181B;
}

.beian {
  a {
    text-decoration: none;
    color: #859dc2;
    font-size: 13px;
    height: 26px;

    &:hover {
      color: #175199;
    }
  }

  .gongan {
    .gongan_link {
      display: inline-flex;
      align-items: center;
    }

    img {
      margin-right: 4px;
    }
  }
}

.contact_wrapper {
  font-size: 13px;
  color: #859dc2;

  .contact:hover {
    color: #175199;
  }
}
</style>
